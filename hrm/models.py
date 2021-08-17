from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Volunteer(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField("First Name", null=True, blank=True, max_length=30)
    last_name= models.CharField("Last Name", null=True, blank=True, max_length=30)
    birth_date = models.DateField("Date of Birth", blank=True, null=True)
    birth_place = models.CharField("Birth Place", blank=True, null=True, max_length=100)
    adress = models.CharField("Adress", blank=True, null=True, max_length=200)
    country = models.CharField("Country", blank=True, null=True, max_length=30)
    county = models.CharField("County", blank=True, null=True, max_length=30)
    parents = models.CharField("Parents", blank=True, null=True, max_length=50)
    domiciliu = models.CharField("Domiciliu", blank=True, null=True, max_length=100)
    cnp_id = models.DecimalField("CNP ID", decimal_places=0, blank=True, null=True, max_digits=13)
    seria_id = models.CharField("Serie ID", max_length=2, blank=True, null=True)
    nr_serie_id = models.DecimalField("Number Serie ID", blank=True, null=True,max_digits=6, decimal_places=0)
    emitere_id = models.CharField("Emitere Buletin", blank=True, null=True, max_length=30)
    id_date = models.DateField("Date ID", blank=True, null=True)
    telephone_number = PhoneNumberField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, default="files/default-user-image.png", blank=True)
    # departments = models.ForeignKey("Department", on_delete=models.CASCADE, blank=True,  null=True) 

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.user.username
    
class Department(models.Model):
    hod = models.ForeignKey(Volunteer, verbose_name="Head Of Department", on_delete=models.CASCADE, null="Not Added", blank=True) # HOD = Head Of Department
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name

class Organizer(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
class Event(models.Model):
    title = models.CharField(max_length=30)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null="Not Added", blank=True)
    volunteers = models.ManyToManyField(Volunteer)
    def __str__(self):
        return self.title

class LegalTemplate(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null="Not Added")
    file = models.FileField(upload_to="important/contract_templates/", null=True, blank=True)
    TEMPLATE_TYPE = [
        ('Contract Voluntariat', 'Contract Voluntariat'),
        ('GDPR', 'GDPR'),
        ('Acord Tutore', 'Acord Tutore'),
    ]
    type = models.CharField(choices=TEMPLATE_TYPE, max_length=30)
    def __str__(self):
        return self.event.title + " - " + self.type
class Contract(models.Model):
    volunteer = models.ForeignKey(Volunteer,on_delete=models.CASCADE, null="Not Added")
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null="Not Added")
    file = models.FileField(upload_to="contracte/", null=True, blank=True)
    def __str__(self):
        if self.volunteer.first_name and self.volunteer.last_name:
            return self.event.title + " - " + self.volunteer.first_name + " " + self.volunteer.last_name
        else:
            return self.event.title + " - " + self.volunteer.user.username