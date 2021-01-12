from django.shortcuts import render


def send_welcome_email(email,password,phone_number,username):
    try:
        context = {'email':email,'password':password,'phone_number':phone_number,'username':username}
        text = f"Hello {username} Your {email} And {phone_number}"
        return True
    except Exception as e:
        print(e)
        return False

def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request,'login.html')
	else:
		forms = RegistrationForm()
		return render(request,'registration.html',{'form':forms})



# Create your views here.
