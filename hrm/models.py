from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Volunteer(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField("Prenume", null=True, blank=True, max_length=30)
    last_name= models.CharField("Nume", null=True, blank=True, max_length=30)
    birth_date = models.DateField("Date of Birth", blank=True, null=True)
    residence = models.CharField("Current place of residence", blank=True, null=True, max_length=300)
    profile_pic = models.ImageField(null=True, default="files/default-user-image.png", blank=True)
    OCCUPATION_CHOICES = (
        ('Highschool Student', 'Highschool Student'),
        ('University Student', 'University Student'),
        ('Employee', 'Employee'),
    )
    LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('Romanian', 'Romanian'),
        ('Hungarian', 'Hungarian'),
        ('German', 'German'),
        ('French', 'French'),
    )
    SHIRTSIZES_CHOICES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    )
    occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, blank=True, null=True)
    languages_spoken = MultiSelectField(choices = LANGUAGE_CHOICES, blank=True,  null="Not Added")
    email = models.EmailField(max_length=200,blank=True,  null=True)
    phone_number = PhoneNumberField(null=True, blank=True, )
    fb_link = models.URLField(max_length=300, null=True, blank=True)
    departments = models.ForeignKey("Department", on_delete=models.CASCADE, blank=True,  null=True) 
    # contract = models.FileField(upload_to="contracte/", null=True, blank=True)

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

class Contract(models.Model):
    volunteer = models.ForeignKey(Volunteer,on_delete=models.CASCADE, null="Not Added")
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null="Not Added")
    file = models.FileField(upload_to="contracte/", null=True, blank=True)
    def __str__(self):
        if self.volunteer.first_name and self.volunteer.last_name:
            return self.event.title + " - " + self.volunteer.first_name + " " + self.volunteer.last_name
        else:
            return self.event.title + " - " + self.volunteer.user.username