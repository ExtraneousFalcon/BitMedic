from operator import le
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    doctors = models.ManyToManyField(Doctor, blank=True)


class Document(models.Model):
    doc = models.FileField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, default=None)


class Prescription(models.Model):
    file = models.FileField(null=True)
    hash = models.CharField(max_length=64)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, default=None)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, default=None)
