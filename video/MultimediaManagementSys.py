#!/usr/bin/python3
#Copyright Andrea Di Iorio
#This file is part of scripts
#scripts is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#scripts is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with scripts.  If not, see <http://www.gnu.org/licenses/>.
#!/usr/bin/env python2.7
#Multimedia management system

#ACTUAL STATUS:
#in Model is rappresented an abstract multimedia obj and basic load function, (from current dir take all filename matching extensions, and build MObjs)
#in GUI is rappresented the actual list of loaded MObj in a grid scrollable form 
#actually supported basic function as list and select a subset
#from all multimedial files, allow selection of a specific list of avaibles and output in out.list
from os import walk,path,environ
from sys import argv
import tkinter as tk 
from PIL import ImageTk, Image
from functools import partial
from json import load 
from random import shuffle

##############################################
#EXPORT TO OVVERRIDE OUTPUT
#VERBOSE		#full infos
#METADATA_VIDEO #video stream metadata only
verbose=environ.get("VERBOSE")
VERBOSE=verbose!=None and "T" in verbose.upper()

metadata=environ.get("METADATA_VIDEO")
METADATA=metadata!=None and "T" in metadata.upper()

realPath=environ.get("REAL_PATH")
REAL_PATH=realPath!=None and "T" in realPath.upper()
###############################################
FILTER_SIZE=1200*720
#############	MODEL  ##############
class MultimediaItem:
		def __init__(self,multimediaNameK):
				self.nameID=multimediaNameK	 #AS UNIQUE ID -> MULTIMEDIA NAME (no path and no suffix)
				self.pathName=""
				self.sizeB=0
				self.imgPath=""
				self.metadata=""	
				self.duration=0                 #num of secs for the duration
				self.extension=""
		def __str__(self):
				if VERBOSE: return "MultimediaOBJ\tname: "+self.nameID+" path: "+self.pathName+" size: "+str(self.sizeB)+" imgPath: "+self.imgPath+" metadata: "+str(self.metadata)+"\n"
				elif METADATA: return str(self.metadata["streams"][0])
				elif REAL_PATH: return self.pathName 
				#dflt ret basic infos
				return "MultimediaOBJ\t name: "+self.nameID+" path: "+self.pathName+" size bytes: "+str(self.sizeB)

#MULTIMEDIA FILES HANDLED EXTENSIONS
IMG_TUMBRL_EXTENSION="jpg"
VIDEO_MULTIMEDIA_EXTENSION="mp4"
METADATA_EXTENSION="json"
def parseMultimMetadata(fname):
		#parse ffprobe generated json metadata of fname file
		#return fileSize,streams array of dict metadata # that will have video stream as first
		fileMetadata=open(fname)
		metadata=load(fileMetadata)
		fileMetadata.close()
		fileSize=metadata["format"]["size"]
		streamsDictMetadata=metadata["streams"]
		#make sure video stream is at the first position in metadata.streams
		if len(streamsDictMetadata) > 1 and "video" in  streamsDictMetadata[1]["codec_type"]:
				streamsDictMetadata[0],streamsDictMetadata[1]=streamsDictMetadata[1],streamsDictMetadata[0]
		dur=streamsDictMetadata[0].get("duration","0")
		fileDur=float(dur)
		return fileSize,streamsDictMetadata,fileDur

def GetItems(rootPathStr="."):
		#scan for multimedia objs from rootPathStr recursivelly
		#will be builded multimedia obj for each founded multimedia file
		#first part of encountered multimedia files filenames is used as a key in multimediaItems dict
		#that dict hold for each identified multimedia object : fileKEY -> multimediaObj
		#return list of Multimedia Obj items from current dir content 
		multimediaItems=dict()  #filenameNOSUFFIX -> MultimediaObj
		for root, directories, filenames in walk(rootPathStr):
				#print(root,"\t",directories,"\t",filenames)
				#pathName=path.join(path.abspath(root),filename)
				for filename in filenames:
						tumbrl=""
						metadata=""					 #ffprobe strams list of parsed metadata as dict
						name=filename[:filename.find(".")]
						lastSuffix=filename[-5:]		#take .mp4 .jpg .json last suffix
						extension=lastSuffix[lastSuffix.find("."):]
						#print("lastSuffix founded in ",filename," is: ",lastSuffix)

						#init multimedia item obj if not already did
						item=multimediaItems.get(name)
						if item==None:
								item=MultimediaItem(name)
								multimediaItems[name]=item
						#different cases on file in processing img,metadata,
						#set needed field in accord on file in processing
						fpath=path.join(path.abspath(root),filename)
						if IMG_TUMBRL_EXTENSION in lastSuffix:
								item.imgPath=fpath

						elif METADATA_EXTENSION in lastSuffix:
								try:item.sizeB,item.metadata,item.duration=parseMultimMetadata(fpath) #skip bad/not fully formatted jsons
								except:print("badJsonFormat at ",fpath)
						# elif VIDEO_MULTIMEDIA_EXTENSION in lastSuffix:
						else:	#take all possible other extension as video multimedia extension
								item.pathName=path.join(path.abspath(root),filename)
								item.extension=extension
				#break  #TODO NOT RECURSIVE SCANN
		return multimediaItems

