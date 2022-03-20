from pydoc import Doc
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .models import Document, Doctor, Patient, Prescription
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import SignUpForm

import web3
from web3 import Web3


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
            review.uploader = self.request.user
            review.save()
            return HttpResponseRedirect(reverse('patient', args=[patient]))

        except Doctor.DoesNotExist:
            review.patient = Patient.objects.get(user=self.request.user)
            review.uploader = self.request.user
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


class PrescriptionView(CreateView):
    model = Prescription
    template_name = "main/prescribe.html"
    fields = ['prescription', 'recipientPublic',
              'senderPrivate', 'senderPublic']
    success_url = reverse_lazy('upload')

    def form_valid(self, form):
        web3 = Web3(Web3.HTTPProvider(
            "https://rinkeby.infura.io/v3/4da2bf7c5bb44dfbbd576c6d166d7321"))
        chain_id = 4
        review = form.save(commit=False)
        review.doctor = Doctor.objects.get(
            user=User.objects.get(username=self.request.user))
        patient = self.request.build_absolute_uri()
        patient = patient.split("/")[-1]
        review.patient = Patient.objects.get(
            user=User.objects.get(username=patient))

        recipientPublicKey = review.recipientPublic
        senderPrivateKey = review.senderPrivate
        senderPublicKey = review.senderPublic
        nonce = web3.eth.getTransactionCount(senderPublicKey)
        tx = {
            'nonce': nonce,
            'to': recipientPublicKey,
            'value': web3.toWei(.01, 'ether'),
            'gas': 270000,
            'gasPrice': web3.toWei('55', 'gwei')
        }

        signedTx = web3.eth.account.signTransaction(tx, senderPrivateKey)
        send_store_tx = web3.eth.sendRawTransaction(signedTx.rawTransaction)
        temp = web3.eth.wait_for_transaction_receipt(send_store_tx)
        review.hash = temp.transactionHash.hex()
        review.save()
        return HttpResponseRedirect(reverse('patient', args=[patient]))


"""class PrescriptionPage(FormView):
    template_name = "main/prescribe.html"
    form_class = Prescription
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        pres = Prescription()
        return HttpResponseRedirect(reverse('patient', args=[patient]))

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')

        return super(RegisterPage, self).get(*args, **kwargs)
"""


def createpp(request):
    if request.method == "POST":
        patient = Patient.objects.get(user=request.user)
        if(request.POST.get("conditions")):
            patient.medcond = request.POST.get("conditions")
        if(request.POST.get("dob")):
            patient.dob = request.POST.get("dob")
        if(request.POST.get("phone")):
            patient.phone = request.POST.get("phone")

        patient.save()
        return redirect('profile')
    return render(request, "main/createpp.html", {"p": Patient.objects.get(user=request.user)})


def profile(request):
    p = Patient.objects.get(user=request.user)
    return render(request, "main/profile.html", {'patient': p})


def docprof(request, doctor):
    doc = Doctor.objects.get(user=User.objects.get(username=doctor))
    return render(request, "main/docprof.html", {'doctor': doc})


def createdp(request):
    if request.method == "POST":
        doctor = Doctor.objects.get(user=request.user)
        doctor.special = request.POST.get("special")
        doctor.job = request.POST.get("job")
        doctor.degree = request.POST.get("degree")
        doctor.save()
        return redirect('home')
    return render(request, "main/createdp.html")


def mypres(request):
    patient = Patient.objects.get(user=request.user)
    pres = Prescription.objects.filter(patient=patient)
    return render(request, "main/mypres.html", {"pres": pres})


def order(request, hash):
    if request.method == "POST":
        patient = Patient.objects.get(user=request.user)
        public = request.POST.get("public")
        private = request.POST.get("private")
        amount = request.POST.get("amount")

        web3 = Web3(Web3.HTTPProvider(
            "https://rinkeby.infura.io/v3/4da2bf7c5bb44dfbbd576c6d166d7321"))
        chain_id = 4

        recipientPublicKey = "0x4c05b9cbecD1d0A88f6CdD60B0Fe032EdD5a0172"

        nonce = web3.eth.getTransactionCount(public)
        tx = {
            'nonce': nonce,
            'to': recipientPublicKey,
            'value': web3.toWei(amount, 'ether'),
            'gas': 270000,
            'gasPrice': web3.toWei('55', 'gwei')
        }

        signedTx = web3.eth.account.signTransaction(tx, private)
        send_store_tx = web3.eth.sendRawTransaction(signedTx.rawTransaction)
        temp = web3.eth.wait_for_transaction_receipt(send_store_tx)
        pres = Prescription.objects.get(hash=hash)
        print(pres)
        hash = temp.transactionHash.hex()
        pres.redeemed = True
        pres.save()
        return redirect('mypres')
    return render(request, "main/order.html")
