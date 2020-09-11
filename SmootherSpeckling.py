# this is python2. All the info about it is best accessed here:
# https://docs.python.org/2/library/index.html
from ij.measure import ResultsTable
from ij import WindowManager
from ij import IJ
from ij.plugin.filter import Analyzer
import re
import csv
from os.path import join, exists
import os
from ij.io import Opener

class ResultsTableToCSV:
	def __init__(self,channel1,channel2,ignoreString):
		self.toIgnore = ignoreString
		self.channel1 = channel1
		self.channel2 = channel2

	def getImageNames(self):
		try:
			images = WindowManager.getImageTitles()
			if len(images) ==0: x=x #throw NameError
			incorrectChannel1 = True
			incorrectChannel2 = True
			for imageName in images:
				#this first if statement wChannel2ill skip images with *ignoreString in their name
				if not re.search(self.toIgnore,imageName):
					if re.search(self.channel1,imageName): 
						primary = imageName
						incorrectChannel1 = False
					else:
						if re.search(self.channel2,imageName): 
							secondary = imageName
							incorrectChannel2 = False
			if incorrectChannel1 & incorrectChannel2: 
				print("the primary and secondary channel were entered incorrectly.Enter strings into the last line of this script that identify the primary and secondary images. Alternatively, rename your speckle image to Channel2.tif and your primary image to Channel1.tif.")
		except:
			print("Can't find images with '{}' and '{}' in their names in Fiji. \nPlease do make sure that they're opened in Fiji: \n\tthis can be done via the File dropdown \n\tor by clicking and dragging the primary and secondary images into Fiji.".format(self.channel1,self.channel2))
			primary = ""
			secondary = ""
			images = set()
		finally:
			return primary,secondary, images
	#roiAnalysisToWrite takes the Roi Analysis table and turns it into a table that
	#python can write to a csv
	def roiAnalysisToWrite(self,roiTableName):
		#I can't figure out the syntax to preallocate memory,
		#this will not scale to many speckles
		try:
			RT = ResultsTable.getResultsTable(roiTableName)
			headings = RT.getHeadings()
			labelCol = RT.getColumnAsVariables(headings[0])
			headers = headings[1:]
			numCols = len(headers)
			numRows = len(labelCol)
			out = []
			for col in range(numCols):
				out.append([])
				column = RT.getColumnAsVariables(headers[col])
				for row in range(numRows):
					out[col].append(column[row].getValue())
			outT = []
			for i in range(numRows):
				lis = []
				lis.append(labelCol[i].getString())
				for j in range(numCols):
					lis.append(out[j][i])
				outT.append(lis)
			return outT
		except:
			print("failed roi read")
			return []
	#readResultsTablesOfNumbers takes the speckle list table and turns it into a table that
	#python can write to a csv
	def readResultsTablesOfNumbers(self,tableName):
		#I can't figure out the syntax to preallocate memory,
		#this will not scale to many speckles
		try:
			RT = ResultsTable.getResultsTable(tableName)
			headers = RT.getHeadings()
			labelCol = RT.getColumnAsVariables(headers[0])
			numCols = len(headers)
			numRows = len(labelCol)
			out = []
			for col in range(numCols):
				out.append([])
				column = RT.getColumnAsVariables(headers[col])
				for row in range(numRows):
					out[col].append(column[row].getValue())
			outT = []
			for i in range(numRows):
				lis = []
				for j in range(numCols):
					lis.append(out[j][i])
				outT.append(lis)
			return outT
		except:
			print("failed speckle read")
			return []
	#this function does operation of adding left hand side column to the table
	def appendColToFront(self,column,matrix):
		try:
			for row in matrix:
				row.insert(0,column)
		except:
			print("failed to append the first entry to the front input"
			+"of the all the entries of the second.")
		finally:
			return matrix
		
