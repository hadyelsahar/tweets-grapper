#encoding:utf-8 
'''
Created on Oct 28, 2013
python 2.7.3 
@author: hadyelsahar 
'''
import tweepy
import sys
import argparse
import regex
import subprocess
from Vectors.CosineSim import *

# command line arguments 
parser = argparse.ArgumentParser(description='tool to Grap tweets from twitter API - show on console or write to  output file- giving some input words from text file - or search keywords -- [[optional]] clean tweets')
parser.add_argument('-i','--input', help='Input file name',required=False)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= False)
#parser.add_argument('-c','--clean',help='clean tweets by removal or  RT  , Twitter username , Elongations and non alphanumericals', required= False , action="store_true")
parser.add_argument('-u','--uniq',help='extract uniq list of tweets of input file to outputfile based on cosine Similarity', required= False, action="store_true")

args = parser.parse_args()

if args.uniq is True and args.output is None:
  parser.error('must specify output file when choosing --uniq [-u]  option')

######--- Helper functions
def clean(tweet) : 
  #discarding twitter usernames
  #tweet = regex.sub(r'@[A-Za-z0-9_]+', '', tweet,flags=regex.UNICODE)

  #discarding twitter RT or RTTTT or any of it's elongations
  tweet = regex.sub(r'R+T+\s*:*\s', ' ', tweet,flags=regex.UNICODE)

  #Removing links 
  tweet = regex.sub(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', ' ', tweet)

  #replace underscores with spaces
  tweet = tweet.replace("_"," ")

  #remove Mentions
  tweet = regex.sub('@\w+', '', tweet).strip()

  #remove elongations
  #tweet = regex.sub(r'(.)\1\1+',r'\1\1\1', tweet,flags=regex.UNICODE)

  #Convert hashtags into words
  tweet = regex.sub(r'[#_]+',' ', tweet,flags=regex.UNICODE)

  return tweet.strip()  
def writeTweet(tweet):

  if args.output is not None :
    with open(args.output, "a") as myfile:
      tweet = tweet+"\n"
      myfile.write(tweet.encode('utf-8'))           
  else :
    print tweet
######

# reading keywords from input file 
with open(args.input) as f:
    tws = f.read().split("\n")
    tweets = [unicode(t.strip(), encoding='utf-8') for t in tws if len(t) > 0]

for tweet in tweets: 
  tweet = clean(tweet)
  writeTweet(tweet)


if args.uniq is True:
    print "getting unique tweets out of the extracted ones"
    #define uniq function based on consine similarity > 0.7
    def uniq(iterator):
      previous = ""  # Not equal to anything
      cosim  = CosineSim()
      for value in iterator:          
        
        cos = cosim.get_cosine(previous,value)     
        if  cos < 0.7 :
          yield value      
          previous = value

    with open(args.output) as f:
      tweets = f.read().split("\n")
      with open("uniq_"+args.output, 'w+') as file:
        for line in uniq(sorted(tweets)):
          file.write(line+"\n")