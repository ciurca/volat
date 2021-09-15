from os import name
from crispy_forms.layout import ButtonHolder, Div, Field, HTML, Layout, Reset, Submit
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
		self.helper.layout = Layout(
			FloatingField('first_name'),
			FloatingField('last_name'),
			FloatingField('birth_date'),
			FloatingField('birth_place'),
			FloatingField('adress'),
			FloatingField('county'),
			FloatingField('country'),
			FloatingField('parents'),
			FloatingField('domiciliu'),
			FloatingField('cnp_id'),
			FloatingField('seria_id'),
			FloatingField('nr_serie_id'),
			FloatingField('emitere_id'),
			FloatingField('id_date'),
			FloatingField('telephone_number'),
			ButtonHolder(
				Submit('submit', 'Submit', css_class='button white')
			)

		)
		self.fields['first_name'].help_text = "Exemplu: Marinel"
		self.fields['last_name'].help_text = "Exemplu: Moldovan"
		self.fields['birth_place'].help_text = "Localitate în care te-ai născut. De exemplu: Târgu Mureș"
		self.fields['adress'].help_text = "Adresa ta. Exemplu: Str. Trezită, nr 13B"
		self.fields['parents'].help_text = "Prenumele părinților. De exemplu: Ion și Ana"
		self.fields['domiciliu'].help_text = "Localitatea de domiciliu. De exemplu: Târgu-Mureș"
		self.fields['emitere_id'].help_text = "De exemplu: SPCLEP Tg. Mureș"
		self.fields['seria_id'].help_text = "De exemplu: MS"
		self.fields['nr_serie_id'].help_text = "De exemplu: 183916"
		self.fields['id_date'].help_text = "Data la care a fost emis buletinul."
		self.fields['telephone_number'].help_text = "Numărul tău de telefon. Te rog folosește prefixul +40. De exemplu: +40741221112"
	class Meta:
		model = Volunteer
		fields = '__all__'
		exclude = ['user']
		widgets = {
			'birth_date': DateInput(),
			'id_date': DateInput(),

		}