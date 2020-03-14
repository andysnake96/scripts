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
import os 
from json import load
from os import environ as env   #EXPORT DIFFERENT START REC SEARCH WITH START_SEARCH
############# 
"""
ENV OVERRIDE OPTION
START_SEARCH --> FIRST DIR FOR SEARCH
CONCAT_FILELIST_FNAME -> NUM OF ON THE FLY FFMPEG CMD
"""
###
env["REAL_PATH"]="True" #will export print mode correctly

FFmpegNvidiaAwareBuildPath="~/ffmpeg/bin/ffmpeg_nv"
FFmpegBasePath="~/ffmpeg/bin/ffmpeg"
#ffprobe -v quiet -print_format json -show_format -show_streams $1 > $1.json
from MultimediaManagementSys import *
from random import random,randint
def scanFilesRecoursivelly(rootPathStr=".",targetExtensions=["json","info"]): #TODO OLD 
    #scan recoursivelly for file that their filename match some defined extension suffix
    targetsPaths=list() 
    for root, directories, filenames in os.walk(rootPathStr):
        #print(root,"\t",directories,"\t",filenames)
        
        for f in filenames:
            for ext in targetExtensions: 
                if ext in f[-5:]: targetsPaths.append(os.path.join(os.path.abspath(root),f))
    return targetsPaths

_getVideoStreamDictFromPath=lambda fpath: load(open(fpath))["streams"][0]
def flexibleGroupByFields(multimediaItems,groupKeysList,EXCLUDE_ON_KEYLIST=False,EXCLUDE_WILDCARD=True):
    #group multimedia metadata in on the base of their value on a given list of common fileds expressed in groupKeysList
    #if EXCLUDE_ON_KEYLIST is true the groupping will be based on values of all fields not in groupKeysList 
    #so groupKeysList  will act as a black list actually
        #returned dict of [grouppingKeys]-->[videoInGroup0MultimediaItem,video1MultimediaItem,....]

    groupsDict=dict()   #dict (valueOfK_0,...,valueOfK_N) -> LIST Files with this metadata values groupped
    groupKeysList.sort()
    for item in multimediaItems:
        fMetadata=item.metadata[0]  #get video stream of multimedia obj.metadata
        fMetadataValues=list()  #list of values associated to groupKeysList for the target groupping of files
        fKeysAll=list(fMetadata.keys())
        fKeysAll.sort()
        for k in fKeysAll:
            if EXCLUDE_ON_KEYLIST:  #the given groupKeysList is a black list
                if EXCLUDE_WILDCARD:    #blackList will be used has a pattern to exclude actual f metadata keys
                    kInExcludeList=False
                    for kEx in groupKeysList:
                        if kEx in k:
                            kInExcludeList=True
                            break
                    if kInExcludeList==False:fMetadataValues.append((k,fMetadata[k]))
                else:
                    if k not in groupKeysList: fMetadataValues.append((k,fMetadata[k]))
            else:
                if k in groupKeysList: fMetadataValues.append((k,fMetadata[k]))
        groupK=tuple(fMetadataValues)
        try:    #avoid unhashable contained types??
            if groupsDict.get(groupK)==None: groupsDict[groupK]=list()  #create a new list for target values of groupKeysList
        except: continue
        #finally append to target group list the processed file
        groupsDict[groupK].append(item)
    return groupsDict

