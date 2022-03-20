# Generated by Django 4.0.3 on 2022-03-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_patient_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Nonbinary'), ('O', 'Other')], max_length=1, null=True),
        ),
    ]