#!/bin/sh
while [ true ]
do
    python TweetGrapper.py -i keywords.txt -o output.txt
    sleep 20
done