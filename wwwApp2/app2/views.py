# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import datetime
import json
from app2.serializers import *
from app2.models import *
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
		'tableId' : tableId,
		'leftColumnName' : leftColumnName,
		'nextUrl' : nextUrl,
		'candidates' : candidates,
		'tableResult' : tableResult,
		'chartResult' : chartResult,
		'dataForMap' : dataForMap,
		'title' : name,
		'chartData' : chartData,
		'viewName' : viewName,
		})

def main(request):
	return electionViewHelp(
		request,
		'mainPageTemplate.html',
		'main',
		'voivodeshipTable',
		'Województwo',
		'voivodeship',
		''
		)

def voivodeship(request, voivodeshipName):
	# return HttpResponse(voivodeshipName)
	return electionViewHelp(
		request,
		'voivodeshipPageTemplate.html',
		'voivodeship',
		'regionTable',
		'Okręg',
		'region',
		voivodeshipName
		)

def region(request, regionName):
	# return HttpResponse(regionName)
	return electionViewHelp(
		request,
		'regionPageTemplate.html',
		'region',
		'boroughTable',
		'Gmina',
		'borough',
		regionName
		)

def borough(request, boroughName):
	# return HttpResponse(boroughName)
	return electionViewHelp(
		request,
		'boroughPageTemplate.html',
		'borough',
		'regionTable',
		'Gmina',
		'borough',
		boroughName
		)

@login_required(login_url='/admin')
def editVote(request, borough, candidate):
	template_name = 'voteTemplate.html'
	instance = getVote(borough, candidate)
	if request.method == 'POST':
		form = VoteForm(request.POST or None, instance = instance)
		
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/app2/success/Pomyślnie zmienione głosy :)/')
	else:
		form = VoteForm(request.POST or None, instance = instance)
	return render(request, 'voteTemplate.html',
			{'form' : form, 'borough' : instance.borough.name, 'candidate' : instance.candidate.name})

	# text = '<h1>Tu będzie zmiana liczby głosów</h1>' + form
	# text += '<p>dla głosu z gminy: ' + instance.borough.name + '</p>'
	# text += '<p>dla kandydata: ' + instance.candidate.name + '</p>'
	# text += '<p>z poprzednią iloscią głosów: ' + str(instance.votes) + '</p>'
	# return HttpResponse(text)
	# if form.is_valid():
	# 	form.save()
	# 	redirect('success_view')
	return render('voteTemplate.html', {'form': form})

# New view with REST generating
def mainNew(request):
	return render(request, 'jsPageGeneratorTemplate.html', {
		'viewName' : 'mainNew',
		})

def success(request, message):
	return render(request, 'resultPage.html', {'message' : message, 'type' : 'Sukces'})


###################### API VIEWS ##################################
def candidatesApi(request):
	candidates = Candidate.objects.all()
	serializer = CandidateSerializer(candidates, many = True)
	return JsonResponse(serializer.data, safe = False)	

def BadRequestApi(text):
	return JsonResponse('Bad request: ' + text)

@csrf_exempt
def votesApi(request):
	if request.method == 'GET':
		boroughName = request.GET.get('borough', '')
		candidateName = request.GET.get('candidate', '')
		
		votes = Vote.objects.all()
		if candidateName != '':
			candidate = Candidate.objects.get(name = candidateName)
			votes = votes.filter(candidate = candidate)			
		if boroughName != '':
			boroughSet = Borough.objects.filter(name = boroughName).all()
			votes = votes.filter(borough__in = boroughSet)

		serializer = VoteSerializer(votes, many = True)
		return JsonResponse(serializer.data, safe = False)
	elif request.method == 'POST':
		#  TODO dodac tu walidacje
		boroughName = request.POST.get('borough', '')
		candidateName = request.POST.get('candidate', '')
		votes = request.POST.get('votes', '')

		if boroughName != '' and candidateName != '':
			try:
				votesInt = int(votes)
				instance = getVote(boroughName, candidateName)
				instance.votes = votesInt
				instance.save()
				serializer = VoteSerializer(instance, many = False)
				return JsonResponse(serializer.data, safe = False)	
			except ValueError:
				return JsonResponse({'ERROR' : 'votes parsing failed'}, safe = False)
		return JsonResponse({'ERROR' : 'boroughName and candidateName should be specified'}, safe = False)
	return BadRequestApi('Only GET and POST methods supported')

def userApi(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			return JsonResponse([request.user.username], safe = False)
		return JsonResponse([''], safe = False)
	return BadRequestApi('Only GET method is supported')

def voivodeshipApi(request):
	if request.method == 'GET':
		voivodeshipName = request.GET.get('voivodeship', '')
		if voivodeshipName == '':
			result = createTableResultForMain()
		else:
			result = createTableResultForVoivodeship(voivodeshipName)
		return JsonResponse(result, safe = False)
	return BadRequestApi('Only GET method is supported')

def regionApi(request):
	if request.method == 'GET':
		regionName = request.GET.get('region', '')
		if regionName == '':
			return BadRequestApi('Region should be specified')
		result = createTableResultForRegion(regionName)
		return JsonResponse(result, safe = False)
	return BadRequestApi('Only GET method is supported')

def boroughApi(request):
	if request.method == 'GET':
		boroughName = request.GET.get('borough', '')
		if boroughName == '':
			return BadRequestApi('Borough should be specified')
		borough = Borough.objects.filter(name = boroughName)
		if len(borough) == 0:
			return JsonResponse(['NOTFOUND'], safe = False)
		result = createTableResultForBorough(boroughName)
		return JsonResponse(result, safe = False)
	return BadRequestApi('Only GET method is supported')

def boroughSearchApi(request):
	if request.method == 'GET':
		boroughName = request.GET.get('borough', '')
		return JsonResponse(searchBorough(boroughName), safe = False)
	return BadRequestApi('Only GET method is supported')

