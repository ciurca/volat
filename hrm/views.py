import os
import time as t
from datetime import datetime
from volat.settings import BASE_DIR
from django import contrib
from django.core.files.base import File
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

from django.contrib.auth.forms import UserCreationForm # for the register page
from django.contrib.auth import authenticate, login, logout # for the authentification part
from django.contrib.auth.models import Group
from django.contrib import messages #send success/error messages

from django.contrib.auth.decorators import login_required # requires login
from django.utils.decorators import method_decorator
from django.utils.html import format_html

from docxtpl import DocxTemplate
# Create your views here.
from .models import *
from .forms import CreateUserForm, VolunteerForm
from .decorators import * 
import volat

@login_required(login_url='login')
def home(request):
    total_volunteers = Volunteer.objects.all().count() 
    total_events = Event.objects.all().count() 
    total_organizers = Organizer.objects.all().count() 
    events = Event.objects.all()
    context= {
        'total_volunteers':total_volunteers,
        'total_events':total_events,
        'total_organizers':total_organizers,
        'events':events,
        }
    return render(request, 'hrm/dashboard.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='volunteer')
            user.groups.add(group)
            Volunteer.objects.create(
                user=user,
                email=email,
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'hrm/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect.')
    context = {}
    return render(request, 'hrm/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def userPage(request):

    context = {}
    return render(request, 'hrm/user.html', context)

@login_required(login_url='login')
def accountSettings(request):
    volunteer = request.user.volunteer
    form = VolunteerForm(instance=volunteer)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'hrm/account_settings.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EventView(generic.DetailView):
    model = Event
    template_name = "hrm/event.html"
    def get_context_data(self, **kwargs):
         context = super(EventView, self).get_context_data(**kwargs)
         self.volunteer = self.request.user.volunteer
         try:
            context['contract_list'] = Contract.objects.all().filter(volunteer=self.volunteer.id)
         except Contract.DoesNotExist:
            context['contract_list'] = None
         return context

def generateContract(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    volunteer = request.user.volunteer
    contracts = Contract.objects.all().filter(volunteer=volunteer.id)
    template_path = "static/files/important/contract_templates/example.docx"
    savelocation_path = "static/files/contracte/test.docx"
    contract_list = []
    if bool(contracts): 
        for contract in contracts:
                if contract.event == event:
                    contract_list.append(contract)
        if bool(contract_list):
            print(contract_list)
            messages.warning(request, "There is already a contract for this event.")
        else:
            if volunteer.first_name and volunteer.last_name:
                print("no contract for this event")
                firstName = volunteer.first_name
                lastName = volunteer.last_name
                birthDay = volunteer.birth_date
                templatedoc = DocxTemplate(os.path.join(BASE_DIR, template_path))
                context = { 
                    'FirstName' : firstName,
                    'LastName' : lastName,
                    'Birthday' : str(birthDay),
                    'Date' : '{:%d-%b-%Y}'.format(datetime.today()),
                }
                templatedoc.render(context)
                save_location = os.path.join(BASE_DIR, savelocation_path)
                templatedoc.save(save_location)
                t.sleep(3)
                f = open(save_location, 'rb')
                new_contract = Contract.objects.create(
                    volunteer=volunteer,
                    event=event,
                )
                new_contract.file.save(f"Contract-{firstName}{lastName}.docx", File(f))
                messages.success(request, 'Contract created succesfully!')
                return HttpResponseRedirect(reverse('event', args=(event.id,)))
            else:
                messages.warning(request, "Go into settings and complete your profile.")
                return HttpResponseRedirect(reverse('event', args=(event.id,)))

    else:
        if volunteer.first_name and volunteer.last_name:
            firstName = volunteer.first_name
            lastName = volunteer.last_name
            birthDay = volunteer.birth_date
            templatedoc = DocxTemplate(os.path.join(BASE_DIR, template_path))
            context = { 
                'FirstName' : firstName,
                'LastName' : lastName,
                'Birthday' : str(birthDay),
                'Date' : '{:%d-%b-%Y}'.format(datetime.today()),
            }
            templatedoc.render(context)
            save_location = os.path.join(BASE_DIR, savelocation_path)
            templatedoc.save(save_location)
            t.sleep(3)
            f = open(save_location, 'rb')
            new_contract = Contract.objects.create(
                volunteer=volunteer,
                event=event,
            )
            new_contract.file.save(f"Contract-{firstName}{lastName}.docx", File(f))
            messages.success(request, 'Contract created succesfully!')
            return HttpResponseRedirect(reverse('event', args=(event.id,)))
        else:
            message= format_html("Go into&nbsp;<a href='{}'>account settings</a>&nbsp;and complete your profile.", reverse('account-settings'))
            messages.error(request, message)
            return HttpResponseRedirect(reverse('event', args=(event.id,)))
    return HttpResponseRedirect(reverse('event', args=(event.id,)))