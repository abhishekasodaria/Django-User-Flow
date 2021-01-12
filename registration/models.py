from django.db import models



class Users(models.Model):
	id = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 255,null = True,blank = True)
    email = models.EmailField(max_length = 255,null = True,blank = True,unique = True)
    email2 = models.EmailField(max_length = 255,null = True,blank = True)
    email3 = models.EmailField(max_length = 255,null = True,blank = True)
    phone_number = models.CharField(max_length = 14,unique = True,null = True,blank = True)
    password = models.CharField(max_length = 255)

class OTP(models.Model):
	phone_number = models.CharField(max_length = 14,unique = True,null = True,blank = True)
	otp = models.CharField(max_length = 255,null = True,blank = True)
	# Create your models here.
	