from app2.models import *

counter = 0
maxVal = len(Vote.objects.all())
for v in Vote.objects.all():
	c = v.candidate
	b = v.borough
	vv = Vote.objects.filter(candidate = c).filter(borough = b)
	counter += 1
	print str(counter) + '/' + str(maxVal)
	if len(vv) > 1:
		vv[1].delete()

counter = 0
maxVal = len(Borough.objects.all())
for b in Borough.objects.all():
	bb = Borough.objects.filter(name = b.name)
	counter += 1
	print str(counter) + '/' + str(maxVal)
	if len(bb) > 1:
		for i in range(1, len(bb)):
			bb[i].delete()
