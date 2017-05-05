# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm
from django.db import models


class Candidate(models.Model):
	name = models.CharField(max_length = 30)

	class Meta:
		db_table = "candidates"

class Voivodeship(models.Model):
	name = models.CharField(max_length = 50)

	class Meta:
		db_table = "voivodeships"

class Region(models.Model):
	name = models.CharField(max_length = 50)
	voivodeship = models.ForeignKey(Voivodeship)

	class Meta:
		db_table = "regions"

class Borough(models.Model):
	name = models.CharField(max_length = 50)
	region = models.ForeignKey(Region)

	class Meta:
		db_table = "boroughs"

class Vote(models.Model):
	borough = models.ForeignKey(Borough)
	candidate = models.ForeignKey(Candidate)
	votes = models.IntegerField(default = 0)

	class Meta:
		db_table = "votes"

class VoteForm(ModelForm):
	class Meta:
		model = Vote
		fields = ['votes']
