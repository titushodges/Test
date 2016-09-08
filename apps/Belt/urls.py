from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^register$', views.register),
	url(r'^friends$', views.home),
	url(r'^user/(?P<user_id>\d+)$', views.user),
	url(r'^add/(?P<item_id>\d+)$', views.add),
	url(r'^delete/(?P<item_id>\d+)$', views.delete),
	url(r'^logout$', views.logout),
]