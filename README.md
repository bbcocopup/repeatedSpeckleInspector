# repeatedSpeckleInspector
Run the Fiji or ImageJ speckle inspector with the same settings for a folder filled with subfolders containing image pairings. 
Your structure should be as follows 
  Fiji.app/images/demo
    capture1
      ch1.tif
      ch2.tif
    capture2
      ch1.tif
      ch2.tif
      ...
    ...
<br />


<br />
Note) You can record a macro in Fiji that will track your manual execution of the speckle inspector. Look at the format string in the macro after you run it.
It looks something like "primary=[yourFileName.TIF]..." you can replace the inspectorInput with that but replace the 
file names with brackets '{}'. to change your settings. Or message me and I may help!

Instructions to use “SmootherSpeckling.py”

In a single run, this code will convert 16-bit TIFs into binary 8-bit TIFs at custom set thresholds, then run the BioVoxxel Speckle Inspector for each of the binary pairs, and compile the results in a folder containing the binary images, the ‘speckle image’ which indicates the speckle count that cells in the image received (for traceability), and spreadsheets (in csv format) containing the measurements for each image pair. 

You can set your own lower threshold for each of two channels to optimize signal-to-noise for your assay. **You should manually adjust images (using command t in ImageJ) to get a sense of where your threshold should be.** This will vary by assay and should be determined by testing for the highest (most sensitive) lower threshold that doesn’t lead to high background. The goal is to detect true signal without losing foci. You can also customize your minimum primary image size. 

Before you begin: 

1.	Exposure times for your protein of interest should be the same for all of your images. 
2.	You will need to start with single channel 16-bit TIFs in individual folders. 16-bit images contain far more information than 8-bit images. You can do this when you export images from the AxioVision:
a.	Make sure “Create project folder” is checked (under the top file panel)
b.	Do not generate merged images
c.	Use channel names
d.	Uncheck “Convert to 8-bit” (left)
e.	Export as TIF (middle)
3.	Download (Fiji is Just) ImageJ if you haven’t already
a.	https://imagej.net/Fiji/Downloads
4.	Install the BioVoxxel Toolbox for ImageJ if you haven’t already
a.	https://imagej.net/BioVoxxel_Toolbox
5.	Download SmootherSpeckling.py from: https://github.com/kyleButler9/repeatedSpeckleInspector
a.	Click the green “Code” button on the home screen
b.	Then click “Download ZIP”
c.	Unzip the file
6.	Save SmootherSpeckling.py to the “scripts” folder in the Fiji application
a.	Copy the .py file
b.	Go to Applications in your file explorer (Finder)
c.	Open the app’s files by right clicking it and then clicking “open package contents”
7.	Save your images in a folder within Fiji’s “images” folder

Set up and run the script: 

8.	Open Fiji. 
9.	Open the script. Go to File  Open  Fiji  scripts  SmootherSpeckling.py
10.	Edit the code for your experiment in the last line (keep the quotation marks):
a.	inputFolderName
i.	the name of the folder of images you copied into the Fiji app images folder
b.	outputFolderName
i.	the name you want for the folder that will contain your results. It will be found in your Downloads folder. 
1.	I usually include the secondary lower threshold in the name in case you want to compare runs using different thresholds. 
c.	DAPI
i.	The ‘keyword’ found in the name of the primary images. If you exported images using channel names, you do not need to change this. 
d.	GFP
i.	The ‘keyword’ found in the name of the secondary images. Might be dsRed (whichever channel you used for the protein of interest). If you forgot to check “Use channel names” in AxioVision, use the channel label in your image title names.
e.	3000 
i.	Number of pixels you want to be the minimum primary size during the speckle inspection.
ii.	The number 3000 is chosen to exclude micronuclei but does not ignore full nuclei. 
f.	10
i.	The lower threshold** for your DAPI (primary) image.
ii.	The goal is to cover the entire nucleus. A bit of background is actually fine (only for DAPI), as long as it doesn’t merge signals from your nuclei. 
g.	80
i.	Replace with your lower threshold** for your secondary image (your protein of interest).
11.	Click run and watch the data run.
12.	It is done when it says “script completed successfully” in the console and no more windows are popping up.
13.	It is recommended that you save (command s) this edited code for the next time you use it (or forget what settings you used)

Troubleshooting:
•	For error messages, try breaking the images into smaller runs.

After running SmootherSpeckling.py:

14.	Go to your downloads folder
15.	Open the SpeckleResults folder (or whatever you named it)
16.	Check that all is there: 
a.	analysisOutput.csv
i.	This is the compiled ROI (region of interest) data for each speckle
b.	speckleOutput.csv
i.	This is the compiled list of the number of speckles per nucleus
c.	speckleInspectorImage0 for each image
i.	This is the binary image of the speckle protein signal
d.	speckleInspectorImage1 for each image
i.	This is the binary image of DAPI signal
e.	logs.txt for each image
f.	InspectorOutput.tif for each image
i.	This counts the nuclei and shows the number of speckles counted per nucleus in white text. The nuclei are pink. The ignored DAPI signal is black.
17.	Save the SpeckleResults folder somewhere on your computer.
18.	Open all of the InspectorOutput files. Scroll through for quality control of each image. 

Clean up the data and tables

19.	Make a list of each “bad” image’s number or name by checking the ‘inspect images’ (TIF with pink nuclei with nucleus number and counted speckle number). You will delete this data from each of the two results csvs. I suggest you save this list to your computer for record keeping. Likewise, it is recommended that you list the reason for deleting the data. Examples of data to delete:
a.	A micronucleus that is counted as a nucleus (primary object) (pink with a number of speckles listed in white).
b.	Multiple nuclei counted as a single nucleus (because they are too close together).
c.	Any aberrant DAPI staining counted as an individual nucleus (pink).
d.	Some things that are okay:
i.	Black DAPI signal in the background. As long as it’s not counted as a nucleus (pink), then it won’t affect your data analysis.
ii.	Black DAPI signal that was not counted because it was on the edge of the image. The program is set to run to ignore primary objects on the edges so that you don’t get an incomplete readout of a nucleus.
iii.	Pink blobs connected to a nucleus. I believe these are micronuclei that are close to the nucleus, and should not affect your analysis. The speckle analysis does not depend on nucleus size.
e.	Save your list. 
20.	Save speckleOutput.csv and AnalysisOutput.csv with an identifying name for the experiment. For each run, the code will always be directed to a csv with the default name. 



****How to use thresholding (generates binary images)
 Drag 16-bit TIF into Fiji. The image should appear.
Convert to binary image :
•	Shift command t (Mac)
•	Best setting for DAPI = Renyi Entropy
o	Use Red, not B&W setting
o	Adjust lower threshold accordingly if some nuclei are not fully covered in red or if speckles are not specific or not counted
o	Upper threshold should be 65534
•	Click Set
•	Record the Renyi Entropy Lower Threshold number
•	Click Apply
