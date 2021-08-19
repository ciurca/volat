from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from hrm.models import *
from django.shortcuts import get_object_or_404, redirect, render
from docxtpl import DocxTemplate
import os
from volat.settings import BASE_DIR, DEBUG, DEFAULT_FROM_EMAIL
import zipfile
from io import BytesIO, StringIO
from django.urls import reverse
import time as t
from datetime import datetime
from django.utils.html import format_html
from django.core.files.base import File
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from tempfile import TemporaryDirectory
from pathlib import Path
import secrets
def _generateContract(volunteer, template_path, savelocation_path, event, request):
	if volunteer.first_name and volunteer.last_name:
				firstName = volunteer.first_name
				lastName = volunteer.last_name
				upperFullName = f"{volunteer.last_name} {volunteer.first_name}"
				templatedoc = DocxTemplate(template_path)
				fields_list = [
					volunteer.first_name,
					volunteer.last_name,
					str(volunteer.birth_date),
					volunteer.birth_place,
					volunteer.adress,
					volunteer.country,
					volunteer.county,
					volunteer.parents,
					volunteer.domiciliu,
					str(volunteer.cnp_id),
					volunteer.seria_id,
					str(volunteer.nr_serie_id),
					volunteer.emitere_id,
					str(volunteer.id_date),
					str(volunteer.telephone_number),
				]
				context = { 
					'first_name' : volunteer.first_name,
					'last_name' : volunteer.last_name,
					'birth_date' : str(volunteer.birth_date),
					'birth_place': volunteer.birth_place,
					'adress': volunteer.adress,
					'country': volunteer.country,
					'county': volunteer.county,
					'parents': volunteer.parents,
					'domiciliu' : volunteer.domiciliu,
					'cnp_id' : str(volunteer.cnp_id),
					'seria_id': volunteer.seria_id,
					'nr_serie_id': str(volunteer.nr_serie_id),
					'emitere_id': volunteer.emitere_id,
					'id_date': str(volunteer.id_date),
					'telephone_number': str(volunteer.telephone_number),
					'full_name_caps': upperFullName.upper(),
				}
				for field in fields_list:
					if field is None:
						message= format_html("Go into&nbsp;<a href='{}'>personal information</a>&nbsp;and complete your profile.", reverse('account-personal_information'))
						messages.error(request, message)
						return HttpResponseRedirect(reverse('event', args=(event.id,)))
				templatedoc.render(context)
				save_location = os.path.join(BASE_DIR, savelocation_path)
				templatedoc.save(save_location)

				t.sleep(3)
				with open(save_location, 'rb') as file_handle:
					new_contract = Contract.objects.create(
						volunteer=volunteer,
						event=event,
					)
					new_contract.file.save(f"Contract-{firstName}{lastName}{secrets.token_hex(3)}.docx", File(file_handle))
				os.remove(save_location)
				messages.success(request, 'Contract created succesfully!')
				return HttpResponseRedirect(reverse('event', args=(event.id,)))
	else:
		message= format_html("Go into&nbsp;<a href='{}'>personal information</a>&nbsp;and complete your profile.", reverse('account-personal_information'))
		messages.error(request, message)
		return HttpResponseRedirect(reverse('event', args=(event.id,)))

def generateContract(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	volunteer = request.user.volunteer
	contracts = Contract.objects.all().filter(volunteer=volunteer.id)
	legal_templates = LegalTemplate.objects.all().filter(event=event.id)
	if legal_templates is None:
		messages.warning(request, "There are no template associated with this event. Please talk to the event organizer.")
		return HttpResponseRedirect(reverse('event', args=(event.id,)))
	contract_template = []
	for template in legal_templates:
		if template.type == "Contract Voluntariat":
			contract_template.append(template)
	# if contract_template[0] is None:
	# 	messages.warning(request, "There are no template associated with this event. Please talk to the event organizer.")
	# 	return HttpResponseRedirect(reverse('event', args=(event.id,)))
	if bool(contract_template):
		template_path = contract_template[0].file
		savelocation_path = f"static/files/contracte/contract{secrets.token_hex(3)}.docx"
		contract_list = []
		if bool(contracts): 
			for contract in contracts:
					if contract.event == event:
						contract_list.append(contract)
			if bool(contract_list):
				messages.warning(request, "There is already a contract for this event.")
			else:
				return _generateContract(volunteer, template_path, savelocation_path, event, request)

		else:
			return _generateContract(volunteer, template_path, savelocation_path, event, request)
	else:
		messages.warning(request, "There are no templates associated with this event. Please talk to the event organizer.")
		return HttpResponseRedirect(reverse('event', args=(event.id,)))
	return HttpResponseRedirect(reverse('event', args=(event.id,)))

def _delete_contract(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	volunteer = request.user.volunteer
	vol_contracts = Contract.objects.all().filter(volunteer=volunteer.id)
	contracts = vol_contracts.filter(event=event.id)
	for contract in contracts:
		contract.delete()
	return HttpResponseRedirect(reverse('event', args=(event.id,)))

def exportContracts(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	contracts = Contract.objects.all().filter(event=event.id)
	contract_files = []  # CHANGED
	for contract in contracts:
		if contract.file:
			contract_files.append(contract.file)  # CHANGED
		else:
			messages.error(request, "Some contracts don't have any files associated with them.")
			return HttpResponseRedirect(reverse('event', args=(event.id,)))
		
	zip_subdir= f"Contracts for {event.title}"
	zip_filename = f"Contracts for {event.title}.zip"
	s = BytesIO()
	zf = zipfile.ZipFile(s, "w")
	for contract_file in contract_files:  # CHANGED
		# Calculate path for file in zip
		fdir, fname = os.path.split(contract_file.name)  # CHANGED
		zip_path = os.path.join(zip_subdir, fname)

		# Add file, at correct path
		with zf.open(zip_path, 'w') as dst:
			for chunk in contract_file.chunks():
				dst.write(chunk)
	zf.close()

	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp