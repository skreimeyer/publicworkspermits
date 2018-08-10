from django.db import models
from django.forms import ModelForm
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User,Group

from datetime import datetime
import json

with open('permits/static/resources/codes.json','r') as infile:
    zoning_codes = json.load(infile)
    zoning_choices = [(key,zoning_codes[key]) for key in zoning_codes]


class ApplicantInformation(models.Model):
    """Contains contact information for applicants related to specific
    permit applications"""
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    agent_for = models.CharField(max_length=100,blank=True,null=True,
    help_text="Organization or person being represented for this application")
    applicant_address = models.CharField(max_length=50,blank=True,null=True,
    help_text="Address of applicant or agent if different from project address")
    applicant_city = models.CharField(max_length=50,blank=True,null=True)
    applicant_state = models.CharField(max_length=20,blank=True,null=True)
    applicant_zip = models.CharField(max_length=7,blank=True,null=True)
    applicant_phone = models.CharField(max_length=10,blank=True,null=True,
    help_text="Phone number (digits only): 5551234567")
    last_modified = models.DateField(auto_now=True)


class ProjectInformation(models.Model):
    """Contains the location and basic information about the location of
    projects for reference with the permit applications"""
    project_address = models.CharField(max_length=50,blank=True,null=True)
    project_city = models.CharField(max_length=50,)
    project_zip = models.CharField(max_length=7,)
    parcel_id = models.CharField(max_length=20,blank=True,null=True,help_text="Please \
    provide the county parcel id number if addressing is not available")
    zoning = models.CharField(max_length=20,choices=zoning_choices)
    engineer_of_record = models.CharField(max_length=100,blank=True,null=True)
    project_owner = models.CharField(max_length=50,help_text="Person, business \
    or organization with ownership of the project")
    project_description = models.TextField(help_text="A brief summary of the \
    project scope")
    last_modified = models.DateField(auto_now=True)


def sfha_file_path(instance,filename):
    today = str(datetime.now().date())
    return 'sfha/{0}-{1}-{2}'.format(instance.user.username,today,filename)

class SFHA(models.Model):
    """Special Flood Hazard Area Permit"""
    site_plan = models.FileField(upload_to=sfha_file_path,help_text="\
    Provide a PDF of the survey or site plans for the project.",blank=True,null=True)
    elevation_certificate = models.FileField(upload_to=sfha_file_path,help_text="\
    Provide an elevation certificate stamped by a professional land surveyor",
    blank=True,null=True)
    flood_proofing = models.FileField(upload_to=sfha_file_path,help_text="\
    Provide a flood-proofing certificate.",blank=True,null=True)
    no_rise_certificate = models.FileField(upload_to=sfha_file_path,help_text="\
    Provide an engineer's certificate of no-rise within the floodway.",
    blank=True,null=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.last_modified)


def grading_file_path(instance,filename):
    today = str(datetime.now().date())
    return 'grading/{0}-{1}-{2}'.format(instance.user.username,today,filename)

threshold_choices = (('SFHA','Project is located within the special flood \
                        hazard area'),
                        ('vertical','Ten or more vertical feet \
                        will be cut or filled'),
                        ('volume','Cut or fill will exceed 1000 cubic yards'),
                        ('trees','Seven or more trees will be removed'))

class Grading(models.Model):
    """Grading Permit"""
    grading_plan = models.FileField(upload_to=grading_file_path,help_text="\
    Provide a PDF that includes the grading, drainage and erosion control plans.",
    blank=True,null=True)
    threshold_condition = models.CharField(max_length=10,choices=threshold_choices)
    construction_start = models.DateField()
    construction_end = models.DateField()
    disturbed_area = models.FloatField(help_text='acres')
    soil_loss_pre = models.FloatField(help_text ='tons per acre')
    soil_loss_post = models.FloatField(help_text='tons per acre',)
    max_depth_of_fill = models.FloatField(help_text='feet',blank=True,null=True)
    volume_of_fill = models.FloatField(help_text='cubic yards',blank=True,null=True)
    haul_in = models.FloatField(help_text='cubic yards of material to be \
    hauled in excluding gravel and asphalt',blank=True,null=True)
    source_of_haul_material = models.CharField(max_length=100,blank=True,null=True,
    help_text='location of fill to be brought in')
    haul_out = models.FloatField(help_text='cubic yards of material to be \
    hauled off the project site')
    destination_of_haul_material = models.CharField(max_length=100,blank=True,null=True,
    help_text='destination of material taken from the project site')
    tracking_pads= models.TextField(help_text='approximate location of tracking \
    pads to prevent soil loss onto city streets')
    haul_route = models.TextField(help_text='route haul trucks will take to \
    access the project site')
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.last_modified)


