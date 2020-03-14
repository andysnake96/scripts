Various scripts, mostly in bash and python
main topics:
ec2 wrapper -> aws folder
	->used in university project for an implementation of MapReduce application on ec2 instances FaultTollerant&LocallityAware 
		-> see my repo mapreduce
net -> wget with header customization, and netcatFTP client/server 
pari_gp scripts mostly on BSmooth sieve&check in a given interval with a custom mongomery polynomial
	-> very useful with Quadratic Sieve variant -> also see my repository on SIMPQS with Large prime variation https://andysnake96@bitbucket.org/andysnake96/simpqs.git 
video -> ffmpeg scritps
also 
	some script to extract contents from some cdn, basically html regex parsing and download enqueuing via wget with headers customized
	some script to get pdf diffs between some file, trivial but very useful UseCase shortly extract differences in 2 pdf version of slide, for say
		-> missing diff parsing to remark changed pages
	some scripts on video editing with the most great and powerl video software -> ffmpeg 
		-> very unclean unfortunatelly but I plan to return on these shortly 
	a non trivial Makefile that I've used in a network university project for the building and dynamically setting parameters used by a bash script to automate time mesuring on different configuration
		->var/getTimesAutomation.sh and var/Makefiles/Makefile
			-> used in an implementation of SelectiveRepete over an berkeley UDP socket to build reliability on top of UDP
				->details in my repo https://github.com/andysnake96/selective_repete_ring_buffer_concurrent
Hopefully Usefull to anybody
