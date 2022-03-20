from operator import le
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    special = models.CharField(max_length=100, default="General")
    job = models.CharField(max_length=100, default="Working")


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    doctors = models.ManyToManyField(Doctor, blank=True)
    dob = models.DateTimeField(null=True)
    medcond = models.CharField(max_length=10000, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Nonbinary')
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="Please choose your gender")


class Document(models.Model):
    doc = models.FileField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, default=None)


class Prescription(models.Model):
    prescription = models.FileField(null=True)
    senderPrivate = models.CharField(max_length=64, null=True, blank=True)
    senderPublic = models.CharField(max_length=64, null=True, blank=True)
    recipientPublic = models.CharField(max_length=64, null=True, blank=True)
    hash = models.CharField(max_length=64, null=True, blank=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, default=None)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, default=None)