def franchise_file_path(instance,filename):
    today = str(datetime.now().date())
    return 'franchise/{0}-{1}-{2}'.format(instance.user.username,today,filename)

class Franchise(models.Model):
    """Franchise Agreement"""
    contact = models.CharField(max_length=100,blank=True,null=True,
    help_text="Person or organization responsible for maintenance of the \
    item to be franchised.")
    contact_phone = models.CharField(max_length=10,blank=True,null=True,
    help_text="Contact number for questions about maintenance of the \
    item to be franchised.")
    contact_email = models.EmailField(blank=True,null=True,
    help_text="Email address for a person or organization responsible for the \
    maintenance of the item to be franchised.")
    reason = models.TextField(help_text="Please explain the need for a \
    right of way franchise permit.")
    drawings = models.FileField(upload_to=franchise_file_path,help_text="Drawings must \
    be show the dimensions and location of the item to be franchised. Surveys, \
    blueprints, plans, or other dimensioned graphics are acceptable.",blank=True,
    null=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.last_modified)


class Department(models.Model):
    """Subgrouping of reviewers based on the city department they work in."""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Permit(models.Model):
    """Permit names and basic information"""
    name = models.CharField(max_length=4,choices=(
    ('SFHA','Special Flood Hazard Area'),
    ('GP','Grading'),
    ('FR','Franchise'),
    ))
    flat_fee = models.BooleanField()
    permit_fee = models.FloatField(blank=True,null=True)
    required_approvals = models.ManyToManyField(Department)

    def __str__(self):
        return self.name


class Application(models.Model):
    """provides unique identification for an specific application to simplify
    foreign key relationships."""
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    applicant_info = models.ForeignKey(ApplicantInformation,on_delete=models.CASCADE,null=True)
    project_info = models.ForeignKey(ProjectInformation,on_delete=models.CASCADE,null=True)
    SFHA_permit = models.ForeignKey(SFHA,on_delete=models.CASCADE,blank=True,null=True)
    grading_permit = models.ForeignKey(Grading,on_delete=models.CASCADE,blank=True,null=True)
    franchise_permit = models.ForeignKey(Franchise,on_delete=models.CASCADE,blank=True,null=True)
    type = models.ForeignKey(Permit,on_delete=models.CASCADE,blank=True,null=True)
    paid = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        application_number = str(self.date_created.year+self.id)
        return application_number


class Approval(models.Model):
    """Table for managing approval of one user for one permit"""
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    application=models.ForeignKey(Application,on_delete=models.CASCADE)
    conditional = models.BooleanField(default=False,blank=True)
    final = models.BooleanField(default=False,blank=True)
    date=models.DateField(auto_now=True)


class UserDepartment(models.Model):
    """A table to extend the User table with Department used in lieu of adding
    foreign-key relationships into Django default tables"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)

    def __str__(self):
        uid = self.user.pk
        name = User.objects.get(pk=uid)
        name = name.username+'_department'
        return name


class StockComment(models.Model):
    """Frequently used comments for reviewers."""
    name = models.CharField(max_length=20)
    comment = models.TextField()
    permit = models.ForeignKey(Permit,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    default = models.BooleanField(
                        help_text="This comment will appear in all new reviews")
    acknowledge = models.BooleanField(default=True,
                                help_text="Applicant must acknowledge comment")
    respond = models.BooleanField(default=False,
                        help_text="Applicant must provide a written response")
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class ReviewComment(models.Model):
    """Comments made by reviewers about applications"""
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    macro = models.ForeignKey(StockComment,on_delete=models.CASCADE,blank=True,null=True)
    comment = models.TextField(blank=True,null=True)
    date = models.DateField(auto_now=True)
    acknowledge = models.BooleanField(default=False,blank=True,
                                help_text="Applicant must acknowledge comment")
    respond = models.BooleanField(default=False,blank=True,
                        help_text="Applicant must provide a written response")

    def __str__(self):
        return self.comment
