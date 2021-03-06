# Generated by Django 2.0.5 on 2018-07-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0020_auto_20180722_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinformation',
            name='zoning',
            field=models.CharField(choices=[('PID', 'PID - planned industrial district'), ('C-4', 'C-4 - open display commercial district'), ('OS', 'OS - open space district'), ('POD', 'POD - planned office district'), ('I-3', 'I-3 - heavy industrial district'), ('AF', 'AF - agriculture and forestry district'), ('M', 'M - mining district'), ('R-6', 'R-6 - high-rise apartment district'), ('O-2', 'O-2 - office and institutional district'), ('R-4', 'R-4 - two-family district'), ('I-2', 'I-2 - light industrial district'), ('FP', 'FP - floodplain district'), ('PCD', 'PCD - planned commercial district'), ('O-3', 'O-3 - general office district'), ('R-7A', 'R-7A - manufactured home district'), ('MF-24', 'MF-24 - multifamily district'), ('C-3', 'C-3 - general commercial district'), ('PD', 'PD - industrial district'), ('R-4A', 'R-4A - low density residential district'), ('C-2', 'C-2 - shopping center district'), ('R-2', 'R-2 - single-family district'), ('R-7', 'R-7 - manufactured home park district'), ('R-1', 'R-1 - single-family district'), ('MF-12', 'MF-12 - multifamily district'), ('R-3', 'R-3 - single-family district'), ('PRD', 'PRD - planned residential district'), ('O-1', 'O-1 - quiet office district'), ('MF-18', 'MF-18 - multifamily district'), ('UU', 'UU - urban use district.'), ('DOD', 'DOD - design overlay district'), ('R-5', 'R-5 - urban residence district'), ('I-1', 'I-1 - industrial park district'), ('MF-6', 'MF-6 - multifamily district'), ('PR', 'PR - Park and recreation district'), ('C-1', 'C-1 - neighborhood commercial district')], max_length=20),
        ),
    ]
