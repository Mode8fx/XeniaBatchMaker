import sys
import os
from os import path, walk, mkdir
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from gatelib import *

outputDir = path.join(getCurrFolder(), "Xenia Shortcuts")
titleByte = 0x1692
addOnByte = 0x412

def main():
	Tk().withdraw()
	if path.exists(outputDir):
		print("The directory \""+outputDir+"\" already exists. Either remove or rename this directory.")
		inputHidden("Press Enter to exit.")
		sys.exit()
	print("Select your Xenia executable (Regular or Canary). Created shortcuts will use this executable.")
	xeniaExe = askopenfilename(filetypes=[("Xenia Executable", ".exe")])
	print(xeniaExe)
	if xeniaExe == "":
		inputHidden("\nAction cancelled. Press Enter to exit.")
		sys.exit()
	if not path.isfile(xeniaExe):
		inputHidden("\nInvalid executable path. Press Enter to exit.")
		sys.exit()
	print("\nSelect the Content directory that contains your Xenia games.")
	contentDir = askdirectory(title="Xenia Content Directory")
	print(contentDir)
	if contentDir == "":
		inputHidden("\nAction cancelled. Press Enter to exit.")
		sys.exit()
	if not (path.isdir(contentDir) and path.basename(contentDir).lower() == "content"):
		inputHidden("\nInvalid folder path. Press Enter to exit.")
		sys.exit()
	contentDir = path.join(contentDir, "0000000000000000")
	if not path.isdir(contentDir):
		inputHidden("\nDirectory does not contain \"0000000000000000\" subfolder.\nInvalid folder path. Press Enter to exit.")
		sys.exit()

	print("\nCreating batch files...\n")
	numBatchFiles = 0
	duplicateCreated = False
	namesAndPaths = {}
	for root, dirs, files in walk(contentDir):
		for file in files:
			if path.basename(root).lower() in [
				"00007000", # Games On Demand
				"000d0000", # XBLA
				"00000002"  # Indie Games / Addons
				]:
				filePath = path.join(root, file)
				title = getTitleAtByte(filePath, titleByte)
				if title == "":
					continue
				if path.basename(root).lower() == "00000002":
					if title == "Indie Games":
						title = getTitleAtByte(filePath, addOnByte)
					else:
						continue
				print(filePath)
				print(title)
				# currBatPath = path.join(outputDir, slugify(title))
				# if path.exists(currBatPath+".bat"):
				# 	duplicateCreated = True
				# 	i = 1
				# 	while path.exists(currBatPath+" ("+str(i)+").bat"):
				# 		i += 1
				# 	currBatPath = currBatPath+" ("+str(i)+")"
				# currBatPath += ".bat"
				# createDir(outputDir)
				# with open(currBatPath, "w") as currBat:
				# 	currBat.write("\""+xeniaExe+"\" \""+filePath+"\"")
				title = slugify(title).strip("\'")
				if namesAndPaths.get(title) is None:
					namesAndPaths[title] = []
				namesAndPaths[title].append(filePath)
				print()
				numBatchFiles += 1
	for name in namesAndPaths.keys():
		if len(namesAndPaths[name]) == 1:
			currBatPath = path.join(outputDir, name+".bat")
			createDir(outputDir)
			with open(currBatPath, "w") as currBat:
				currBat.write("\""+xeniaExe+"\" \""+namesAndPaths[name][0]+"\"")
		else:
			for p in namesAndPaths[name]:
				oldTitle = name
				newTitle = getTitleAtByte(p, addOnByte)
				currBatPath = path.join(outputDir, newTitle)
				if path.exists(currBatPath+".bat"):
					duplicateCreated = True
					i = 1
					while path.exists(currBatPath+" ("+str(i)+").bat"):
						i += 1
					currBatPath = currBatPath+" ("+str(i)+")"
				currBatPath += ".bat"
				createDir(outputDir)
				if oldTitle != newTitle:
					newTitle = oldTitle+" - "+newTitle
					currBatPath = path.join(outputDir, newTitle+".bat")
					print("Duplicate \""+oldTitle+".bat\" found. Renaming to \""+newTitle+".bat\".")
				with open(currBatPath, "w") as currBat:
					currBat.write("\""+xeniaExe+"\" \""+p+"\"")

	print("Created "+str(numBatchFiles)+" batch files.")
	if duplicateCreated:
		print("\nAt least one game appears to have multiple batch files. Some of these may not link to the game's executable; try opening one, and if it doesn't work, simply try the next one.")
	inputHidden("\nPress Enter to exit.")

def getTitleAtByte(filePath, byteNum):
	with open(filePath, 'rb') as f:
		f.seek(byteNum)
		title = ""
		lastByteWasZero = False
		titleBytes = f.read(0x7F)
	for byte in titleBytes:
		if byte != 0:
			title += chr(byte)
			lastByteWasZero = False
		else:
			if lastByteWasZero: # reached end of title
				break
			else:
				lastByteWasZero = True
	return title

if __name__ == "__main__":
	main()