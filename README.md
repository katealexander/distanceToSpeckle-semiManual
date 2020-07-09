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
Also threshold the speckle channel. The exact thresholding doesn't matter for the analysis, but if too many spots are selected, the Gaussian fitting in subsequent steps will take a long time to run.
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
Here the intron channel will be shown with red circles, and the speckle channel will be shown in green. For measuring speckle distances, I prefer to use the black and white mode:

<img src="https://github.com/katealexander/TSAseq-Alexander2020/blob/master/images/Venny.png" alt="drawing" width="500"/>
