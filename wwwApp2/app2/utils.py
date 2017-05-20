# -*- coding: utf-8 -*-
from django.db.models import Sum
# from django.db.models import 
from models import *
from random import randint

#  UTILS

def createCandidatesList():
	res = []
	for c in Candidate.objects.all():
		res.append(c.name)
	return res

def createColorsList(n):
	res = []
	for i in range(n):
		res.append('#' + str('%06X' % (0x0000FF - i * 0x00015)))
	return res

def getVote(borough, candidate):
	b = Borough.objects.get(name = borough)
	c = Candidate.objects.get(name = candidate)
	return Vote.objects.get(borough = b, candidate = c)

def getVoivodeshipsForMap():
	res = [v.name for v in Voivodeship.objects.all()]
	return res

def getChartData():
	res = {}
	colors = createColorsList(len(createCandidatesList()))
	counter = 0
	for v in Voivodeship.objects.all():
		votesInVoivodeships = countVotesInVoivodeship(v)
		res[v.name] = createListForChartForVoivodeship(v, colors)
		counter += 1
	return res

def createListForChartForVoivodeship(v, colors):
	res = []
	allVotes = countVotesInVoivodeship(v)
	counter = 0
	left_space = 100
	partPrev = 100
	chartResult = createChartResultForVoivodeship(v.name)
	for name, votes in chartResult:
		part = 100.0 * votes / allVotes
		partRes = 100.0 - part / left_space * 100.0
		left_space -= part
		res.append((partPrev, colors[counter], name))
		partPrev = partRes
		counter += 1
	return res

def countVotesInVoivodeship(v):
	boroughSet = Borough.objects.filter(region__in = v.region_set.all())
	votesInVoivodeship = Vote.objects.filter(borough__in = boroughSet)
	return votesInVoivodeship.aggregate(Sum('votes')).get('votes__sum')


def createTableResult(viewName, name):
	if (viewName == "main"):
		return createTableResultForMain()
	if (viewName == "voivodeship"):
		return createTableResultForVoivodeship(name)
	if (viewName == "region"):
		return createTableResultForRegion(name)
	if (viewName == "borough"):
		return createTableResultForBorough(name)

def createChartResult(viewName, name):
	if (viewName == "main"):
		return createChartResultForMain()
	if (viewName == "voivodeship"):
		return createChartResultForVoivodeship(name)
	if (viewName == "region"):
		return createChartResultForRegion(name)
	if (viewName == "borough"):
		return createChartResultForBorough(name)

def createTableResultForMain():
	res = []
	for v in Voivodeship.objects.all():
		boroughSet = Borough.objects.filter(region__in = v.region_set.all())
		votesInVoivodeship = Vote.objects.filter(borough__in = boroughSet)
		voivodeshipResult = createResultForCandidates(votesInVoivodeship)
		res.append((v.name, voivodeshipResult))
	return res

def createChartResultForMain():
	votesForAll = Vote.objects.all()
	return createResultForCandidates(votesForAll)


def createTableResultForVoivodeship(voivodeshipName):
	res = []
	v = Voivodeship.objects.get(name = voivodeshipName)
	for r in Region.objects.filter(voivodeship = v):
		boroughSet = Borough.objects.filter(region = r)
		votesInRegion = Vote.objects.filter(borough__in = boroughSet)
		regionResult = createResultForCandidates(votesInRegion)
		res.append((r.name, regionResult))
	return res


def createChartResultForVoivodeship(voivodeshipName):
	v = Voivodeship.objects.get(name = voivodeshipName)
	boroughSet = Borough.objects.filter(region__in = v.region_set.all())
	votesInVoivodeship = Vote.objects.filter(borough__in = boroughSet)
	return createResultForCandidates(votesInVoivodeship)

def createTableResultForRegion(regionName):
	res = []
	r = Region.objects.get(name = regionName)
	for b in Borough.objects.filter(region = r):
		votesInBorough = Vote.objects.filter(borough = b)
		boroughResult = createResultForCandidates(votesInBorough)
		res.append((b.name, boroughResult))
	return res

def createChartResultForRegion(regionName):
	r = Region.objects.get(name = regionName)
	boroughSet = Borough.objects.filter(region = r)
	votesInRegion = Vote.objects.filter(borough__in = boroughSet)
	return createResultForCandidates(votesInRegion)

def createTableResultForBorough(boroughName):
	boroughSet = Borough.objects.filter(name = boroughName)
	votesInBorough = Vote.objects.filter(borough__in = boroughSet)
	boroughResult = createResultForCandidates(votesInBorough)
	return [(boroughName, boroughResult)]


def createChartResultForBorough(boroughName):
	boroughSet = Borough.objects.filter(name = boroughName).all()
	votesInBorough = Vote.objects.filter(borough__in = boroughSet)
	return createResultForCandidates(votesInBorough)
	

def createResultForCandidates(votesForPart):
	res = []
	for c in Candidate.objects.all():
		votesForCandidate = votesForPart.filter(candidate = c)
		votes = votesForCandidate.aggregate(Sum('votes')).get('votes__sum')
		res.append((c.name, votes))
	return res

def searchBorough(boroughName):
	result = Borough.objects.filter(name__icontains = boroughName)
	res = []
	for b in result:
		res.append(b.name)
	return res