from django.shortcuts import render, HttpResponse, redirect
from . import models
import bcrypt, re
from django.contrib import messages
# Create your views here.
def index(request):
	request.session['logged_in'] = False
	return render(request, 'Belt/index.html')

def login(request):
	email = request.POST['email']
	password = request.POST['password'].encode()
	user = models.users.objects.all().filter(email= email)
	hashed = bcrypt.hashpw(password, bcrypt.gensalt())
	if not user:
		messages.warning(request,"Invalid email")
		return redirect('/login/')
	else:
		if bcrypt.hashpw(password, hashed) == hashed:
			request.session['logged_in'] = True
			request.session['user_id'] = request.POST['email']
			return redirect("/login/success")
		else:
			messages.warning(request,"Incorrect password!")
			return redirect('/login/')

def register(request):
	return render(request, 'Day_7_Login/register.html')

def submit(request):
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	_digits = re.compile('\d')
	def contains_digits(d):
		return bool(_digits.search(d))
	if len(request.POST['first_name']) < 2:
		messages.warning(request,"First name must have at least 2 characters!")
		return redirect('/login/register')
	elif contains_digits(request.POST['first_name']):
		messages.warning(request,"First name may only contain letters")
		return redirect('/login/register')
	else:
		pass

	if len(request.POST['last_name']) < 2:
		messages.warning(request,"Last name must have at least 2 characters!")
		return redirect('/login/register')
	elif contains_digits(request.POST['last_name']):
		messages.warning(request,"Last name may only contain letters")
		return redirect('/login/register')
	else:
		pass

	try:
		validate_email(request.POST['email'])
		valid_email = True
	except ValidationError:
		valid_email = False
	if valid_email != True:
		messages.warning(request, 'Email is not valid')
		return redirect('/login/register')
	elif models.users.objects.filter(email=request.POST['email']).exists():
		messages.warning(request,"Email already exists")
		return redirect('/login/register')
	else:
		pass

	if len(request.POST['password']) < 8:
		messages.warning(request,"Password must be at least 8 characters!")
		return redirect('/login/register')
	else:
		pass

	if request.POST['confirm_password'] != request.POST['password']:
		messages.warning(request,"Your passwords do not match!")
		return redirect('/login/register')
	else:
		password = request.POST['password'].encode()
		pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
		first_name1 = request.POST['first_name']
		last_name1 = request.POST['last_name']
		email1 = request.POST['email']
		models.users.objects.create(first_name=first_name1, last_name=last_name1, email=email1, password=pw_hash)
		request.session['logged_in'] = True
		request.session['user_id'] = request.POST['email']
		return redirect('/login/success')

def success(request):
	if request.session['logged_in'] != True:
		messages.warning(request,"You are not logged in!")
		return redirect('/login/')
	else:
		data = models.users.objects.all().filter(email=request.session['user_id'])
		context = {"data":data}
		return render(request, 'Day_7_Login/success.html', context)

def logout(request):
	request.session.flush()
	return redirect('/login/')

