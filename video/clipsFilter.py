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
#!/usr/bin/env python3

#basic python module to filter grepped links and names
#reling on target video prev links, poster images, namesFile (lines like CLIP_ID/NAME)
#all files will be read and dictionary of CLIP_ID->name,prevLink,posterLink will be built
#post processing on this dict will handle desired filtering

#OUTPUT MODES
ID_NAME_MODE=0
PREV_LINK_MODE=1
POSTER_LINK_MODE=2
mode=PREV_LINK_MODE
PREFIX_GREP_CONFORT=""
class ClipData:
    def __init__(self,clipid,name):
        self.name=name
        self.id=clipid
        self.prevLink=""
        self.posterLink=""
    def __str__(self):
        if mode==ID_NAME_MODE:
            return self.id+"/"+self.name+"\n"+PREFIX_GREP_CONFORT+prevLink    #conform with id names file
        elif mode==PREV_LINK_MODE:
            return self.id+"/"+self.name+"\n"+PREFIX_GREP_CONFORT+self.prevLink
        elif mode==POSTER_LINK_MODE:
            return self.id+"/"+self.name+"\n"+PREFIX_GREP_CONFORT+self.posterLink
            
#TARGET DATA FROM CLIP4SALE NJjjjjjjjjjj
def readPrevLinks(filename,clipsDict,poster=False):
    #update in place dict of clips
    #poster flag to dicrimitate if filename is poster links file or prev links file list
    #prev links like https://imagecdn.clips4sale.com/accounts111/54509/clips_previews/prev_21596659.mp4
    #poster links like https://imagecdn.clips4sale.com/accounts99/54509/clip_images/previewlg_21596659.jpg
    
    f=open(filename)
    lines=f.readlines()
    f.close()
    
    for l in lines:
        targetRemoteFn=l.split("/")[-1]
        idIndexStart=targetRemoteFn.find("_")+1
        clipID=targetRemoteFn[idIndexStart:-5]   #get id after _ and before .mp4
        if poster:
            clipsDict[clipID].posterLink=l    #update field in place of clip in the dict 
        else:
            clipsDict[clipID].prevLink=l    #update field in place of clip in the dict 

def readClipFilenameID(filename):
    #read from pre processing of site curl filename containing row like clipID/clipName
    #return dict of clipID -> ClipData obj

    f=open(filename)
    lines=f.readlines()
    f.close()
    duplicatedIDs=0
    clipsDict=dict()
    for l in lines:
        idName=l.split("/")
        if clipsDict.get(idName[0])!=None:
            duplicatedIDs+=1
        #    print("duplicateClipID",l)
        clipsDict[idName[0]]=ClipData(idName[0],idName[1])
    print("duplicated IDs= ",duplicatedIDs)
    return clipsDict


def clipsDictFilter(clipsDict,excludingWordsList,PRINT_REMOVED=True):
    oldLen=len(clipsDict)
    print("filtering",excludingWordsList)
    filtered=0
    items=list(clipsDict.items())
    for id,clip in items:
        excluded=False
        for word in excludingWordsList:
            if word.upper() in clip.name.upper():
                excluded=True
                break
        if excluded:
            removed=clipsDict.pop(id)
            if PRINT_REMOVED: print("#",removed,clip.name)
            filtered+=1
    print("filtered",filtered,oldLen," out of ",len(clipsDict))


from sys import argv
if __name__=="__main__":
#    ID_NAMES_FILENAME="stilettoNamesALL.list"
#    PREV_LINK_FILENAME="stilettoLinksALL.list"
#    POSTER_LINK_FILENAME="posterLinksALL.list"
#    clipsDict=readClipFilenameID(ID_NAMES_FILENAME)
#    readPrevLinks(PREV_LINK_FILENAME,clipsDict)             #read preview links
#    readPrevLinks(POSTER_LINK_FILENAME,clipsDict,True)             #read poster Links
#    excludingWordsList=["sissi","cbt","cock","cuck","dick","suck","slut","bbc","whore","cum","fuck","ball","orgasm","virgin","chastity","daddy","handjob","orgasm"]
#    clipsDictFilter(clipsDict,excludingWordsList)
#    #printOut clips
#    for id,clip in clipsDict.items():
#        print(clip)
     
    if len(argv)<3: 
    	print("usage idNamesFilePath, pervLinksFilePath [posterLinkFilePath]")
    	exit(1)
    ID_NAMES_FILENAME=argv[1]
    PREV_LINK_FILENAME=argv[2]
    #POSTER_LINK_FILENAME=argv[3]
    clipsDict=readClipFilenameID(ID_NAMES_FILENAME)
    readPrevLinks(PREV_LINK_FILENAME,clipsDict)             #read preview links
    ##unfiltered ##
    #for id,clip in clipsDict.items():        print(clip)
    excludingWordsList=["4K","4k","SD","vr","eat","sissi","cbt","cock","cuck","dick","suck","slut","bbc","whore","vore","cum","fuck","ball","orgasm","virgin","chastity","daddy","handjob","orgasm"]
    clipsDictFilter(clipsDict,excludingWordsList)
    #printOut clips
    PREFIX_GREP_CONFORT="@"
    for id,clip in clipsDict.items():        print(clip)
