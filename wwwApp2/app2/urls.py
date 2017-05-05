from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = [
	url(r'^main/', views.main, name = "main"),
	url(r'^index/', views.main, name = "main"),
	url(r'^voivodeship/(.+)/', views.voivodeship, name = "voivodeship"),
	url(r'^region/(.+)/', views.region, name = "region"),
	url(r'^borough/(.+)/', views.borough, name = "borough"),
	url(r'^vote/edit/(.+)/(.+)', views.editVote, name = "voivodeship"),
]