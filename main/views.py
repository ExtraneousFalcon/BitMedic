from pydoc import Doc
from aiohttp import request
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .models import Document, Doctor, Patient
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import SignUpForm, Prescription


@login_required(login_url='login/')
def home(request):
    is_patient = False
    if Patient.objects.filter(user=request.user).exists():
        is_patient = True
    context = {}
    context["is_patient"] = is_patient
    """if(request.method == 'POST'):
        fs = FileSystemStorage()
        uploaded_file = request.FILES['document']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = url
        patient = Patient.objects.get(
            user=User.objects.get(username=request.user))
        print(patient)
        doc = Document(path=uploaded_file.name, patient=patient, doc=url)
        doc.save()"""
    return render(request, "main/home.html", context)


class DocumentView(CreateView):
    model = Document
    template_name = "main/document_form.html"
    fields = ['doc']
    success_url = reverse_lazy('upload')

    def form_valid(self, form):
        review = form.save(commit=False)
        try:
            doctor = Doctor.objects.get(
                user=User.objects.get(username=self.request.user))
            patient = self.request.build_absolute_uri()
            patient = patient.split("/")[-1]
            review.patient = Patient.objects.get(
                user=User.objects.get(username=patient))
            review.save()
            return HttpResponseRedirect(reverse('patient', args=[patient]))

        except Doctor.DoesNotExist:
            review.patient = Patient.objects.get(user=self.request.user)
        review.save()
        return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Document.objects.all()
        return context


class CustomLoginView(LoginView):
    template_name = "main/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = "main/register.html"
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            if self.request.POST.get('role') == "2":
                p = Patient(user=self.request.user)
                p.save()
            else:
                d = Doctor(user=self.request.user)
                d.save()

        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')

        return super(RegisterPage, self).get(*args, **kwargs)


def filelistpatient(request):
    patient = Patient.objects.get(user=User.objects.get(username=request.user))
    files = Document.objects.filter(patient=patient)
    return render(request, "main/filelist.html", {'files': files})


def patientlist(request):
    doctor = Doctor.objects.get(user=User.objects.get(username=request.user))
    patients = Patient.objects.filter(doctors__in=[doctor])
    return render(request, "main/patientlist.html", {'patients': patients})


def patientview(request, name):
    patient = Patient.objects.get(user=User.objects.get(username=name))
    documents = Document.objects.filter(patient=patient)
    return render(request, "main/patientview.html", {'patient': patient, 'documents': documents})


def doctorlist(request):
    patient = Patient.objects.get(user=User.objects.get(username=request.user))
    doctors = patient.doctors.all()
    return render(request, "main/doctorlist.html", {"doctors": doctors})


def add_doctor(request):
    doctors = Doctor.objects.all()
    docList = []
    context = {}
    context['message'] = None
    for doctor in doctors:
        docList.append(doctor.user.username)
    if request.GET.get("name") in docList:
        patient = Patient.objects.get(user=request.user)
        patient.doctors.add(Doctor.objects.get(
            user=User.objects.get(username=request.GET.get("name"))))
    else:
        context['message'] = "Doctor not found"
    patient = Patient.objects.get(user=User.objects.get(username=request.user))
    context["doctors"] = patient.doctors.all()

    return render(request, "main/doctorlist.html", context)


def remove_doctor(request, doctor):
    docObject = Doctor.objects.get(user=User.objects.get(username=doctor))
    patients = Patient.objects.filter(doctors__in=[docObject])
    for patient in patients:
        patient.doctors.remove(docObject)
    return redirect('doctorlist')


class PrescriptionPage(FormView):
    template_name = "main/prescribe.html"
    form_class = Prescription
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        return HttpResponseRedirect(reverse('patient', args=[patient]))

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')

        return super(RegisterPage, self).get(*args, **kwargs)
