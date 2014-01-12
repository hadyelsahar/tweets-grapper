#!/bin/sh
while [ true ]
do
    python TweetGrapper.py -i $1 -o output.txt -c 
    sleep 20
done