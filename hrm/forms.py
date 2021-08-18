from crispy_forms.layout import Field, HTML, Layout, Submit
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
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'register-form'

        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            FloatingField('username', placeholder="Username"),
            FloatingField('email', placeholder="email"),
            FloatingField('password1', placeholder="Password"),
            FloatingField('password2', placeholder="Password"),
            HTML("""
           <div class="form-text">
                Already have an account? <a href="{% url 'login'%}">Login</a>
           </div> 
        """),
        )
        self.helper.add_input(Submit('submit', 'Register', css_class='btn btn-primary'))

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
            'id_date': DateInput(),

        }