# Generated by Django 4.0.3 on 2022-03-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_doctor_job_alter_doctor_special'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='degree',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='special',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
