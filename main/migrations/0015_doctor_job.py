# Generated by Django 4.0.3 on 2022-03-19 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_doctor_special'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='job',
            field=models.CharField(default='Working', max_length=100),
        ),
    ]