class SaveStuff:
	def __init__(self,uniqueFileName):
		self.uniqueID = uniqueFileName[:-4]
		
		self.downloadsFolder = join(IJ.getDir("downloads"),"SpeckleResults")
		if not exists(self.downloadsFolder):
			os.mkdir(self.downloadsFolder)
			
	#this writes a suitably formatted table to a csv
	def table2CSV(self,csvName, writeTable):
		try:
			with open(join(self.downloadsFolder,csvName), 'a') as f:
				writer = csv.writer(f)
				writer.writerows(writeTable)
		except:
			print("failed to write table to csv.")
		finally:
			print("")
	#this saves the logs with a name based on what you add in the columns 
	def saveLogs(self):
		try:
			log = IJ.getLog()
			#change the below line to f=open(join(self.downloadsFolder,"logs.txt"),'a') 
			#for one log file to rule them all...it will append all logs to one file.
			f = open(join(self.downloadsFolder,self.uniqueID + " logs.txt"),'w')
			f.write(log)
			print("saved the log.")
		except:
			print("no speckles.")
		finally:
			f.close()
			
	def saveNewImages(self,oldImages):
		try:
			#this will extract all the new images generated sence oldImages was created
			#and will save them all to the downloads folder
			newImages = WindowManager.getImageTitles()
			titles2Save = list(set(newImages) - set(oldImages))
			iterID = int(0)
			for image in titles2Save:
				im2Save = WindowManager.getImage(image)
				IJ.save(im2Save, join(self.downloadsFolder,"speckleInspectorOutput "+self.uniqueID + "{}.tif".format(iterID)))
				iterID = iterID + 1
			for image in oldImages:
				#this loop will kill off the save dialog box that will 
				#pop up for the secondary image
				im2Save = WindowManager.getImage(image)
				im2Save.changes = False
			print("saved new images.")
		except:
			print("failed to save new images.")
		finally:
			print("")
			
	def saveNewImage(self,oldImages):
		try:
			#this will extract one image
			newImages = WindowManager.getImageTitles()
			title2Save = list(set(newImages) - set(oldImages))
			im2Save = WindowManager.getImage(title2Save[0])
			IJ.save(im2Save, join(self.downloadsFolder,"speckleInspectorOutput "+self.uniqueID + ".tif"))
			for image in list(set(newImages)-set([title2Save[0]])):
				#this loop will kill off the save dialog box that will 
				#pop up for other images bescides the Inspector output
				im2Save = WindowManager.getImage(image)
				im2Save.changes = False
			print("saved new image.")
		except:
			print("failed to save image.")
		finally:
			print("")
			
	def saveAllImages(self,oldImages):
		try:
			#this will extract all the new images generated sence oldImages was created
			#and will save them all to the downloads folder
			titles2Save = WindowManager.getImageTitles()
			inspectorOutput = list(set(titles2Save) - set(oldImages))[0]
			im2Save = WindowManager.getImage(inspectorOutput)
			IJ.save(im2Save,join(self.downloadsFolder,"InspectorOutput"+self.uniqueID+".tif"))
			iterID = int(0)
			for image in list(set(titles2Save) - set([inspectorOutput])):
				
				im2Save = WindowManager.getImage(image)
				IJ.save(im2Save, join(self.downloadsFolder,self.uniqueID 
					+ " speckleInspectorImage{}.tif".format(iterID)))
				iterID = iterID + 1
			print("saved all images.")
		except:
			print("failed to save all images.")
		finally:
			print("")

class Binarize:
	def __init__(self,primaryThreshold,secondaryThreshold,primaryImage,secondaryImage):
		self.primaryLowerThreshold = primaryThreshold
		self.secondaryLowerThreshold = secondaryThreshold
		self.primaryImage = primaryImage
		self.secondaryImage = secondaryImage
		self.primaryUpperThreshold = 65535
		self.secondaryUpperThreshold = 183
		self.renyiBinarization()
		
	def renyiBinarization(self):
		try:
			IJ.selectWindow(self.primaryImage)
			primaryImageID = IJ.getImage()
			IJ.setAutoThreshold(primaryImageID, "Default dark")
			IJ.setThreshold(self.primaryLowerThreshold, self.primaryUpperThreshold)
			IJ.run("Convert to Mask")
			
			IJ.selectWindow(self.secondaryImage)
			secondaryImageID = IJ.getImage()
			IJ.setAutoThreshold(secondaryImageID,"Default dark")
			IJ.setThreshold(self.secondaryLowerThreshold,self.secondaryUpperThreshold)
			IJ.run("Convert to Mask")
		except:
			print("unable to binarize images.")
		finally:
			return self
		
