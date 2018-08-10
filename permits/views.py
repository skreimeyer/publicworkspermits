# Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.views import generic
from django.forms import formset_factory, modelformset_factory
from django.core.paginator import Paginator
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

# Local imports
from .models import *
from .forms import *

# Common imports
from datetime import datetime
import os
import mimetypes
import decimal
import stripe

import pdb

def index(request):
    all_permits = Permit.objects.all()
    return render(request,'permits/index.html',{'permit_list':all_permits})

def success(request):
    return render(request,'permits/success.html')
    #Fees should be shown here.

def download(request,folder,filename):
    file_path = os.path.join(settings.MEDIA_ROOT,folder,filename)
    type,encoding = mimetypes.guess_type(filename)
    if type is None:
        type = 'application/octet-stream'
    if os.path.exists(file_path):
        with open(file_path,'rb') as f:
            response = HttpResponse(f.read(),content_type=type)
        if encoding is not None:
            response['Content-Encoding']=encoding
        response['Content-Disposition'] = 'inline; filename={0}'.format(filename)
    else:
        response = HttpResponseNotFound()
    return response

def user_login(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            message = "You are now logged in."
            return render(request,'permits/index.html',{'message':message})
        else:
            return render(request,'permits/index.html')
        #Add an error message here.
    else:
        return render(request,'permits/login.html',{'form':LoginForm})

def user_logout(request):
    logout(request,)
    message = "You are now logged out."
    return render(request,'permits/index.html',{'message':message})

def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            group_pk = Group.objects.get(name='Applicant').pk # get pk to pass to set
            new_user = User.objects.create_user(
                                                username=username,
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                )
            new_user.save()
            new_user.groups.set([group_pk,]) # Can't direct-assign to many-many
            new_user.save() # might be unnecessary . . .
            return render(request,'permits/index.html')
        else:
            error_message = "Invalid input. Please try again."
            return render(request,'permits/index.html',{'error_message':error_message}) # send a nastygram
    else:
        return render(request,'permits/register.html',{'form':RegisterForm})

def sfha(request):
    fee = Permit.objects.get(name='SFHA').permit_fee
    if request.method=="POST":
        appform = ApplicantForm(request.POST,prefix="app")
        prjform = ProjectForm(request.POST,prefix="prj")
        sfhaform = SFHAForm(request.POST,request.FILES,prefix="sfha")
        if appform.is_valid() and prjform.is_valid() and sfhaform.is_valid():
            appform = appform.save()
            prjform = prjform.save()
            sfhaform = sfhaform.save(commit=False)
            sfhaform.user = request.user
            sfhaform.save()
            application = Application.objects.create(user=request.user,
            type = Permit.objects.get(name='SFHA'),
            SFHA_permit=sfhaform,
            applicant_info=appform,
            project_info=prjform,)
            application.save()
            # create application object here
            request.session['application']=application.id
            request.session['fee']=fee
            return redirect('permits:payment')
        else:
            error_message = "Invalid input. Please try again."
            return render(request,'permits/sfha.html',{
                                                "error_message":error_message,
                                                'appform':appform,
                                                'prjform':prjform,
                                                'sfhaform':sfhaform})
    else:
        appform = ApplicantForm(prefix="app")
        prjform = ProjectForm(prefix="prj")
        sfhaform = SFHAForm(prefix="sfha")
        return render(request,'permits/sfha.html',{
                                                    'appform':appform,
                                                    'prjform':prjform,
                                                    'sfhaform':sfhaform,
                                                    'fee':fee,})

def grading(request):
    if request.method=="POST":
        appform = ApplicantForm(request.POST,prefix="app")
        prjform = ProjectForm(request.POST,prefix="prj")
        gradingform = GradingForm(request.POST,request.FILES,prefix="grading")
        if appform.is_valid() and prjform.is_valid() and gradingform.is_valid():
            appform = appform.save()
            prjform = prjform.save()
            gradingform = gradingform.save(commit=False)
            gradingform.user = request.user
            gradingform.save()
            application = Application.objects.create(user=request.user,
            type = Permit.objects.get(name='GP'),
            grading_permit=gradingform,
            applicant_info=appform,
            project_info=prjform,)
            application.save()
            # Wacky permit fee structure. Saturn, much?
            disturbed_area = gradingform.disturbed_area
            if disturbed_area <= 1.0:
                fee = 120.0*disturbed_area
            elif disturbed_area <= 10.0:
                fee = 120.0+disturbed_area*60.0
            else:
                fee = 660.0
            request.session['application']=application.id
            request.session['fee']=fee
            return redirect('permits:payment')
        else:
            error_message = "Invalid input. Please try again."
            return render(request,'permits/grading.html',{
                                                "error_message":error_message,
                                                'appform':appform,
                                                'prjform':prjform,
                                                'gradingform':gradingform})
    else:
        appform = ApplicantForm(prefix="app")
        prjform = ProjectForm(prefix="prj")
        gradingform = GradingForm(prefix="grading")
        return render(request,'permits/grading.html',{
                                                    'appform':appform,
                                                    'prjform':prjform,
                                                    'gradingform':gradingform})

def franchise(request):
    fee = Permit.objects.get(name='FR').permit_fee
    if request.method=="POST":
        appform = ApplicantForm(request.POST,prefix="app")
        prjform = ProjectForm(request.POST,prefix="prj")
        franchiseform = FranchiseForm(request.POST,request.FILES,prefix="franchise")
        if appform.is_valid() and prjform.is_valid() and franchiseform.is_valid():
            appform = appform.save()
            prjform = prjform.save()
            franchiseform = franchiseform.save(commit=False)
            franchiseform.user = request.user
            franchiseform.save()
            application = Application.objects.create(user=request.user,
            type = Permit.objects.get(name='FR'),
            franchise_permit=franchiseform,
            applicant_info=appform,
            project_info=prjform,)
            application.save()
            request.session['application']=application.id
            request.session['fee']=fee
            return redirect('permits:payment')
        else:
            error_message = "Invalid input. Please try again."
            return render(request,'permits/franchise.html',{
                                                "error_message":error_message,
                                                'appform':appform,
                                                'prjform':prjform,
                                                'franchiseform':franchiseform})
    else:
        appform = ApplicantForm(prefix="app")
        prjform = ProjectForm(prefix="prj")
        franchiseform = FranchiseForm(prefix="franchise")
        return render(request,'permits/franchise.html',{
                                                    'appform':appform,
                                                    'prjform':prjform,
                                                    'franchiseform':franchiseform
                                                    })

def my_applications(request):
    application = Application.objects.select_related().filter(user=request.user)
    return render(request,'permits/my_applications.html',{'application':application})

def my_app_detail(request,pk):
    application = get_object_or_404(Application,pk=pk)
    if application.user == request.user:
        if request.method=="POST":
            appform=ApplicantForm(request.POST,instance=application.applicant_info)
            prjform=ProjectForm(request.POST,instance=application.project_info)
            if application.SFHA_permit:
                spcform = SFHAForm(request.POST,request.FILES,instance=application.SFHA_permit)
            elif application.grading_permit:
                spcform = GradingForm(request.POST,request.FILES,instance=application.grading_permit)
            elif application.franchise_permit:
                spcform = FranchiseForm(request.POST,request.FILES,instance=application.franchise_permit)
            else:
                spcform = None
            if appform.is_valid() and prjform.is_valid() and spcform.is_valid():
                appform.save()
                prjform.save()
                spcform.save()
                return render(request,'permits/success.html')
            else:
                error_message = "Invalid input. Please try again."
                return render(request,'permits/my-detail.html',{
                                                    "error_message":error_message,
                                                    'appform':appform,
                                                    'prjform':prjform,
                                                    'spcform':spcform})
        else:
            appform = ApplicantForm(instance= application.applicant_info)
            prjform = ProjectForm(instance=application.project_info)
            if application.SFHA_permit:
                spcform = SFHAForm(instance=application.SFHA_permit)
            elif application.grading_permit:
                spcform = GradingForm(instance=application.grading_permit)
            elif application.franchise_permit:
                spcform = FranchiseForm(instance=application.franchise_permit)
            else:
                spcform = None
            return render(request,'permits/my_detail.html',{
            'application':application,
            'appform':appform,
            'prjform':prjform,
            'spcform':spcform,
            })
    else:
        error_message = "You are not authorized to view this page."
        return render(request,'permits/index.html',{"error_message":error_message})

def review(request):
    applications = Application.objects.order_by('date_created')
    error_message = None
    form = ReviewFilter()
    if request.method=="POST":
        form = ReviewFilter(request.POST)
        if form.is_valid():
            if 'approved' in request.POST:
                request.session['approved']=True
            else:
                request.session['approved']=False
            if 'start' in request.POST:
                request.session['start']=request.POST['start']
            if 'end' in request.POST:
                request.session['end']=request.POST['end']
            if 'type' in request.POST:
                request.session['type']=request.POST['type']
        else:
            error_message = 'Invalid input'
        #handle filtering
    if 'type' in request.session:
        if request.session['type'] == 'None':
            applications = Application.objects.order_by('date_created')
            # I don't think there's a graceful way to do this.
        else:
            applications = applications.filter(type=Permit.objects.get(name=request.session['type']))
    if 'approved' in request.session:
        applications = applications.filter(approved = request.session['approved'])
    if 'start' in request.session:
        applications = applications.filter(date_created__gte=datetime(request.session['start']))
    if 'end' in request.session:
        applications = applications.filter(date_created__lte=datetime(request.session['end']))
        # This is a problem. You can't 'clear' the filter
    p = Paginator(applications,10)
    page = request.GET.get('page')
    applications = p.get_page(page)
    return render(request,'permits/review_list.html',{
    'error_message':error_message,
    'applications':applications,
    'form':form,
    })

def review_detail(request,pk):
    # Variables needed for POST handling and normal display
    application = get_object_or_404(Application,pk=pk)
    user_department = UserDepartment.objects.get(user=request.user).department
    stock_comments = StockComment.objects.filter(department=user_department,
    permit=application.type)
    if request.method == "POST":
        # Save POST data
        CommentFormSet = modelformset_factory(ReviewComment,
        fields=('macro','comment','acknowledge','respond'),extra=10)
        approveform = ApproveForm(request.POST)
        formset = CommentFormSet(request.POST,queryset=ReviewComment.objects.none())
        # pdb.set_trace()
        if approveform.is_valid() and formset.is_valid():
            # Overwrite values in form
            formset = formset.save(commit=False)
            for form in formset:
                form.user=request.user
                form.application=application
                form.department=user_department
                form.save()
            approval = Approval(user=request.user,application=application)
            if 'conditional' in request.POST:
                approval.conditional=True
                approval.save()
            elif 'final' in request.POST:
                approval.final=True
                approval.save()
            return redirect('permits:review')
        else:
            error_message = 'Please check your submission'
            return render(request,'permits/review_detail.html',{
            'error_message':error_message,
            'application':application,
            'department':user_department,
            'required':required,
            'comments':comments,
            'stock_comments':stock_comments,
            'approveform':approveform,
            'formset':formset,
            })
    else:
        # Show the information for a specific application, including files and
        # provide the user with a comment formset
        error_message = None
        comments = ReviewComment.objects.filter(application=application).order_by('department')
        defaults = stock_comments.filter(default=True)
        # Find which departments have approved of this permit and which are needed.
        required = application.type.required_approvals.all() # queryset of Department
        required = [r.name for r in required]
        approvals = Approval.objects.filter(application=application)
        current_approvals = dict.fromkeys(required)
        for key in current_approvals:
            current_approvals[key] = ('','','','') # Template must unpack a predictable number of items
        for a in approvals:
            approved_by = a.user.username
            approved_on = str(a.date)
            conditional = a.conditional
            final = a.final
            dept = UserDepartment.objects.get(user=a.user).department.name
            current_approvals[dept]=(approved_by,approved_on,conditional,final)
        # Generate comment forms
        approveform = ApproveForm()
        # CommentFormSet = formset_factory(CommentForm,extra=10,department=user_department,permit=application.type)
        CommentFormSet = modelformset_factory(ReviewComment,
        fields=('macro','comment','acknowledge','respond'),extra=10)
        formset = CommentFormSet(initial=[{
        'comment':d.comment,
        'acknowledge':d.acknowledge,
        'respond':d.respond,}
        for d in defaults],
        queryset=ReviewComment.objects.none())
        for form in formset:
            form.fields['macro'].queryset=StockComment.objects.filter(
            department=user_department,permit=application.type)
        return render(request,'permits/review_detail.html',{
        'error_message':error_message,
        'application':application,
        'department':user_department,
        'approvals':current_approvals,
        'comments':comments,
        'stock_comments':stock_comments,
        'approveform':approveform,
        'formset':formset,
        })

@csrf_exempt
def make_payment(request):
    fee = int(request.session['fee']*100)
    application_id = request.session['application']
    application = Application.objects.get(pk=application_id)
    stripe.api_key = settings.STRIPE_PUBLIC_KEY
    pubkey = settings.STRIPE_PUBLIC_KEY
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        charge = stripe.Charge.create(
        amount=fee,
        currency='usd',
        description='Application fee',
        source=request.POST['stripeToken'],
        )
        application.paid = True
        application.save()
        paid = True
        return redirect('permits:my_applications')
    else:
        return render(request,'permits/payment.html',{
        'fee':fee,
        'key':pubkey,
        })
