from django.shortcuts import render,redirect
from .models import Users,OTP

import random
import string
import datetime
import time
import hashlib
import os
from django.db.models import F

def send_welcome_email(email,password,phone_number,username):
    try:
        #context = {'email':email,'password':password,'phone_number':phone_number,'username':username}
        text = f"Hello {username} Your {email} And {phone_number}"
        print(text)    ## We can use MIMEPart,EmailMultiAlternatives ,SMTP etc to send email but as mentioned i have just printed it on terminal
        return True
    except Exception as e:
        print(e)
        return False

def register(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		emai1 = request.POST['email1']
		email2 = request.POST['email2']
		phone_number = request.POST['phone_number']
		password = request.POST['password']
		
		salt = os.urandom(32)
		result = hashlib.sha256(password.encode()) 
		user = Users(username = username,email = email,phone_number = phone_number,password = result.hexdigest())
		user.save()
		
		print(send_welcome_email(email,password,phone_number,username))

		return render(request,'login.html')
	else:
		return render(request,'registration.html')


def login(request):
	if request.method == "POST":
		phone_number = request.POST["phone_number"]
		otp_number = "".join(random.choices(string.digits,k=6))
		user_check = Users.objects.filter(phone_number = phone_number)
		user_values = user_check.values()
		if not user_check.exists():
			return redirect('registration')
		if user_values[0]['time_track'] > time.time():
			return render(request,'login.html',{"message":"Please Try again after 5 min"})
		else: 
			user_check.update(is_block = False)
		if OTP.objects.filter(phone_number = phone_number).exists():
			return render(request,'otp.html',{'cell_number':phone_number})
		otp = OTP(otp = otp_number,phone_number = phone_number)
		otp.save()
		print(otp_number,'otpp')
		return render(request,'otp.html',{"cell_number":phone_number})
	else:
		return render(request,'login.html')

def otp(request):
	if request.method == "POST":
		otp = request.POST["otp"]
		phone_numbers = request.POST["phone_number"]
		print(phone_numbers)
		user_check = OTP.objects.filter(phone_number = phone_numbers)
		user_value = user_check.values()
		
		if not user_check.exists():
			return redirect('registration')
		
		user = Users.objects.filter(phone_number = user_value[0]['phone_number']).values()
		
		if user_value[0]['otp'] == otp:
			user_check.delete()
			user.update(last_login = datetime.datetime.now()) 
			return render(request,'home.html',{'username':user[0]["username"]})
		else:
			user_check.update(otp_counter = F('otp_counter')+1)
			if user_value[0]['otp_counter'] > 3:
				user_check.delete()
				user.update(is_block = True,time_track = time.time()+300) 
				return render(request,'login.html',{"message":"Please Try Again After 5 min"})
			else:

				return render(request,'otp.html',{"cell_number":phone_numbers})
			
	else:
		return render(request,'otp.html')








# Create your views here.
