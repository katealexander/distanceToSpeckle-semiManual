# Semi-manual measurement of speckle distances to transcription sites from immunoRNA-FISH or immunoDNA-FISH data
This repository describes how to co-opt [rajlabimagetools](https://github.com/arjunrajlaboratory/rajlabimagetools/wiki) for the measurement of distances from transcription sites to nuclear speckles (or any other feature of interest that can be seen in imaging data).
## Data preparation
First [install rajlabimagetools](https://github.com/arjunrajlaboratory/rajlabimagetools/wiki/Installation), run through the [worked example](https://github.com/arjunrajlaboratory/rajlabimagetools/wiki/workedExample), and [call transcription sites](https://github.com/arjunrajlaboratory/rajlabimagetools/wiki/Transcription%20Site%20Analysis). 
### Breifly, this involves (all described in greater detail in above links):
#### Cell segmentation
```
improc2.segmentGUI.SegmentGUI
```
#### Processing image objects
```
improc2.processImageObjects
```
#### Thresholding
```
improc2.launchThresholdGUI
```
Also threshold the speckle channel. The exact thresholding of the speckle channel doesn't matter for the analysis, but if too many spots are selected, the Gaussian fitting in subsequent steps will take a long time to run.
#### Transcription site calling
```
improc2.txnSites2.launchGUI('tmr','alexa')
```
#### Extracting the data
```
ExtractTxnSiteData('molten', 'exonintron', 'tmr', 'alexa')
```
This data extraction will result in the table called "BigTable.csv" that will later be used to calculate speckle distances and measure normalized transcription site intensities.
  
In this example, these are the identities of the channels used are:
tmr - RNA-FISH exon channel
alexa - RNA-FISH intron channel
gfp - immunofluorescence speckle channel

## Clicking nearest speckle
Where this analysis differs from the standard use of rajlabimage tools is its cooptation to assess speckle distances. To measure speckle distances, we make use of the Transcription Site GUI used above, which stores the coordinates of the clicked locations. We therefore run transcription site calling again, but this time with the speckle channel as the "exons"
```
improc2.txnSites2.launchGUI('tmr','alexa')
```
Here the intron channel will be shown with red circles, and the speckle channel will be shown in green. For measuring speckle distances, I prefer to use the black and white mode.

#### This involves switching to the "Exon" channel on the left.
<img src="https://github.com/katealexander/distanceToSpeckle-semiManual/blob/master/distToSpeckleImages/First.png" alt="drawing" width="700"/>

#### Next, zoom in so that you can see individual pixels:
<img src="https://github.com/katealexander/distanceToSpeckle-semiManual/blob/master/distToSpeckleImages/Second.png" alt="drawing" width="700"/>
  
#### Finally, click on the edge of the nearest speckle to the red circle. If the red circle is in a speckle, click directly in the middle of the red circle.
<img src="https://github.com/katealexander/distanceToSpeckle-semiManual/blob/master/distToSpeckleImages/Third.png" alt="drawing" width="700"/>

  
A green circle will appear. Do not worry if the green circle is not where you clicked! The subsequent measurments are based on where you click, not where the green circle appears. If you are unsure which speckle is the closest, click on both speckles. We later identify the nearest clicked location to each transcription site.

## Extracting clicked data from MATLAB
To extract the clicked data, you'll need to first edit the extraction MATLAB scripts to designate the directory your images analysis is in:
```
%% extract data to, then extract data from (directories)
%%
extractionDir = '/YOURDIRECTORYNAME';
bigDataDir = '/YOURDIRECTORYNAME';
%% extract transcription site data
clearvars -except bigDataDir extractionDir

% name of folder that experiment is actually in
folder = {...
'',...
''};
eid = {...
    '/sc35Intron', '/exonIntron'};
```
You can also edit the names of your output files, which in this example will be called "sc35Intron.csv" and "exonIntron.csv". Then copy the entire script and paste it into MATLAB.
  
For RNA-FISH data, use RNA-FISH_extraction.m  
For DNA-FISH data, use DNA-FISH_extraction_oneGene.m

## Calculating transcription site speckle distances and normalized transcription site intensities
#### DNA-FISH data
For DNA-FISH data just the distance from the loci to the nearest speckle is calculated
```
USAGE: python calcSpeckleDist_DNAfish.py BigTable.txt speckle_p53targ.csv > outfile
```
The above Python script will output a text file of the following format:
```
4;6	0.06866282216911732
1;9	0.34689006393173993
4;5	0.16274410926527397
4;2	0.09576229634367708
4;3	0.3400109084438244
4;1	0.018533554209403582
1;2	0.06876807547733012
1;1	0.04707596887163341
1;6	0.0434855334186055
```
The first column is the object;array number. This can be used to go back and look at the individual cells that gave each distance value. The second column is the distance to the speckle in microns. Unless your pixel sizes is 0.13 microns like mine is, you will need to edit the Python script on Line 11 to reflect your pixel size in microns.
```
pixel = float(0.13)
```
#### RNA-FISH data
For RNA-FISH data, several data are collected and reported.
```
USAGE: python calcSpeckleDists.py exonIntron.csv sc35Intron.csv BigTable.txt > outfile
```
The above Python script will output a text file of the following format:
```
objectID	intronX	intronY	intronZ	intronIntensity	exonX	exonY	exonZ	clickedX	clickedY	exonIntensity	numExonSpots	exonAveIntensity	DistToSpeckle	TSrelIntensity
10;2	294.067348271708	142.794755062985	14	0.016021247009529	294.144161321174	143.632898996309	15	294.702723735409	142.312451361868	0.00505217634074242	251	0.001541497923097139	0.18129048223645933	3.27744608996
10;2	310.883381388833	176.632277524355	15	0.0105430935012985	310.492734734446	176.682962250585	15	311.577431906615	176.927237354086	0.00560965599976076	251	0.001541497923097139	0.0629392508424831	3.63909410172
4;2	60.1641662212918	103.852973348334	19	0.0220332180035183	60.5421846105646	103.876183195929	19	60.2447470817121	103.736186770428	0.00536278815308674	53	0.001689739925649693	0.2445194892541605	3.17373583454
```
It reports the locations of the transcription site spots for both the intron and exon channels (intronX, intronY, exonX, exonY). It also reports clicked locations (clickedX, clickedY). The distance to the speckle (DistToSpeckle) is calculated in 2D, and does not take the Z coordinates into consideration. The intensity of the intron transcription site and exon transcription site spot (intronIntensity, exonIntensity), as well as the median intensity of all exon spots (exonAveIntensity) are reported. The intensity of the transcription site exon channel relative to the median intensity of all exon spots is also reported (TSrelIntensity), as is the total number of exon spots detected (numExonSpots). Based on these data, you can now relate speckle distance to any other variable of interest.

