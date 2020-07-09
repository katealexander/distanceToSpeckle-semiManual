#!/usr/bin/python


import sys, re, numpy

def main(args):
	if len(args) != 3: sys.exit("USAGE: python calcSpeckleDist_DNAfish.py BigTable speckle > outfile")
	
	#distance between sections
	slice = float(0.33)
	pixel = float(0.13)
	
	## to make sure we're only counting called transcription sites, txnSiteIntensities from BigTable must match intron intensity from speckleFISH file
	f = open(args[1])
	line = f.readline()[:-1]
	line = f.readline()[:-1]
	intensities = []
	while line != "":
		if line.split(',')[3] == 'txnSitesExonIntensities':
			intensities.append(line.split(',')[2][:8])
		line = f.readline()[:-1]
	f.close()
	
	f = open(args[2])
	line = f.readline()[:-1]
	line = f.readline()[:-1]
	speckleCoords = {} ## for each object key will be array;object, value will be a list of lists of [x,y]
	FISHcoords = {} ## same structure as speckle coords
	while line != "":
		array = line.split(",")[1]
		object = line.split(",")[0]
		k = str(array) + ";" + str(object)
		FISHx = line.split(",")[2]
		FISHy = line.split(",")[3]
		speckX = line.split(",")[9]
		speckY = line.split(",")[10]
		if line.split(',')[5][:8] in intensities:
			if k in FISHcoords.keys():
				if [FISHx, FISHy] not in FISHcoords[k]:
					FISHcoords[k].append([FISHx, FISHy])
			else:
				FISHcoords[k] = [[FISHx, FISHy]]
		if k in speckleCoords.keys():
			speckleCoords[k].append([speckX, speckY])
		else:
			speckleCoords[k] = [[speckX, speckY]]
		line = f.readline()[:-1]
	f.close()
	
	
	for object in FISHcoords.keys():
		speckles = speckleCoords[object]
		for site in FISHcoords[object]:
			dist = getNearestSpeckle(site, speckles, pixel)
			print object + "\t" + str(dist)
			
			
			
def getNearestSpeckle(site, speckles, pixel):
	dist = 20
	siteX = float(site[0])
	siteY = float(site[1])
	for speckle in speckles:
		speckleX = float(speckle[0])
		speckleY = float(speckle[1])
		d = pixel*numpy.sqrt(numpy.square(siteX-speckleX) + numpy.square(siteY-speckleY))
		if float(d) < float(dist):
			dist = d
	return dist
	
		
if __name__ == "__main__": main(sys.argv)
