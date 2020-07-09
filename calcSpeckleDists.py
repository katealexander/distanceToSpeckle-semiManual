#!/usr/bin/python

#for each transcription site return:
#	1. Object and array number
#	2. distance to nearest speckle
#	3. # TS in that cell
#	4. # RNA molecules per cell
#	5. intensity of transcription site (exon TS normalized to total exons) 

import sys, re, numpy

def main(args):
	if len(args) != 4: sys.exit("USAGE: python calcSpeckleDists.py exons speckle BigTable > outfile")
	
	#distance between sections
	slice = float(0.33)
	pixel = float(0.13)
	
	# read in dictionary where key is object;array and value is a list of lists, with each item in list being a called transcription site
	f = open(args[1])
	line = f.readline()[:-1]
	line = f.readline()[:-1]
	exonTSs = {}
	while line != "":
		items = line.split(',')
		key = str(items[1]) + ";" + str(items[0])
		value = items[2:]
		if abs(float(items[4]) - float(items[8])) <= 2:  ## removes transcription sites where they are on completely different z sections
			if key in exonTSs:
				exonTSs[key] += [value]
			else:
				exonTSs[key] = [value]
		line = f.readline()[:-1]
	f.close
	
	f = open(args[2])
	line = f.readline()[:-1]
	line = f.readline()[:-1]
	speckles = {}
	while line != "":
		items = line.split(',')
		key = str(items[1]) + ";" + str(items[0])
		value = items[2:]
		if key in speckles:
			speckles[key] += [value]
		else:
			speckles[key] = [value]
		line = f.readline()[:-1]
	f.close
	
	# add total exon spots of each object and average exon intensity
	f = open(args[3])
	line = f.readline()[:-1]
	line = f.readline()[:-1]
	intensities = {}
	while line != "":
		items = line.split(',')
		if items[3] == "numExonSpots":
			key = str(items[0]) + ";" + str(items[1])
			numSpots = items[2]
			if key in exonTSs.keys():
				for value in exonTSs[key]:
					value.append(numSpots)
		if items[3] == "exonIntensities":
			key = str(items[0]) + ";" + str(items[1])
			intensity = items[2]
			if key in intensities.keys():
				intensities[key].append(float(intensity))
			else:
				intensities[key] = [float(intensity)]
		line = f.readline()[:-1]
	f.close
	
	for key in intensities.keys():
		if key in exonTSs.keys():
			# get average intensity
			aveInt = numpy.mean(intensities[key])
			for value in exonTSs[key]:
				value.append(aveInt)

	print 	"objectID	intronX	intronY	intronZ	intronIntensity	exonX	exonY	exonZ	clickedX	clickedY	exonIntensity	numExonSpots	exonAveIntensity	DistToSpeckle	TSrelIntensity"
	
	# for every transcription site, find the nearest speckle, calculate exonic TS intensity
	for cell in exonTSs.keys():
		for TS in exonTSs[cell]:
			if cell in speckles.keys():
				dist = findNearestSpeckle(speckles, TS, cell, slice, pixel)
				TS.append(dist)
			else:
				TS.append('na')
			TS.append(float(TS[9])/float(TS[11]))
			TS = [str(i) for i in TS]
			print cell + "\t" + "\t".join(TS)				
			
	
def findNearestSpeckle(speckleDict, TS, key, slice, pixel):
	speckles = speckleDict[key]
	TSx = float(TS[4])
	TSy = float(TS[5])
#	TSz = float(TS[2])*slice
	finalDist = 100
	for speckle in speckles:
		speckleX = float(speckle[7])
		speckleY = float(speckle[8])
#		speckleZ = float(speckle[6])*slice
		dist = pixel*numpy.sqrt(numpy.square(TSx-speckleX) + numpy.square(TSy-speckleY))
#		dist = numpy.sqrt(numpy.square(TSx-speckleX) + numpy.square(TSy-speckleY) + numpy.square(TSz-speckleZ))
		if dist < finalDist:
			finalDist = dist
	return finalDist
		
		
	
if __name__ == "__main__": main(sys.argv)


