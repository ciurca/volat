from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from hrm.models import *
from django.shortcuts import get_object_or_404
from docxtpl import DocxTemplate
import os
from volat.settings import BASE_DIR
import zipfile
from io import BytesIO, StringIO
from django.urls import reverse
import time as t
from datetime import datetime
from django.utils.html import format_html
from django.core.files.base import File

def _generateContract(volunteer, template_path, savelocation_path, event, request):
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
				with open(save_location, 'rb') as file_handle:
					new_contract = Contract.objects.create(
						volunteer=volunteer,
						event=event,
					)
					new_contract.file.save(f"Contract-{firstName}{lastName}.docx", File(file_handle))
				messages.success(request, 'Contract created succesfully!')
				return HttpResponseRedirect(reverse('event', args=(event.id,)))
	else:
		message= format_html("Go into&nbsp;<a href='{}'>account settings</a>&nbsp;and complete your profile.", reverse('account-settings'))
		messages.error(request, message)
		return HttpResponseRedirect(reverse('event', args=(event.id,)))

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
			return _generateContract(volunteer, template_path, savelocation_path, event, request)

	else:
		return _generateContract(volunteer, template_path, savelocation_path, event, request)
	return HttpResponseRedirect(reverse('event', args=(event.id,)))

def exportContracts(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	contracts = Contract.objects.all().filter(event=event.id)
	filenames = []
	for contract in contracts:
		filenames.append(contract.file.path)
	zip_subdir= f"Contracts for {event.title}"
	zip_filename = f"Contracts for {event.title}"
	s = BytesIO()
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		# Calculate path for file in zip
		fdir, fname = os.path.split(fpath)
		zip_path = os.path.join(zip_subdir, fname)

		# Add file, at correct path
		zf.write(fpath, zip_path)
	zf.close()

	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp