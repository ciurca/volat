from crispy_forms.layout import Layout
from django.db.models import fields
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
class DateInput(forms.DateInput):
    input_type= 'date'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class VolunteerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VolunteerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag=False
    class Meta:
        model = Volunteer
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'birth_date': DateInput(),
        }