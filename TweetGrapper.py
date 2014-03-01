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
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import threading

#location variables 
LOCATIONS = {
'egypt': [22.187405, 26.561508, 31.353637, 36.207504],
'cairo': [29.965643, 31.14682, 30.157002, 31.549194]
}

#common usages:
#1- search keywords from file in twitter and add to file 
#2- subscribe to stream of keywords and write to file

# command line arguments:
parser = argparse.ArgumentParser(description='tool to Grap tweets from twitter API - show on console or write to  output file- giving some input words from text file - or search keywords -- [[optional]] clean tweets')
parser.add_argument('-mode','--mode', help='either "search" or "stream" ',required=True)
parser.add_argument('-i','--input', help='Input file name contains keywords to search for',required=True)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= False)
parser.add_argument('-c','--clean',help='clean tweets by removal or  RT  , Twitter username , Elongations and non alphanumericals', required= False , action="store_true")
parser.add_argument('-kw','--showkw',help='show keyword that was used to get the tweet before the tweet itself separated by a tab', required= False , action="store_true")
parser.add_argument('-u','--uniq',help='extract uniq list of tweets of input file to outputfile based on cosine Similarity', required= False, action="store_true")
parser.add_argument('-l','--lang',help='specify language of the tweets', required= False)
parser.add_argument('-loc','--location', help='activate search mode and capture keyword for search',required=True)
parser.add_argument('-sep','--separator',help='separator used to separate between tweets , otherwise newline is used ', required= False)
parser.add_argument('-printevery','--printevery',help='[Stream only] print notifications every number of tweets otherwise 1000', required= False)

args = parser.parse_args()

if args.uniq is True and args.output is None:
  parser.error('must specify output file when choosing --uniq [-u]  option')

if args.showkw is True and args.mode.lower() in "stream":
  parser.error('showing keyword is not implemented yet with streaming mode')

if args.mode.lower() not in "stream" and args.printevery is not None:
  parser.error('--printevery option works only with streaming mode')

if args.printevery is not None and not args.printevery.isdigit():
  parser.error('--printevery option should be a proper integer')  


######--- Helper functions
# cleaning tweets
def clean(tweet) : 
  #discarding twitter usernames
  #tweet = regex.sub(r'@[A-Za-z0-9_]+', '', tweet,flags=regex.UNICODE)

  #discarding twitter RT or RTTTT or any of it's elongations
  tweet = regex.sub(r'R+T+\s*:*\s', ' ', tweet,flags=regex.UNICODE)

  #Removing links 
  tweet = regex.sub(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', ' ', tweet)

  #replace underscores with spaces
  tweet = tweet.replace("_"," ")

  #remove elongations
  #tweet = regex.sub(r'(.)\1{2,}',r'\1\1\1', tweet,flags=regex.UNICODE)
  #Convert hashtags into words
  tweet = regex.sub(r'[#_]+',' ', tweet,flags=regex.UNICODE)

  return tweet.strip()  

# add keyword to the begining of each tweet if option is selected 
def addKeyWord(keyword, tweet) : return  keyword+'\t'+tweet 

def writeTweet(keyword, tweet):
  if args.clean is True :  
    tweet = clean(tweet)
      
  if args.showkw is True : 
    tweet = addKeyWord(keyword ,tweet)

  separator = ("\n" if args.separator is None else args.separator)      
  
  if args.output is not None :
    with open(args.output, "a") as myfile:
      tweet = tweet+separator
      myfile.write(tweet.encode('utf-8'))           
  else :
    print tweet

##--- Helper Classes

class StdOutListener(StreamListener): 
  counter = 0 
  printevery = 1000

  """ A listener handles tweets are the received from the stream.
  This is a basic listener that just prints received tweets to stdout.
  """
  def __init__(self):     
    self.run = True
    self.keywords = []

  def on_data(self, data):                
    tweet = regex.sub(r'[\t\n\s]+',' ',json.loads(data)['text'])           
    writeTweet("", tweet)
    StdOutListener.counter += 1 
    if StdOutListener.counter % StdOutListener.printevery == 0 and args.output is not None:
      print str(StdOutListener.counter) + "tweets collected"

    if self.run:                  
      return True

    else :
      return False

  def on_error(self, status):
    print status


# setting twitter API 
consumer_token = "HHb0Q4EwqUFhiOT9cuZw"
consumer_secret = "wiUpi18szMmaBeDe3Xz0W8hTm4DSSSwRKSAdE5OTv0"
ACCESS_TOKEN = '158681231-7iclqcgq8kFkPZBiQPK0AruMSKySUlNr0FethRFf'
ACCESS_TOKEN_SECRET = 'VisPcmHHE6ENNDspL48g15CloHNVmt0FRMPopCdphzpQb'


#setting Tweepy API
auth = tweepy.OAuthHandler( consumer_token,consumer_secret )
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# reading keywords from input file 
with open(args.input) as f:
    kws = f.read().split("\n")    
    keywords = [kw.strip() for kw in kws if len(kw) > 0]

#SEARCH Mode
#----------------
if  "search" in args.mode.lower() : 
  for keyword in keywords:     
    try:
      # fetcing tweet with specificed language or not 
      if args.lang is not None :
        tweets = api.search(keyword,count=1000,lang=args.lang,locale=args.location)
      else :
        tweets = api.search(keyword,count=1000,locale=args.location)
    
      print str(len(tweets)) + " - " + keyword
      # getting tweet text   
      def txt(tweet) : return regex.sub(r'[\t\n\s]+',' ',tweet.text)
      tweets = map(txt,tweets)
            
      for tweet in tweets:
        writeTweet(unicode(keyword, encoding='utf-8'), tweet)
    
    except Exception, e:
      with open("log.txt", 'a+') as file:    
        file.write(str(e) + "error when writing tweet of " + keyword)


#STREAM Mode
#------------------
elif "stream" in args.mode.lower():

  #max count for keywords in Streaming is 400
  kwChunkSize = 400
  streams = []

  #for each 400 keywords , initialize stdoutlistener object for it (because limit of streaming api for twitter is 400)
  for i in xrange(0,len(keywords),kwChunkSize):
    l = StdOutListener()
    l.keywords = keywords[i:i+kwChunkSize]
    streams.append(l)

  print str(len(streams)) +" streams created"

  ##check print every : 
  if args.printevery is not None:
    pe = int(args.printevery)
    StdOutListener.printevery = pe

  ## run exit mode : 
  #streaming will run forever unless user write "stop" 
  def capture(streams):     
    word = "emptytext" 
    while word not in "stop":
      word = raw_input ("write \"stop\" to stop streaming \n")
      if word.lower() not in "stop" :
        print "wrong input"

    print "stopped streaming with " + str(StdOutListener.counter) + " tweets collected"
    for l in streams:
      l.run = False

  t = threading.Thread(target=capture, args=(streams,))
  t.start()
 

  #todo implement locations
  locs = LOCATIONS[args.location]
  langs = [args.lang] if args.lang is not None else None  

  for l in streams:    
    stream = Stream(auth, l)
    stream.filter(track=l.keywords,languages=langs,locations=locs)



# make new file of uniq tweets only 
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
    with open("uniq_"+args.output, 'w+') as file:
      for line in uniq(sorted(f)):
        file.write(line)