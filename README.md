tweets-grapper
==============

LightWeight Tweets Grapper available with some processing options on the tweets for Text Mining common tasks 

usage: TweetGrapper.py [-h] -mode MODE -i INPUT [-o OUTPUT] [-c] [-kw] [-u] [-l LANG] -loc LOCATION [-sep SEPARATOR] [-printevery PRINTEVERY]

optional arguments:
  -h, --help            show this help message and exit
  -mode MODE, --mode MODE
                        either "search" or "stream"
  -i INPUT, --input INPUT
                        Input file name contains keywords to search for
  -o OUTPUT, --output OUTPUT
                        Output file name - print in console if not specified
  -c, --clean           clean tweets by removal or RT , Twitter username ,
                        Elongations and non alphanumericals
  -kw, --showkw         show keyword that was used to get the tweet before the
                        tweet itself separated by a tab
  -u, --uniq            extract uniq list of tweets of input file to
                        outputfile based on cosine Similarity
  -l LANG, --lang LANG  specify language of the tweets
  -loc LOCATION, --location LOCATION
                        activate search mode and capture keyword for search
  -sep SEPARATOR, --separator SEPARATOR
                        separator used to separate between tweets , otherwise
                        newline is used
  -printevery PRINTEVERY, --printevery PRINTEVERY
                        [Stream only] print notifications every number of
                        tweets otherwise 1000

options :
-----------
* continous Streaming or Search latest 100 for each keyword
* write to file or on console 
* clean tweets 
* get uniq tweets only using consine similarity