def _printList(l):
		for i in l:
				print(i)


		

#############	GUI	###################
#sample function -- MMSYS SELCTION
selectedList=list()
lastSelected=""
def _select(selected):
		if len(selectedList)>0 and selectedList[-1]==selected:
			selectedList.pop()
			print("DEL:",selected,"removed")
		else:selectedList.append(selected)


WrittenFiles=0
BASE_FLUSH_FNAME="multimItemsSelected_"
LINE_HEADER="File\t"
LOG_SELECTED_TO_FILE=environ.get("LOG_SELECTED_TO_FILE")!=None and "T" in environ["LOG_SELECTED_TO_FILE"].upper()
def _printMItems(selected=selectedList):
		cumulativeSize=0
		lines=list()
		for i in selected:
				print(i.pathName,"\t\t ",int(i.sizeB)/2**20," MB")
				lines.append(LINE_HEADER+i.pathName)
				cumulativeSize+=int(i.sizeB)
		if LOG_SELECTED_TO_FILE:
			f=open(BASE_FLUSH_FNAME+str(WrittenFiles)+".list","w")
			f.writelines(lines)
			WrittenFiles+=1
			f.close()

		print("CUMULATIVE SIZE:\t",int(cumulativeSize)/2**20," MB")
		_cleanSelectedGlbl()
def _saveSelected(selected,outName="choiced.list"):
		outF=Open(outName,"w")
		outlist=list()
		for s in selected:
				outlist.append(s.pathName)
		outF.write("\n".join(outlist))
		outF.close()
		print("saved: ",len(selected))

def _cleanSelectedGlbl(sList=selectedList):
		sList.clear()

class VerticalScrolledFrame(tk.Frame):
		"""A pure Tkinter scrollable frame that actually works!
		* Use the 'interior' attribute to place widgets inside the scrollable frame
		* Construct and pack/place/grid normally
		* This frame only allows vertical scrolling
		"""
		def __init__(self, parent, *args, **kw):
				tk.Frame.__init__(self, parent, *args, **kw)					

				# create a canvas object and a vertical scrollbar for scrolling it
				vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
				vscrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=tk.FALSE)
				canvas = tk.Canvas(self, bd=0, highlightthickness=0,height=999,yscrollcommand=vscrollbar.set)
				#canvas.configure(scrollregion=canvas.bbox("all"))
				canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.TRUE)
				vscrollbar.config(command=canvas.yview)
				# reset the view
				canvas.xview_moveto(0)
				canvas.yview_moveto(0)

				# create a frame inside the canvas which will be scrolled with it
				self.interior = interior = tk.Frame(canvas)
				##TODO #self.interior.bind("<MouseWheel>", self.OnMouseWheel)
				interior_id = canvas.create_window(0, 0, window=interior,anchor=tk.NW)

				# track changes to the canvas and frame width and sync them,
				# also updating the scrollbar
				def _configure_interior(event):
						# update the scrollbars to match the size of the inner frame
						size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
						canvas.config(scrollregion="0 0 %s %s" % size)
						if interior.winfo_reqwidth() != canvas.winfo_width():
								# update the canvas's width to fit the inner frame
								canvas.config(width=interior.winfo_reqwidth())

				interior.bind('<Configure>', _configure_interior)

				def _configure_canvas(event):
						if interior.winfo_reqwidth() != canvas.winfo_width():
								# update the inner frame's width to fill the canvas
								canvas.itemconfigure(interior_id, width=canvas.winfo_width())
				canvas.bind('<Configure>', _configure_canvas)
				

