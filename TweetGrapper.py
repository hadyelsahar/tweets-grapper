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
parser = argparse.ArgumentParser(description='tool to Grap tweets from twitter API - show on console or write to  output file- giving some input words from text file -- [[optional]] clean tweets')
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= False)
parser.add_argument('-c','--clean',help='clean tweets by removal or  RT  , Twitter username , Elongations and non alphanumericals', required= False , action="store_true")
parser.add_argument('-kw','--showkw',help='show keyword that was used to get the tweet before the tweet itself separated by a tab', required= False , action="store_true")
parser.add_argument('-l','--lang',help='specify language of the tweets', required= False)
parser.add_argument('-s','--separator',help='separator used to separate between tweets , otherwise newline is used ', required= False)
parser.add_argument('-u','--uniq',help='extract uniq list of tweets of input file to outputfile based on cosine Similarity', required= False, action="store_true")

args = parser.parse_args()

if args.uniq is True and args.output is None:
  parser.error('must specify output file when choosing --uniq [-u]  option')

# setting twitter API 
consumer_token = "HHb0Q4EwqUFhiOT9cuZw"
consumer_secret = "wiUpi18szMmaBeDe3Xz0W8hTm4DSSSwRKSAdE5OTv0"
auth = tweepy.OAuthHandler( consumer_token,consumer_secret )
api = tweepy.API(auth)


# reading keywords from input file 
with open(args.input) as f:
    kws = f.read().split("\n")
    keywords = [unicode(kw.strip(), encoding='utf-8') for kw in kws if len(kw) > 0]

for keyword in keywords: 
  try:
    # fetcing tweet with specificed language or not 
    if args.lang is not None :
      tweets = api.search(keyword,count=1000,lang=args.lang)
    else :
      tweets = api.search(keyword,count=1000)
  
    # getting tweet text   
    def txt(tweet) : return regex.sub(r'[\t\n\s]+',' ',tweet.text)
    tweets = map(txt,tweets)
 
    # cleaning tweets if required 
    def clean(tweet) : 
  	  #discarding twitter usernames
      tweet = regex.sub(r'@[A-Za-z0-9_]+', '', tweet,flags=regex.UNICODE)
      #discarding twitter RT or RTTTT or any of it's elongations
      tweet = regex.sub(r'R+T+\s*:*\s', ' ', tweet,flags=regex.UNICODE)
      #Removing links 
      tweet = regex.sub(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', ' ', tweet)
      #replace underscores with spaces
      tweet = tweet.replace("_"," ")
      #remove elongations
      #tweet = regex.sub(r'(.)\1{2,}',r'\1\1\1', tweet,flags=regex.UNICODE)
      #remove non characters     
      tweet = regex.sub(r'[\W]+',' ', tweet,flags=regex.UNICODE)

      return tweet.strip()  

    if args.clean is True :  
      tweets = map(clean,tweets)

    # add keyword to the begining of each tweet if option is selected 
    def addKeyWord(tweet) : return  keyword+'\t'+tweet 
    if args.showkw is True : tweets = map(addKeyWord,tweets)
 
    # parsing separating them with separator  
    separator = ("\n" if args.separator is None else args.separator)

    tweetsText = separator.join(tweets)   	       	    	   	                 	      

    if args.output is not None :
      with open(args.output, "a") as myfile:
        myfile.write(tweetsText.encode('utf-8'))	      
      print "-- "+str(len(tweets))+" tweets for keyword : \""+ keyword+"\"" 
    else :
      print tweetsText

  except:
    with open("log.txt", 'a+') as file:    
      file.write(keyword)


# make new file of uniq tweets only 
if args.uniq is True:
  print "getting unique tweets out of the extracted ones"
  #define uniq function based on consine similarity > 0.7
  def uniq(iterator):
    previous = ""  # Not equal to anything
    cosim  = CosineSim()
    for value in iterator:          
      
      cos = cosim.get_cosine(previous,value) 
      print cosim.text_to_vector(value)
      print cos 
      if  cos < 0.7 :
        yield value      
        previous = value

  with open(args.output) as f:
    with open("uniq_"+args.output, 'w+') as file:
      for line in uniq(sorted(f)):
        file.write(line)