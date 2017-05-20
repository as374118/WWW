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
	url(r'^success/(.+)/', views.success, name = "success"),
	url(r'^candidates_api/', views.candidatesApi, name = "candidates_api"),
	url(r'^votes_api/', views.votesApi, name = "votes_api"),
	url(r'^voivodeship_api/', views.voivodeshipApi, name = "voivodeship_api"),
	url(r'^region_api/', views.regionApi, name = "region_api"),
	url(r'^borough_api/', views.boroughApi, name = "borough_api"),
	url(r'^main_new/', views.mainNew, name = "main_new"),
	url(r'^borough_search_api/', views.boroughSearchApi, name = "borough_search_api"),
	url(r'^user_api/', views.userApi, name = "user_api"),
]