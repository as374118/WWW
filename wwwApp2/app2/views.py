# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import datetime
from utils import *

# help function
def electionViewHelp(request, template, viewName, tableId, leftColumnName, nextUrl, name):
	candidates = createCandidatesList()
	tableResult = createTableResult(viewName, name)
	chartResult = createChartResult(viewName, name)
	dataForMap = getVoivodeshipsForMap()
	chartData = getChartData()
	return render(request, template,
		{
		"tableId" : tableId,
		"leftColumnName" : leftColumnName,
		"nextUrl" : nextUrl,
		"candidates" : candidates,
		"tableResult" : tableResult,
		"chartResult" : chartResult,
		"dataForMap" : dataForMap,
		"title" : name,
		"chartData" : chartData,
		"viewName" : viewName,
		})

def main(request):
	return electionViewHelp(
		request,
		"mainPageTemplate.html",
		"main",
		"voivodeshipTable",
		"Województwo",
		"voivodeship",
		""
		)

def voivodeship(request, voivodeshipName):
	# return HttpResponse(voivodeshipName)
	return electionViewHelp(
		request,
		"voivodeshipPageTemplate.html",
		"voivodeship",
		"regionTable",
		"Okręg",
		"region",
		voivodeshipName
		)

def region(request, regionName):
	# return HttpResponse(regionName)
	return electionViewHelp(
		request,
		"regionPageTemplate.html",
		"region",
		"boroughTable",
		"Gmina",
		"borough",
		regionName
		)

def borough(request, boroughName):
	# return HttpResponse(boroughName)
	return electionViewHelp(
		request,
		"boroughPageTemplate.html",
		"borough",
		"regionTable",
		"Gmina",
		"borough",
		boroughName
		)

@login_required(login_url='/admin')
def editVote(request, borough, candidate):
	template_name = 'voteTemplate.html'
	instance = getVote(borough, candidate)
	text = "<h1>Tu będzie zmiana liczby głosów</h1>"
	text += "<p>dla głosu z gminy: " + instance.borough.name + "</p>"
	text += "<p>dla kandydata: " + instance.candidate.name + "</p>"
	text += "<p>z poprzednią iloscią głosów: " + str(instance.votes) + "</p>"
	return HttpResponse(text)
	form = VoteForm(request.POST or None, instance = instance)
	if form.is_valid():
		form.save()
		redirect('success_view')
	return render('voteTemplate.html', {'form': form.as_p})


def success_view(request):
	return HttpResponse('<h1>Sukces!!!</h1>')
