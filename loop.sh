#!/bin/sh
while [ true ]
do
    python TweetGrapper.py -i $1 -o output.txt -c -loc cairo -l ar
    sleep 20
done