ITEMS_LIMIT=256
pageN=-1
scframe=None
def _nextPage(nextItems=None):
		global pageN,items
		if nextItems==None: nextItems=items
		pageN+=1
		if pageN > len(items)/ITEMS_LIMIT: pageN=0	  #circular next page
		print(pageN)
		nextPage.configure(text="nextPage: "+str(pageN))
		drawItems(nextItems,ITEMS_LIMIT*pageN,ITEMS_LIMIT,True,FILTER_SIZE)

_computeSize=lambda itemStreamList: int(itemStreamList[0]["width"])*int(itemStreamList[0]["height"])
def drawItems(items,itemsStart=0,itemsToDrawLimit=ITEMS_LIMIT,FILTER_PATH_NULL=False,filterSize=0):
		global root,scframe
		global btns,imgs
		if scframe!=None:
				scframe.grid_forget()
				scframe.destroy()
		scframe = VerticalScrolledFrame(root)
		scframe.grid()
		btns=list()
		imgs=list()
		row=col=i=0
		colSize=3
		lastSelected=""
		for mitem in items[itemsStart:itemsStart+itemsToDrawLimit]:
				print(mitem.nameID,mitem.imgPath,row,col,i)
				funcTmp= partial(_select,mitem)
				try: itemSize=_computeSize(mitem.metadata)
				except: itemSize=filterSize 
				if mitem.imgPath!="" and (mitem.pathName!="" or FILTER_PATH_NULL==False) and itemSize>=filterSize :
						try:
								tumbrl= ImageTk.PhotoImage(Image.open(mitem.imgPath))
						except:
								print(mitem.imgPath,"!!!!!!!!!!!!")
								continue
						imgs.append(tumbrl)
						btn=tk.Button(scframe.interior,image=tumbrl,command=funcTmp,borderwidth=5)
				else:
						print("skipped:\t",mitem)
						continue

				if col >= colSize:
						col=0
						row+=1
				btns.append(btn)
				btn.grid(row=row,column=col)
				col+=1
				
				i+=1

		root.mainloop() 

def IntersectItemsAndFilenames(items,filenames):
		intersectedItems=list()
		for fn in filenames:
				for i in items:
						if i.nameID in fn:	  #matching remoteFilename == item i
								intersectedItems.append(i)
		return intersectedItems

def guiMinimalStart(startItems):
		global nextPage,items,root
		items=startItems
		root = tk.Tk()
		#root.resizable(True,True)
		nextPage=tk.Button(root,command=_nextPage,text="nextPage",background="yellow")
		nextPage.grid(row=0,column=0)
		flushBtn=tk.Button(root,command=_printMItems,text="printSelectedMItems",background="green")
		flushBtn.grid(row=1,column=0)
		shuffle(items)
		#for i in items: print(i.imgPath)
		_nextPage()

if __name__=="__main__":
		#get filenames from FILENAME.LIST
		global items,i
		_itemsDict=GetItems()
		_items=list(_itemsDict.values())
		items=_items
		if len(argv)>1:
				print("Usage [ namesList to show only ]")
				filterList=open(argv[1])
				nameOnly=list() #will old name filtered from given file[path] list
				for l in filterList.readlines():
						name=l.split("/")[-1]
						nameOnly.append(name[:n.find(".")])
				items=list()
				for i in _items: 
						if i.name in nameOnly: items.append(i)
		#	   items=i
		#else:
		#	   filenames=open(INPUT_FILENAME).readlines()
		#	   items=IntersectItemsAndFilenames(i,filenames)   #filter from all avaible items, the ones that nameKey is in one input filename
		
		#_printList(items)
		#print("targetItemsLen,allAvaibleItemsTumbrlsLen,inputFilenamesLen",len(items),len(i),len(filenames))
		


		#GUI MINIMAL START
		root = tk.Tk()
		#root.resizable(True,True)
		global nextPage
		nextPage=tk.Button(root,command=_nextPage,text="nextPage",background="yellow")
		nextPage.grid(row=0,column=0)
		flushBtn=tk.Button(root,command=_printMItems,text="printSelectedMItems",background="green").grid(row=1,column=0)
		shuffle(items)
		#for i in items: print(i.imgPath)
		_nextPage()