#rand segment cutting from item
#cutting constr specification
MODE_DURATION="MODE_DURATION" #time identified as floating point in (0,1) as a proportion of the full time of the mItem
MODE_ABSTIME="MODE_ABSTIME"   #time points specified as num of second
def genVideoCutSegmentsRnd(mItem,minSegLen,maxSegLen,maxSegN=1,minStartConstr=-1,maxEndConstr=None,mode=MODE_DURATION,MORE_SEGN_THREASHOLD_DUR_SEC=596,ROUND_INT_START_SEEK=True):
    """generate random segment identified by start/end point in abs time in seconds returned as [(s1Start,s1End),(s2Start,s2End),...]
    minStartConstr maxEndConstr identify respectivelly constraint in start/end for the segments
    maxEndConstr may be specified as an absolute end time (as a positive num) or as a negative time, the abs will be subtracted to target duration of mItem
    mode specify how this costraint and min/maxSegLen has to be interpreted (see above constants documentation=
    multiple segment will be allocated in different portions, not overlapped if parameter expressed correctly
    enable more likelly max SEG N alloc on long item if duration is above MORE_SEGN_THREASHOLD_DUR_SEC
    if MORE_SEGN_THREASHOLD_DUR_SEC is 0 the segN will be selected random uniformly
    """

    duration=mItem.duration
    if maxEndConstr!=None:  
        if maxEndConstr>0 and maxEndConstr < duration: duration=maxEndConstr
        elif maxEndConstr<0: duration+=maxEndConstr #subtrack maxEndConstr from duration
    if MORE_SEGN_THREASHOLD_DUR_SEC>0 and duration>=MORE_SEGN_THREASHOLD_DUR_SEC:
        # GEN SEGMENT WITH RAND EXTRACTION x IN 01 --> i if x in [i *segRangeProp01,(i+1)*segRangeProp01)
        # if duration is above MORE_SEGN_THREASHOLD => extraction 1 is reduced to fixed 5% and maxSegN is enhanced to 77%, remaining proportional
        extraction=random()
        nSeg=0
        if extraction <.05: nSeg=1
        elif extraction>.77:nSeg=maxSegN
        else:
            st,end=.05,.77
            segN=1
            segRangeProp01=(.77-.05)/(maxSegN-2)
            while st<=end:
                if st<=extraction and extraction < st+segRangeProp01:
                    nSeg=segN
                    break
                #update segN decision vars
                st+=segRangeProp01
                nSeg+=1
    else:   nSeg=randint(1,maxSegN)         #basic rand seg N decision else
    ## N SEG OBTAINED

    outSegs=list()  #list of [(startSegSec,endSegSec),...]
    segmentSlotLen=float(duration)/nSeg
    segmentSlotLenTotProportion=segmentSlotLen/duration
    start=max(0,minStartConstr) #base time for start slot time generation
    for x in range(nSeg): #segment times genration in different slots NB minMax SegLen has to be setted correctly
        ## MODE_ABSTIME
        segLen=(random()*(maxSegLen-minSegLen))+minSegLen
        segStart=start+random()*(segmentSlotLen-segLen) #actual start for segment random placed in the whole avaible space inside the curr slot
        ## MODE_DURATION
        if mode==MODE_DURATION:
            start-=x*segmentSlotLen #revert MODE_ABSTIME mod on seg base start
            start+=x*segmentSlotLenTotProportion
            segStart=duration*(start+random()*(segmentSlotLenTotProportion-segLen))
            segLen*=duration
        ###alloc generated segment
        if ROUND_INT_START_SEEK:
            segStart=int(segStart)
        outSegs.append((segStart,segStart+segLen))
        start=x*segmentSlotLen          #start for the next iteration
    return outSegs

import turtle

def _debug_graph_turtle_segments(itemSegmentList,SCREEN_W=700,EXTRA_WIDTH_STRINGS=500,SEGS_FNAME="segments.eps"):
    #draw a new line on canva with in black item duration in green segment allocated
    #each new line will be drawn down of 2 unit
    #the size of each line will be proportional to corresponding element normalized to the longest item

    sc=turtle.Screen()
    turtle.tracer(0, 0)
    LINE_WIDTH=15
    SCREEN_H=len(itemSegmentList*LINE_WIDTH)+22
    FONT=("Arial",6,"normal")
    sc.setup(SCREEN_W,len(itemSegmentList)*LINE_WIDTH)
    sc.setworldcoordinates(0,0,SCREEN_W+EXTRA_WIDTH_STRINGS,SCREEN_H)
    END_X=SCREEN_W+EXTRA_WIDTH_STRINGS
    turtle.setpos(0,SCREEN_H-10)
    turtle.speed(0)
    durs=list()
    for i,s in itemSegmentList:
        durs.append(i.duration)
    maxDur=max(durs)
    turtle.up()
    for item,segs in itemSegmentList:
        turtle.down()
        pos=turtle.pos()
        turtle.color("black")
        turtle.width(1)
        turtle.forward((item.duration/maxDur)*SCREEN_W) #duration
        turtle.setpos(pos)
        turtle.color("green")
        turtle.width(3)
        for s in segs:
            turtle.up()
            turtle.setpos(pos)
            turtle.forward((((s[0])/maxDur)*SCREEN_W))         #seek to segment start
            turtle.down()
            turtle.forward(((s[1]-s[0])/maxDur)*SCREEN_W)    #draw segment
        #move down for next line
        turtle.up()
        if EXTRA_WIDTH_STRINGS>0:
            turtle.setpos(pos)
            turtle.forward((item.duration/maxDur)*SCREEN_W+20) #duration
            #draw a dotted line until END
            turtle.color("black")
            DOT_STEP=50
            turtle.width(1)
            while turtle.pos()[0]<END_X:
                turtle.forward(DOT_STEP)
                turtle.dot(1)
            turtle.setx(END_X)
            turtle.write(str(item.duration)+" - "+str(segs),False,"right",FONT)
        turtle.setpos(pos)
        turtle.sety(pos[1]-LINE_WIDTH)
    #save rappresentation of  segments generated and freeze image
    turtle.getscreen().getcanvas().postscript(file=SEGS_FNAME)
    turtle.done()
    turtle.update()
    input()


