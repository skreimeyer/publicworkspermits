# Generated by Django 2.0.5 on 2018-07-12 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0008_auto_20180712_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permit',
            name='required_approvals',
            field=models.ManyToManyField(null=True, to='permits.Department'),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='zoning',
            field=models.CharField(choices=[('C-3', 'C-3 - general commercial district'), ('R-2', 'R-2 - single-family district'), ('O-1', 'O-1 - quiet office district'), ('O-2', 'O-2 - office and institutional district'), ('MF-24', 'MF-24 - multifamily district'), ('I-2', 'I-2 - light industrial district'), ('PR', 'PR - Park and recreation district'), ('M', 'M - mining district'), ('PCD', 'PCD - planned commercial district'), ('MF-18', 'MF-18 - multifamily district'), ('PRD', 'PRD - planned residential district'), ('AF', 'AF - agriculture and forestry district'), ('R-7A', 'R-7A - manufactured home district'), ('I-1', 'I-1 - industrial park district'), ('R-6', 'R-6 - high-rise apartment district'), ('DOD', 'DOD - design overlay district'), ('PID', 'PID - planned industrial district'), ('POD', 'POD - planned office district'), ('R-4', 'R-4 - two-family district'), ('MF-12', 'MF-12 - multifamily district'), ('OS', 'OS - open space district'), ('R-7', 'R-7 - manufactured home park district'), ('C-2', 'C-2 - shopping center district'), ('UU', 'UU - urban use district.'), ('O-3', 'O-3 - general office district'), ('R-3', 'R-3 - single-family district'), ('C-4', 'C-4 - open display commercial district'), ('PD', 'PD - industrial district'), ('FP', 'FP - floodplain district'), ('MF-6', 'MF-6 - multifamily district'), ('C-1', 'C-1 - neighborhood commercial district'), ('I-3', 'I-3 - heavy industrial district'), ('R-1', 'R-1 - single-family district'), ('R-4A', 'R-4A - low density residential district'), ('R-5', 'R-5 - urban residence district')], max_length=20),
        ),
    ]
