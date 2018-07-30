#!/bin/bash

program="py6nimmt"
if [ ! -z "$2" ]
	then
		args="$2"
fi
# switch on $1
case "$1" in
# run debug as is
	"debug")
		python3 ./"$program"DEBUG.py $args
		;;

# make a debug-free file
	"clean")
		grep -v -e "DEBUG:" ./"$program"DEBUG.py > "$program".py	
		;;

# display help
	"help")	
		printf "Tool to simplify startung's workflow\nUsage: $0 debug|clean|help|run \"any arguments that need passing\"\n"
		;;

# default: make debug-free, run debug-free
	"run"|*)	
		grep -v -e "DEBUG:" ./"$program"DEBUG.py > "$program".py	
		python3 ./"$program".py $args
		;;
esac	