buildFFMPEG_segExtract=lambda pathName,segStart,segTo,destPath:FFmpegBasePath+" -i "+pathName+" -ss "+str(segStart)+" -to "+str(segTo)+" -c copy "+destPath
buildFFMPEG_segExtract_reencode=lambda pathName,segStart,segTo,destPath:FFmpegNvidiaAwareBuildPath+" -ss "+str(segStart)+" -to "+str(segTo)+" -i '"+pathName+"' -c:v h264_nvenc  "+destPath
def _concatFilterInputStr(numInputs): 
    outStr=""
    for x in range(numInputs): outStr+="["+str(x)+"]"
    return outStr

BASH_NEWLINE_CONTINUE="\\\n"
def concatFilterCmd(itemSegsList,outFname="out.mp4",ffmpegBinShellPath="ffmpeg",ONTHEFLY_PIPE=True,PIPE_FORMAT="matroska",MULTILINE_OUT=True):
    #itemSegsList: [(itemObj,[(seg0Start,seg0End),...]),...]
    outStrCmd=ffmpegBinShellPath
    inputFileSeekedList=list()  # list of subStr for input file segmentized by -ss-to
    numInputs=len(itemSegsList)
    for item,segs in itemSegsList: #filePath0,[segs...]
        for seg in segs:
            inputFileSeekedList.append("\t-ss "+str(seg[0])+" -to "+str(seg[1])+" -i '"+item.pathName+"'\t")
            #if MULTILINE_OUT: outStrCmd+='\\'+'\n'           #multiline cmd
    shuffle(inputFileSeekedList)    #shuf segment list as input operand
    outStrCmd+=BASH_NEWLINE_CONTINUE.join(inputFileSeekedList) #join in segment shuffled with as prefix \+\n
    outStrCmd+=' -filter_complex "'+_concatFilterInputStr(numInputs)+"concat=n="+str(numInputs)+':v=1:a=1"'
    outStrCmd+=" -vsync 2"
    targetOutput=" "+outFname
    if ONTHEFLY_PIPE: targetOutput=" -f "+PIPE_FORMAT+" - | ffplay - " #on the fly generate and play with ffplay
    outStrCmd+=targetOutput
    return outStrCmd
        
        

CONCURRENCY_LEVEL_FFMPEG_BUILD_SEGS=3
if env.get("CONCURRENCY_LEVEL_FFMPEG_BUILD_SEGS")!=None: CONCURRENCY_LEVEL_FFMPEG_BUILD_SEGS=int(env["CONCURRENCY_LEVEL_FFMPEG_BUILD_SEGS"])
def ffmpegConcatFilterbatchGen(itemsList,BASH_BATCH_SEGS_GEN="genSegsConcatFilter.sh",CONCAT_FILELIST_FNAME="concat.list"):
    #print ffmpeg cut cmd for a group of concat compatible videos in itemsList 
    #output will be setted to be written in tmpCut/itemNameID folder
    itemSegmentsList=list()
    trgtSegsList=list()
    trgtDirsList=list()
    ffmpegSegBuildCmds=list()
    i=0
    for item in itemsList:
        if item.pathName=="": continue  #skip not sync.ed metadata/files
        itemName=item.pathName.split("/")[-1]
        
        #############   SEGs GENERATION     #############################################
        # segs=genVideoCutSegmentsRnd(item,0.2,0.30,maxSegN=2,minStartConstr=.088,mode=MODE_DURATION)
        segs=genVideoCutSegmentsRnd(item,4,7,maxSegN=3,minStartConstr=7,maxEndConstr=-6,mode=MODE_ABSTIME)
        ##########################################
        itemSegmentsList.append((item,segs))
        #TODO DEBUG SEG GENERATION ONLY
        print(segs,item.duration)                
        concatFilterCmdStr=concatFilterCmd(itemSegmentsList)
        bashBatchSegGen=open(BASH_BATCH_SEGS_GEN,"w")
        bashBatchSegGen.write("#~/ffmpeg/bin/ffmpeg_nv\n")
        bashBatchSegGen.write(concatFilterCmdStr)
        bashBatchSegGen.close()


