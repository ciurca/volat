from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Volunteer)
admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(Contract)

