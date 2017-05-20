from rest_framework import serializers
from app2.models import Candidate, Vote, Borough

class CandidateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Candidate
		fields = ('id', 'name')

class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = ('id', 'votes', 'candidate', 'borough')