def ffmpegConcatBatchGen_cutReencoding_and_concatReencodingLess(itemsList,segsLenSec=4,BASH_BATCH_SEGS_GEN="genSegs.sh",CONCAT_FILELIST_FNAME="concat.list"):
    #print ffmpeg cut cmd for a group of concat compatible videos in itemsList 
    #output will be setted to be written in tmpCut/itemNameID folder
    itemSegmentsList=list()
    trgtSegsList=list()
    trgtDirsList=list()
    ffmpegSegBuildCmds=list()
    i=0
    for item in itemsList:
        skipItem=True  
        try:skipItem = item.pathName=="" or os.path.getsize(item.pathName)==0
        except: continue
        if skipItem: continue
        itemName=item.pathName.split("/")[-1]
        
        #############   SEGs GENERATION     #############################################
        # segs=genVideoCutSegmentsRnd(item,0.2,0.30,maxSegN=2,minStartConstr=.088,mode=MODE_DURATION)
        segs=genVideoCutSegmentsRnd(item,segsLenSec,segsLenSec,maxSegN=4,minStartConstr=7,maxEndConstr=-6,mode=MODE_ABSTIME)
        ##########################################
        itemSegmentsList.append((item,segs))
        #TODO DEBUG SEG GENERATION ONLY
        print(segs,item.duration)
        trgtDir="tmpCut/"+item.nameID
        trgtDirsList.append("mkdir '"+trgtDir+"'\n")
        for s in range(len(segs)):
            trgtSegDestPathName=trgtDir+"/"+str(s)+item.extension
            trgtSegsList.append("file\t"+trgtSegDestPathName+"\n")
            # print("@ ffmpeg -i ",item.pathName," -ss ",segs[s][0]," -to ",segs[s][1],"-c copy ",trgtSegDestPathName,"\t ___totDuration ",item.duration)
            ffmpegSegBuildCmds.append(buildFFMPEG_segExtract_reencode(item.pathName,segs[s][0],segs[s][1],trgtSegDestPathName)+" &\n")
            #interleave build cmd with wait to concurrency build fixed num of vids
            if i%CONCURRENCY_LEVEL_FFMPEG_BUILD_SEGS==0:  ffmpegSegBuildCmds.append("wait\n")    
            i+=1
            #print(ffmpegSegBuildCmds[-1])
        #write bash ffmpeg build segs
        bashBatchSegGen=open(BASH_BATCH_SEGS_GEN,"w")
        bashBatchSegGen.write("mkdir tmpCut\n")
        bashBatchSegGen.writelines(trgtDirsList)        #write dirs to make
        bashBatchSegGen.writelines(ffmpegSegBuildCmds)  #write ffmpeg cmds
        bashBatchSegGen.write("\nwait\necho DONE")                 #wait concurrent ffmpeg seg builds
        #write output segment file list
        file=open(CONCAT_FILELIST_FNAME,"w")
        shuffle(trgtSegsList)
        file.writelines(trgtSegsList)
        file.close()


    #_debug_graph_turtle_segments(itemSegmentsList)


if __name__=="__main__":
    TAKE_ALL=True
    startPath="/home/andysnake/DATA2/all/all"
    if env.get("START_SEARCH")!=None: startPath=env["START_SEARCH"]
    mItemsDict=GetItems(startPath)
    #filter list of videos metadata for groupping by common fields
    metadataItems=list()    #multimedia objs that have a defined metadata field
    for v in mItemsDict.values():
        if v.metadata!="":
            metadataItems.append(v)
    #GROUP KEYS--------------------------
    groupKeys=["width","height"]
    #ECLUDE KEYS-------------------------
    #excludeGroupKeys=["bit_rate","nb_frames","tags","disposition","avg_frame_rate","color","index"]
    excludeGroupKeys=["duration","bit_rate","nb_frames","tags","disposition","avg_frame_rate","color"]
    #excludeGroupKeys=["rate","tags","disposition","color","index","refs"]
    grouppings=flexibleGroupByFields(metadataItems,excludeGroupKeys,EXCLUDE_ON_KEYLIST=True,EXCLUDE_WILDCARD=True)
    #grouppings=flexibleGroupByFields(metadataItems,excludeGroupKeys,EXCLUDE_ON_KEYLIST=True,EXCLUDE_WILDCARD=True)

    i=0
    itemsGroupped=list(grouppings.items())
    itemsGroupped.sort(key=lambda x:len(x[1]))
    itemsGroupped.reverse()
    print(len(grouppings),len(metadataItems))
    for k,v in itemsGroupped:
        print("GRUOP ",i)
        print(k," --> ",len(v),"\n\n")
        for item in v:         print(i,"\tfile\t",item)
        i+=1
    #CHOICE TARGET GROUPPABLE ITEMS FOR SEGMENT GENERATION  WITH GUI MMSYS
    global selectedList
    if TAKE_ALL: #take all in most popolous group
        selectedList=itemsGroupped[0][1]   
    else:
        guiMinimalStart(itemsGroupped[0][1])

    shuffle(selectedList)
    #ffmpegConcatFilterbatchGen(selectedList[:40])
    ffmpegConcatBatchGen_cutReencoding_and_concatReencodingLess(selectedList[:32],5)
