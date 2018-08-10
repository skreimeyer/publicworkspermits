# Generated by Django 2.0.5 on 2018-07-10 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import permits.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('permits', '0004_auto_20180709_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='approval',
            name='conditional',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='approval',
            name='final',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviewcomment',
            name='application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='permits.Application'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='franchise',
            name='drawings',
            field=models.FileField(blank=True, help_text='Drawings must     be show the dimensions and location of the item to be franchised. Surveys,     blueprints, plans, or other dimensioned graphics are acceptable.', null=True, upload_to=permits.models.franchise_file_path),
        ),
        migrations.AlterField(
            model_name='permit',
            name='name',
            field=models.CharField(choices=[('SFHA', 'Special Flood Hazard Area'), ('GP', 'Grading'), ('FR', 'Franchise')], max_length=4),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='zoning',
            field=models.CharField(choices=[('MF-6', 'MF-6 - multifamily district'), ('MF-18', 'MF-18 - multifamily district'), ('C-3', 'C-3 - general commercial district'), ('R-2', 'R-2 - single-family district'), ('R-6', 'R-6 - high-rise apartment district'), ('MF-12', 'MF-12 - multifamily district'), ('DOD', 'DOD - design overlay district'), ('OS', 'OS - open space district'), ('I-3', 'I-3 - heavy industrial district'), ('AF', 'AF - agriculture and forestry district'), ('O-2', 'O-2 - office and institutional district'), ('PID', 'PID - planned industrial district'), ('R-3', 'R-3 - single-family district'), ('R-4A', 'R-4A - low density residential district'), ('UU', 'UU - urban use district.'), ('PR', 'PR - Park and recreation district'), ('FP', 'FP - floodplain district'), ('C-4', 'C-4 - open display commercial district'), ('O-1', 'O-1 - quiet office district'), ('C-1', 'C-1 - neighborhood commercial district'), ('POD', 'POD - planned office district'), ('R-1', 'R-1 - single-family district'), ('I-1', 'I-1 - industrial park district'), ('R-7A', 'R-7A - manufactured home district'), ('R-5', 'R-5 - urban residence district'), ('PRD', 'PRD - planned residential district'), ('C-2', 'C-2 - shopping center district'), ('R-7', 'R-7 - manufactured home park district'), ('PCD', 'PCD - planned commercial district'), ('O-3', 'O-3 - general office district'), ('MF-24', 'MF-24 - multifamily district'), ('I-2', 'I-2 - light industrial district'), ('PD', 'PD - industrial district'), ('R-4', 'R-4 - two-family district'), ('M', 'M - mining district')], max_length=20),
        ),
    ]