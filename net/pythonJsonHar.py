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
from json import load
from base64 import b64decode
from sys import argv

EXTENSION_IMAGE=".jpg" #extension in grepped and decoded base64 from firefox har
EXTENSION_VIDEO=".mp4"
OutputFilenameID=0
def parseHarFirefox(harFileName,Urls=dict()):
	#parse firefox har json decoding base64 fields reading harFileName
	#Urls is a dict used to keep last part of url of content in Hashmap so quick duplicate filter is implemented
	global OutputFilenameID
	print(len(Urls))
	f=open(harFileName)
	harParsed=load(f)
	f.close()
	base64GreppedImage=list()
	base64GreppedVideo=list()
	entries=harParsed['log']['entries']
	for e in entries:
		respData=e['response']['content']
		url=e["request"]["url"]
		url=url.split("/")[-1]	#take just the last part of url (skip eventual cdn replica selection :)
		#avoid http arg added eventually by content provider in filtering dups
		httpArgStrIndx=url.find("?")
		if httpArgStrIndx > 0: url=url[:httpArgStrIndx]
		##try: url=url[:url.index("?")]	#avoid http arg added eventually by content provider
		if Urls.get(url) != None: 			#SKIP DUP
			print("SKIP ",url)
			continue 
		if respData['mimeType']=="image/jpeg":
			base64GreppedImage.append(respData['text']) 
			Urls[url]=True
		elif respData['mimeType']=="video/mp4": 
			base64GreppedVideo.append(respData['text']) 
			Urls[url]=True
	
	#serialize
	return
	for i in range(len(base64GreppedImage)):
		f=open(str(i+OutputFilenameID)+EXTENSION_IMAGE,"wb")
		f.write(b64decode(base64GreppedImage[i]))
		f.close()
	
	for i in range(len(base64GreppedVideo)):
		f=open(str(i+OutputFilenameID)+EXTENSION_VIDEO,"wb")
		f.write(b64decode(base64GreppedVideo[i]))
		f.close()
	OutputFilenameID+=max(len(base64GreppedVideo),len(base64GreppedImage))

if __name__=="__main__":
	if len(argv)<1:
		print("usage har0Fname [,har1Fname,....] ")
		exit()
	dupFilterUrls=dict()
	for harFname in argv[1:]:
		parseHarFirefox(harFname,dupFilterUrls)
	#urls=list(dupFilterUrls.keys())
	#urls.sort()
	#for u in urls:print(u)
