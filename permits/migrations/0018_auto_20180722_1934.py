# Generated by Django 2.0.5 on 2018-07-22 19:34

from django.db import migrations, models
import django.db.models.deletion
import permits.models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0017_auto_20180721_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewcomment',
            name='macro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permits.StockComment'),
        ),
        migrations.AlterField(
            model_name='grading',
            name='grading_plan',
            field=models.FileField(blank=True, help_text='    Provide a PDF that includes the grading, drainage and erosion control plans.', null=True, upload_to=permits.models.grading_file_path),
        ),
        migrations.AlterField(
            model_name='projectinformation',
            name='zoning',
            field=models.CharField(choices=[('FP', 'FP - floodplain district'), ('C-3', 'C-3 - general commercial district'), ('R-1', 'R-1 - single-family district'), ('AF', 'AF - agriculture and forestry district'), ('R-7', 'R-7 - manufactured home park district'), ('I-2', 'I-2 - light industrial district'), ('DOD', 'DOD - design overlay district'), ('PR', 'PR - Park and recreation district'), ('MF-12', 'MF-12 - multifamily district'), ('R-6', 'R-6 - high-rise apartment district'), ('PRD', 'PRD - planned residential district'), ('R-4A', 'R-4A - low density residential district'), ('R-3', 'R-3 - single-family district'), ('PCD', 'PCD - planned commercial district'), ('MF-6', 'MF-6 - multifamily district'), ('UU', 'UU - urban use district.'), ('I-1', 'I-1 - industrial park district'), ('R-5', 'R-5 - urban residence district'), ('R-4', 'R-4 - two-family district'), ('POD', 'POD - planned office district'), ('R-2', 'R-2 - single-family district'), ('OS', 'OS - open space district'), ('C-2', 'C-2 - shopping center district'), ('C-1', 'C-1 - neighborhood commercial district'), ('MF-18', 'MF-18 - multifamily district'), ('PID', 'PID - planned industrial district'), ('M', 'M - mining district'), ('MF-24', 'MF-24 - multifamily district'), ('R-7A', 'R-7A - manufactured home district'), ('I-3', 'I-3 - heavy industrial district'), ('O-2', 'O-2 - office and institutional district'), ('O-3', 'O-3 - general office district'), ('PD', 'PD - industrial district'), ('O-1', 'O-1 - quiet office district'), ('C-4', 'C-4 - open display commercial district')], max_length=20),
        ),
    ]