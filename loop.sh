#!/bin/sh
while [ true ]
do
    python TweetGrapper.py -i $1 -o output.txt
    sleep 20
done