class Binarize:
	def __init__(self,primaryThreshold,secondaryThreshold,primaryImage,secondaryImage):
		self.primaryLowerThreshold = primaryThreshold
		self.secondaryLowerThreshold = secondaryThreshold
		self.primaryImage = primaryImage
		self.secondaryImage = secondaryImage
		self.primaryUpperThreshold = 65535
		self.secondaryUpperThreshold = 183
		self.renyiBinarization()
		
	def renyiBinarization(self):
		try:
			IJ.selectWindow(self.primaryImage)
			primaryImageID = IJ.getImage()
			IJ.setAutoThreshold(primaryImageID, "Default dark")
			IJ.setThreshold(self.primaryLowerThreshold, self.primaryUpperThreshold)
			IJ.run("Convert to Mask")
			
			IJ.selectWindow(self.secondaryImage)
			secondaryImageID = IJ.getImage()
			IJ.setAutoThreshold(secondaryImageID,"Default dark")
			IJ.setThreshold(self.secondaryLowerThreshold,self.secondaryUpperThreshold)
			IJ.run("Convert to Mask")
		except:
			print("unable to binarize images.")
		finally:
			return self
		
		
		
def main(channel1,channel2,ignoreString,primarySize,primaryImageThresh,secondaryImageThresh):
	def writeTablesToCSV(id,roiOut,speckleOut):
		try:
			#append your labels to them before they're written
			identifier =id[:-4]
			speckleOut_ = RTC.appendColToFront(identifier, speckleOut)
			roiOut_ = RTC.appendColToFront(identifier, roiOut)
			#save the tables to csvs -- they will append to a currently existing csv 
			#or create a new one
			Saves.table2CSV("speckleOutput.csv",speckleOut_)
			Saves.table2CSV("AnalysisOutput.csv",roiOut_)
			print("finished writing tables to csvs.")
		except:
			print("failed to write to csvs.")
		finally:
			print("")
			
	#Begin
	try:
		RTC = ResultsTableToCSV(channel1,channel2,ignoreString)
		primary,secondary,images = RTC.getImageNames()
		Binarize(primaryImageThresh,secondaryImageThresh,primary,secondary)
		speckleInputs = "primary=[{}] " \
			 "secondary=[{}] " \
			 "redirect=None min_primary_size={} show=secondary " \
			 "exclude speckle statistic secondary_object" 
		IJ.run("Speckle Inspector",speckleInputs.format(primary,secondary,primarySize))
	
		Saves = SaveStuff(primary)
		Saves.saveLogs()
		Saves.saveNewImages(images)
		
		speckleTableName = "Speckle List " + primary
		roiTableName = "Roi Analysis"
		
		roiOut = RTC.roiAnalysisToWrite(roiTableName)
		speckleOut = RTC.readResultsTablesOfNumbers(speckleTableName)
		WindowManager.closeAllWindows()
		fijiDir = IJ.getDir("imagej")
		fijiScriptsDir = join(fijiDir,"scripts")
		writeTablesToCSV(primary,roiOut,speckleOut)
		IJ.open(join(fijiScriptsDir,"SmootherSpeckling.py"))
		print("script completed successfully.")
	except:
		print("sorry, the script broke :/")
	finally:
		print("")
	#End
	
if __name__ in ['__builtin__','__main__']:
	#these are examples below. Change them to your values
		#the first input must  be a character string, i.e. "primary", 
		#that does not exist in the secondary image title but does
		#in the first image title. 
		#the second input is the same for the secondary image.
		#the third input is a string that if it is in an image title that
		#is open in Fiji, then 
	main("Channel","Channel2","Inspector",500,15,115)


