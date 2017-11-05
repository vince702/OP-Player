


import json
import urllib2
import unicodedata
import re
import urllib


def returnOpNum(event):
    return int(event['request']['intent']['slots']['opNumber']['value'])
    
def returnAnimeName(event):
    return str(event['request']['intent']['slots']['animeName']['value'])
    


def getto(op,k):
  op -=1
  url = "http://jikan.me/api/anime/"
# open the url and the screen name 
# (The screen name is the screen name of the user for whom to return results for)
  url += "{}".format(k)
  response = urllib2.urlopen(url)
  result = json.load(response)
  ops=[]
  for i in result['opening-theme']:
    unicodedata.normalize('NFKD', i).encode('ascii','ignore')
    k = i.replace(";"," ")
    k = k.replace("&quot","")
    k = re.sub('(\(eps .*\))',"",k)
    k = re.sub('#\d*: ',"",k)
    k = re.sub("&#\S*\s","'",k)   
    k = re.sub("&amp","and",k)             
    k = unicodedata.normalize('NFKD', k).encode('ascii','ignore')
    k = k.replace("()","")
    
    ops.append(k)

  return ops[op]
  
def animeNumber(keyword):
    url = "https://myanimelist.net/search/all?q="
    url += keyword.replace(" ","+")
    f = urllib.urlopen(url)
    html = f.read()
    idNumber = re.search('/anime/\d\d*',html).group(0).replace("/anime/",'')
    idNumber
    return int(idNumber)


def handler(event, context):
    
    
    
    outputSpeech = {"type": "PlainText","text":"Hello World! {}".format("h")}
    reprompt = {"type": "PlainText", "text":"come again?"}
    if event['request']['type']=="IntentRequest":
        
     if   event['request']['intent']['name'] == "price" :
  
       return {
        "sessionAttributes": {},
        "response": {
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "12345",
                            "url": "http://67.159.62.2/anime_ost/puella-magi-madoka-magica-movie-main-theme-single-colourful/gaflfchqkh/01%20-%20Colourful.mp3",
                            "offsetInMilliseconds": 0
                        }
                    }
                }
            ],
            "shouldEndSession": False
          }
        }


     
     else:
         animeID = animeNumber(returnAnimeName(event))
         text = "Opening {} of {} is {}".format(returnOpNum(event)+1,returnAnimeName(event),getto(returnOpNum(event),animeID))
         
         outputSpeech = {"type": "PlainText","text":text}
     reprompt = {"type": "PlainText", "text":"come again?"}
    
    
    
    
    r = {"outputSpeech":outputSpeech,"reprompt": reprompt,"shouldEndSession":True}
    response = {"version":"1.0","sessionAttributes": {}, "response":r}
    return response
    



def main():  
    print getto(1,animeNumber("baccano"))
    return True
    
if __name__ == '__main__':
    main()