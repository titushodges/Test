from django.shortcuts import render, HttpResponse, redirect
from .models import users, friends
import bcrypt, re, requests
from django.db.models import Count
from django.contrib import messages
# Create your views here.
def index(request):
	request.session['logged_in'] = False
	return render(request, 'Belt/index.html')

def login(request):
	email = request.POST['email']
	passw = request.POST['password'].encode()
	user = users.objects.all().filter(email= email)
	if not user:
		messages.warning(request,"Invalid email")
		return redirect('/')
	else:
		if bcrypt.hashpw(passw, user[0].password.encode()) == user[0].password:
			request.session['logged_in'] = True
			request.session['user_id'] = request.POST['email']
			return redirect('/friends')
		else:
			messages.warning(request,"Incorrect password!")
			return redirect('/')
	

def register(request):
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	_digits = re.compile('\d')
	error = 0
	def contains_digits(d):
		return bool(_digits.search(d))
	if len(request.POST['name']) < 2:
		messages.warning(request,"Name must have at least 2 characters!")
		error = 1
	elif contains_digits(request.POST['name']):
		messages.warning(request,"Name may only contain letters")
		error = 1
	else:
		pass

	if len(request.POST['alias']) < 2:
		messages.warning(request,"Alias must have at least 2 characters!")
		error = 1
	else:
		pass

	try:
		validate_email(request.POST['email'])
		valid_email = True
	except ValidationError:
		valid_email = False
	if valid_email != True:
		messages.warning(request, 'Email is not valid')
		error = 1
	elif users.objects.filter(email=request.POST['email']).exists():
		messages.warning(request,"Email already exists")
		error = 1
	else:
		pass

	if len(request.POST['password']) < 8:
		messages.warning(request,"Password must be at least 8 characters!")
		error = 1
	else:
		pass

	if request.POST['confirm_password'] != request.POST['password']:
		messages.warning(request,"Your passwords do not match!")
		error = 1
	else:
		pass
	if error == 1:
		return redirect('/')
	else:
		password = request.POST['password'].encode()
		pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
		first_name1 = request.POST['name']
		last_name1 = request.POST['alias']
		email1 = request.POST['email']
		bday = request.POST['bday']
		users.objects.create(name=first_name1, alias=last_name1, email=email1, password=pw_hash,dob=bday)
		request.session['logged_in'] = True
		request.session['user_id'] = request.POST['email']
		return redirect('/friends')

def home(request):
	if request.session['logged_in'] != True:
		messages.warning(request,"You are not logged in!")
		return redirect('/')
	else:
		use = users.objects.all().filter(email=request.session['user_id'])
		users_id = use[0]
		userlist = friends.objects.all().filter(user_id=users_id).values_list('friend_id', flat=True)
		context = {
			'user' : users.objects.all().filter(email=request.session['user_id']),
			'users' : users.objects.all().exclude(email=request.session['user_id']).exclude(pk__in=userlist),
			'yourfriends' : friends.objects.all().filter(user_id=users_id).prefetch_related('user_id').prefetch_related('friend_id'),
		}
		return render(request, 'Belt/home.html', context)

def user(request, user_id):
	if request.session['logged_in'] != True:
		messages.warning(request,"You are not logged in!")
		return redirect('/')
	else:
		context = {
			'user' : users.objects.all().filter(id=user_id),
		}
		return render(request, 'Belt/user.html', context)

def logout(request):
	request.session.flush()
	return redirect('/')

def add(request, item_id):
	if request.session['logged_in'] != True:
		messages.warning(request,"You are not logged in!")
		return redirect('/')
	else:
		use = users.objects.all().filter(email=request.session['user_id'])
		users_id = use[0]
		friend = users.objects.all().filter(id=item_id)
		fri = friend[0]
		friends.objects.create(user_id=users_id,friend_id=fri)
		return redirect('/friends')

def delete(request, item_id):
	if request.session['logged_in'] != True:
		messages.warning(request,"You are not logged in!")
		return redirect('/')
	else:
		friends.objects.all().filter(id=item_id).delete()
		return redirect('/friends')