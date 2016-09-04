from django.shortcuts import render, HttpResponse, redirect
from . import models
import bcrypt, re
from django.contrib import messages
# Create your views here.
def index(request):
	request.session['logged_in'] = False
	return render(request, 'Belt/index.html')

