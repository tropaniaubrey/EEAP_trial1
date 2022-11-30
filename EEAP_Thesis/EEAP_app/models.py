from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class accounts(AbstractUser):
    idnumber = models.CharField(max_length = 30,primary_key = True, unique = True)
    birthday = models.CharField(max_length = 30)
    contactnumber = models.CharField(max_length = 11)
    usertype = models.CharField(max_length = 30)
    course = models.CharField(max_length = 100)
    year = models.CharField(max_length = 30)
    student_pic = models.ImageField(upload_to = "student_pic/")
    student_qr = models.ImageField(upload_to = "student_qr/")



class registered_vehicles(models.Model):
    vehicleid = models.CharField(max_length = 30,primary_key = True, unique = True)
    idnumber = models.CharField(max_length = 30)
    platenumber = models.CharField(max_length = 10)
    vehiclemodel = models.CharField(max_length = 12)
    imageF = models.ImageField(upload_to = "imageF/")
    imageL = models.ImageField(upload_to = "imageL/")
    imageR = models.ImageField(upload_to = "imageR/")
    imageB = models.ImageField(upload_to = "imageB/")
    ORCR = models.ImageField(upload_to = "ORCR/")
    status = models.CharField(max_length = 20)
    qrcode = models.ImageField(upload_to = "qrcode/")
    approved_by = models.CharField(max_length = 50)
    date_approved = models.CharField(max_length = 30)

class log_record(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    idnumber = models.CharField(max_length = 30)
    date = models.CharField(max_length = 30)
    timein = models.CharField(max_length = 30)
    timeout = models.CharField(max_length = 30)
    vehicleid = models.CharField(max_length = 30)
