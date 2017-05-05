# -*- coding: utf-8 -*-
from models import *
import csv

# this script is used for initial data loading 
file = 'app2/start_data/pkw2000.csv'

candidatesList = ['Dariusz Maciej GRABOWSKI', 'Piotr IKONOWICZ', 'Jarosław KALINOWSKI', 'Janusz KORWIN-MIKKE', 'Marian KRZAKLEWSKI', 'Aleksander KWAŚNIEWSKI', 'Andrzej LEPPER', 'Jan ŁOPUSZAŃSKI', 'Andrzej Marian OLECHOWSKI', 'Bogdan PAWŁOWSKI', 'Lech WAŁĘSA', 'Tadeusz Adam WILECKI']
candidates = []
voivodeships = []
regions = []
boroughs = []
votes = []

def loadStartData():
	data = []
	with open(file, 'r') as f:
		reader = csv.DictReader(f)
		data = list(reader)

	for row in data:
		for candidateName in candidatesList:
			votes = int(row[candidateName])
			voivodeship = row['Województwo']
			region = row['Nr okręgu']
			borough = row['Gmina']
			updateSets(candidateName, votes, voivodeship, region, borough)
	addSetsToDatabase()

def updateSets(candidate, votes, voivodeship, region, borough):
	c = addCandidateToSet(candidate)
	v = addVoivodeshipToSet(voivodeship)
	r = addRegionToSet(region, v)
	b = addBoroughToSet(borough, r)
	addVoteToSet(c, b, votes)

def addCandidateToSet(candidate):
	for c in candidates:
		if c.name == candidate:
			return c
	res = Candidate(name = candidate)
	candidates.append(res)
	return res

def addVoivodeshipToSet(voivodeship):
	for v in voivodeships:
		if v.name == voivodeship:
			return v
	res = Voivodeship(name = voivodeship)
	voivodeships.append(res)
	return res

def addRegionToSet(region, voivodeship):
	for r in regions:
		if r.name == region and r.voivodeship == voivodeship:
			return r
	res = Region(name = region, voivodeship = voivodeship)
	regions.append(res)
	return res

def addBoroughToSet(borough, region):
	for b in boroughs:
		if b.name == borough and b.region == region:
			return b
	res = Borough(name = borough, region = region)
	boroughs.append(res)
	return res

def addVoteToSet(candidate, borough, votesNumber):
	res = Vote(candidate = candidate, borough = borough, votes = votesNumber)
	votes.append(res)
	return res



def addSetsToDatabase():
	#  TODO sprawdzic czy mozna ladowac obiekty do bazy danych za jedno polaczenie
	saveList(candidates)
	saveList(voivodeships)
	for r in regions:
		v = findInList(_list = voivodeships, name = r.voivodeship.name)
		r.voivodeship = v
	saveList(regions)
	for b in boroughs:
		r = findInList(_list = regions, name = b.region.name)
		b.region = r
	saveList(boroughs)
	for v in votes:
		b = findInList(_list = boroughs, name = v.borough.name)
		c = findInList(_list = candidates, name = v.candidate.name)
		v.borough = b
		v.candidate = c
	saveList(votes)


def findInList(name = "", _list = []):
	for obj in _list:
		if name == "" or name == obj.name:
			return obj

def saveList(_list):
	counter = 0
	max_counter = len(_list)
	for obj in _list:
		obj.save()
		counter += 1	
		print str(counter) + "/" + str(max_counter)

