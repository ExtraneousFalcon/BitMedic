from pydoc import Doc
from telnetlib import DO
from django.contrib import admin
from .models import Patient, Doctor, Document, Prescription

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Document)
admin.site.register(Prescription)
