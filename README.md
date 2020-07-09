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
Here the intron channel will be shown with red circles, and the speckle channel will be shown in green. For measuring speckle distances, I prefer to use the black and white mode.

#### This involves switching to the "Exon" channel on the left.
<img src="https://github.com/katealexander/distanceToSpeckle-semiManual/blob/master/distToSpeckleImages/First.png" alt="drawing" width="700"/>

#### Next, zoom in so that you can see individual pixels:
<img src="https://github.com/katealexander/distanceToSpeckle-semiManual/blob/master/distToSpeckleImages/Second.png" alt="drawing" width="700"/>
  
#### Finally, click on the edge of the nearest speckle to the red circle. If the red circle is in a speckle, click directly on the middle of the red circle.
<img src="https://github.com/katealexander/distanceToSpeckle-semiManual/blob/master/distToSpeckleImages/Third.png" alt="drawing" width="700"/>

  
A green circle will appear. Do not worry if the green circle is not where you clicked! The subsequent measurments are based on where you click, not where the green circle appears. If you are unsure which speckle is the closest, click on both speckles. We later identify the nearest clicked location to each transcription site.

