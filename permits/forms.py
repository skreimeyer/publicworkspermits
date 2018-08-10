from django import forms
from django.forms import NumberInput, formset_factory
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label="username",max_length=50)
    password = forms.CharField(widget=forms.PasswordInput,label="password",max_length=50)

class RegisterForm(forms.Form):
    username = forms.CharField(label="username",max_length=50,)
    password = forms.CharField(widget=forms.PasswordInput,label="password",max_length=50)
    first_name = forms.CharField(label="First Name",max_length=50,help_text="optional")
    last_name = forms.CharField(label="Last Name",max_length=50,help_text="optional")
    email = forms.EmailField(label="Email",max_length=50,help_text="A valid email\
    address to receive notifications.")

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = ApplicantInformation
        exclude = ['last_modified',]

class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectInformation
        exclude = ['last_modified',]

class SFHAForm(forms.ModelForm):
    class Meta:
        model = SFHA
        exclude = ['last_modified',]

class GradingForm(forms.ModelForm):
    class Meta:
        model = Grading
        exclude = ['last_modified',]
        widgets = {
        'construction_start':forms.SelectDateWidget,
        'construction_end':forms.SelectDateWidget,
        }

class FranchiseForm(forms.ModelForm):
    class Meta:
        model = Franchise
        exclude = ['last_modified',]

class ReviewFilter(forms.Form):

    OPTIONS = (
    ('None','All'),
    ('SFHA','Special Flood Hazard Area'),
    ('GP','Grading'),
    ('FR','Franchise'),
    )

    approved = forms.BooleanField(label="Approved",required=False)
    start = forms.DateField(widget=forms.SelectDateWidget,label="start date",
    required=False)
    end = forms.DateField(widget=forms.SelectDateWidget,label="end date",
    required=False)
    type = forms.ChoiceField(widget=forms.Select,
    choices=OPTIONS,required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        exclude = ['application','user','department','date']

    def __init__(self,permit,department,*args,**kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['macro'].queryset = StockComment.objects.filter(permit=permit,department=department)

class ApproveForm(forms.Form):
    conditional = forms.BooleanField(label="This project is approved with additional \
    conditions to be met prior to final approval",required=False)
    final = forms.BooleanField(label="This project is approved and all conditions \
    and staff comments have been addressed",required=False)
