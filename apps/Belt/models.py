from __future__ import unicode_literals

from django.db import models

# Create your models here.
class users(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255, unique = True)
	password = models.CharField(max_length=255)
	dob = models.DateTimeField(auto_now_add=False, auto_now=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class friends(models.Model):
	user_id = models.ForeignKey(users, null=True, blank=True)
	friend_id = models.ForeignKey(users, related_name= 'friend_id', null=True, blank=True)
	description = models.TextField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
