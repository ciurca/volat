import os
import time as t
from datetime import datetime

from django.core.mail import send_mail, BadHeaderError
from volat.settings import BASE_DIR, DEBUG, DEFAULT_FROM_EMAIL
from django import contrib
from django.core.files.base import File
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

from django.contrib.auth.forms import PasswordResetForm, UserCreationForm # for the register page
from django.contrib.auth import authenticate, login, logout # for the authentification part
from django.contrib.auth.models import Group
from django.contrib import messages #send success/error messages

from django.contrib.auth.decorators import login_required # requires login
from django.utils.decorators import method_decorator
from django.utils.html import format_html

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from docxtpl import DocxTemplate
import zipfile
from io import BytesIO, StringIO
# Create your views here.
from .models import *
from .forms import CreateUserForm, VolunteerForm
from .decorators import * 

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

@unauthenticated_user
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					if DEBUG == True:
						mail_domain = '127.0.0.1:8000'
					else:
						mail_domain = 'volat.xyz'
					c = {
					"email":user.email,
					'domain':mail_domain,
					'site_name': 'Volat',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox. Please check your SPAM folder.')
					return redirect ("home")
			else:
				messages.error(request, 'An invalid email has been entered.')	
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})