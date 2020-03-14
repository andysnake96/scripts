#!/usr/bin/bash
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
#!/usr/bin/bash
#script to get all PAGES of a given site simply modifing page num url by bash string substitution
#pages will be downloaded in file named progressivelly named ->download started in parallel by & over function containing curl call
#download handled by curl with prepared(commentted) grep regex filter to get content urls inside page directly
echo "usage [[URL_100_xPG,NAME,PAGENUM],...]"
CLIPS_FILTER_PATH="/home/andysnake/DATA2/clipSale/scripts/clipsFilter.py"
#args passed in 3tuples that will be separated and handled in parallel
get_pages(){
	
    PAGE_PATTERN_START="Page1"
    FILTER_CMD1="grep -o http.*\\.gif"
    FILTER_CMD2="pcregrep  --buffer-size 99999 -o1 href=\"/studio/[0-9]+/([0-9]+/.*)\""
    FILTER_CMD3='pcregrep   --buffer-size 99999 -o1 poster=\"(.*jpg)\"'
    FILTER_CMD="grep  -e http.*\\.mp4 -e \"data-clipid\""
    #####	try to use passed arguments as args
    #args=("$@");
    #url=${args[0]}
    #pagenum=${args[2]}
    #nameBase=${args[1]}
    #direct=${args[3]}
    ########	direct binding passed arguments
    url=$1
    nameBase=$2
    pagenum=$3
    echo passed url: $url numPages: $pagenum nameBase: $nameBase directLinksGrep: $direct
    mkdir $nameBase"PREVS"
    cd $nameBase"PREVS"
    mkdir fullPage
    mkdir links
    #get all pages
    for n in $(seq 1 $pagenum); do
        pageReplacer="Page"$n
        url=${url/$PAGE_PATTERN_START/$pageReplacer} #URL of page to download obtained by bash string substitution of pagenum
	PAGE_PATTERN_START=$pageReplacer
        echo $url  "<--->"  $pageReplacer
	#download page and grep it
        cd fullPage && curl --silent $url > $nameBase"fullPage"$pageReplacer &
        cd links && curl --silent $url | $FILTER_CMD1 > $nameBase"linksVideo"$pageReplacer &
        cd links && curl --silent $url | $FILTER_CMD2 > $nameBase"clipNames"$pageReplacer &
        cd links && curl --silent $url | $FILTER_CMD3 > $nameBase"linksPoster"$pageReplacer &
        echo "DONE"$n
    done;
    wait
    cat links/$nameBase"clipNames"* > names.list
    cat links/$nameBase"linksVideo"* > links.list
    cat links/$nameBase"linksPoster"* > poster.list
    python3 $CLIPS_FILTER_PATH names.list links.list > filteredClips.list_raw
}


##  generate a list of args tuplized to progressivelly pass

#echo back arguments
#set -e 	#EXIT AT FIRST ERROR NOT SKIPPED
argc="$#";
args="$@";
echo $argc arguments passed##capsulize args
argsList=""
argsListTmp=("")
tupleSize=3
for((x=0;x< $(($#/$tupleSize)); x++))
do
	argsListTmp=(  ${args[$(( $x*$tupleSize ))]} ${args[$(( $x*$tupleSize+1 ))]} ${args[$(( $x*$tupleSize+2 ))]} ${args[$(( $x*$tupleSize+3 ))]} )
	echo ${argsListTmp[@]}
	argsList+=${argsListTmp[@]}	
	###	DOWNLOAD	#############
	get_pages ${argsListTmp[@]} &	
done

wait






#id of clip in clip4sale generic page...
#<a href="/studio/31813/21710217/We%27re+All+Going+To+Sit+On+You%21++Part+11+SD" class="clipTitleLink" data-method="getClip" data-clipid="21710217">We're All Going To Sit On You!  Part 11 SD</a>
