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
from sys import argv
from re import findall

#target of module is to group video by almost same encoding params so they can be processed togeter avoiding re encoding
#e.g. concat filter

#parse ffprobe metadata file 
#create ffprobe metadata file 
#find -iname "*mp4"  | xargs -n 1 -I "%" sh -c 'echo -ne "%\t\t"  && ffprobe % 2>&1 | grep "Video: " && echo -ne "\t\t" && ffprobe -loglevel error -show_entries stream=time_base -select_streams v:0 -of csv=p=0 % 2>&1'  > a

#for x in $(find -iname "*prev*");do echo -n -e "$x\t\t"; ffprobe -loglevel error -show_entries stream=time_base -select_streams v:0 -of csv=p=0 $x;done > a

##find -iname "*mp4"  | xargs -n 1 -I "%" sh -c 'echo -ne "%\t\t"  && ffprobe % 2>&1 | grep "Video: "'
###find -iname "*mp4"  | xargs -n 1 -I "%" sh -c 'echo -ne "%\t\t"  && ffprobe % && echo -ne "\t\t" && ffprobe -loglevel error -show_entries stream=time_base -select_streams v:0 -of csv=p=0 % 2>&1 | grep "Video: "'
#lines like -> ./640X360/prev_22059533.mp4		    Stream #20:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 640x360 [SAR 1:1 DAR 16:9], 541 kb/s, 25 fps, 25 tbr, 12800 tbn, 50 tbc (default)

#get identifing encoding infos...
def getffprobedStreamEncodingKey0(streamSting):
    #extract stream key for a video described from ffprobe video stream grepped streamSting
    #simbly truncate the stream infos up to last colon before kb/s
    print(streamSting)
    kbsField=findall(", [0-9]+ kb/s",streamSting)[0]
    kbsFieldStartIndx=streamSting.find(kbsField)
    return streamSting[:kbsFieldStartIndx]

def getStreamSize(streamSting):
    #extract video size from stream infos
    size=findall("[0-9]{3,4}x[0-9]+",streamSting)[0]
    return size

if len(argv) < 2:
    print("usage ffprobe filename like filePath\t\tvideoStream")

SEPARATOR="\t\t"
metadataFile=open(argv[1])
metadataLines=metadataFile.readlines()
metadataFile.close()

encoedStreamVideoDict=dict() #create a dict to separe different encoded video from each others by stream size format ...
i=0
print("@@",i)
for line in metadataLines:
    lineFields=line.split(SEPARATOR)
    fname=lineFields[0]
    fStreamMetadata=lineFields[1]
    #fsize=getStreamSize(fStreamMetadata)
    ##fEncodingFullInfos=getffprobedStreamEncodingKey0(fStreamMetadata)
    #out of cmd: ffprobe -loglevel error -show_entries stream=time_base -select_streams v:0 -of csv=p=0 $x;done > a    
    fEncodingFullInfos=fStreamMetadata

    if encoedStreamVideoDict.get(fEncodingFullInfos)==None:   #eventually create a new key in dict if not already done for actual size
        i+=1
        encoedStreamVideoDict[fEncodingFullInfos]=list()
    encoedStreamVideoDict[fEncodingFullInfos].append(fname)
    print("@@",i,fname)
    

#outAput dict in stdout
print("$$$$$$$$$$$")
for size,fnames in encoedStreamVideoDict.items():
    print(size.upper())
    for fname in fnames:
        print(size,"-",fname)

print(len(encoedStreamVideoDict))
