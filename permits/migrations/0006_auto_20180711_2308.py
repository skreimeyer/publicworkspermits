# Generated by Django 2.0.5 on 2018-07-11 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0005_auto_20180710_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='zoning',
            field=models.CharField(choices=[('R-1', 'R-1 - single-family district'), ('R-7A', 'R-7A - manufactured home district'), ('I-2', 'I-2 - light industrial district'), ('C-1', 'C-1 - neighborhood commercial district'), ('POD', 'POD - planned office district'), ('C-2', 'C-2 - shopping center district'), ('PD', 'PD - industrial district'), ('FP', 'FP - floodplain district'), ('DOD', 'DOD - design overlay district'), ('PCD', 'PCD - planned commercial district'), ('MF-18', 'MF-18 - multifamily district'), ('O-1', 'O-1 - quiet office district'), ('R-4A', 'R-4A - low density residential district'), ('PR', 'PR - Park and recreation district'), ('AF', 'AF - agriculture and forestry district'), ('M', 'M - mining district'), ('R-5', 'R-5 - urban residence district'), ('C-4', 'C-4 - open display commercial district'), ('I-3', 'I-3 - heavy industrial district'), ('R-6', 'R-6 - high-rise apartment district'), ('PID', 'PID - planned industrial district'), ('R-2', 'R-2 - single-family district'), ('I-1', 'I-1 - industrial park district'), ('MF-24', 'MF-24 - multifamily district'), ('R-3', 'R-3 - single-family district'), ('R-4', 'R-4 - two-family district'), ('C-3', 'C-3 - general commercial district'), ('UU', 'UU - urban use district.'), ('MF-6', 'MF-6 - multifamily district'), ('O-3', 'O-3 - general office district'), ('OS', 'OS - open space district'), ('MF-12', 'MF-12 - multifamily district'), ('O-2', 'O-2 - office and institutional district'), ('PRD', 'PRD - planned residential district'), ('R-7', 'R-7 - manufactured home park district')], max_length=20),
        ),
    ]