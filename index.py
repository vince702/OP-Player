import json
import base64
import unicodedata
import re
import urllib
import urllib2

def returnOpNum(event):
    
    
    if event['request']['intent']['slots']['opNumber']['value'] == "four":
        return 4
    if event['request']['intent']['slots']['opNumber']['value'] == "for":
        return 4
                    
    if event['request']['intent']['slots']['opNumber']['value'] == "two":
        return 2
    if event['request']['intent']['slots']['opNumber']['value'] == "to":
        return 2
    else:
        return int(event['request']['intent']['slots']['opNumber']['value'])
    
def returnAnimeName(event):
    return str(event['request']['intent']['slots']['animeName']['value'])
    


def getto(op,k):
  

  op -=1
  url = "http://jikan.me/api/anime/"
# open the url and the screen name 
# (The screen name is the screen name of the user for whom to return results for)
  url += "{}".format(k)
  response = urllib.urlopen(url)
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

  
def animeMp3(keyword):
  
    keyword = keyword
    keyword = keyword.replace("  "," ")
    keyword = base64.b64encode(keyword)
   
    url = "https://dmhacker-youtube.herokuapp.com/alexa-search/"
    url1 = url + keyword
    response = urllib2.urlopen(url1)
    result = json.load(response)
    
    mp3Link = "https://dmhacker-youtube.herokuapp.com"
    mp3Link =  mp3Link + result['link']
    
    return mp3Link
  

def lambda_handler(event, context):
    
    outputSpeech = {"type": "PlainText","text":"Hello World! {}".format("h")}
    reprompt = {"type": "PlainText", "text":"come again?"}
    
    
       
    if event['request']['type']=="IntentRequest":
     

         
#--------------------------UTA PLAYER -------------------------#
     if   event['request']['intent']['name'] == "utaPlayer" :
       
       animeID = animeNumber(returnAnimeName(event))
       songName = getto(returnOpNum(event),animeID)
       mp3 = animeMp3(songName)
       songIntroText = "now playing " + songName   
       return {
        "sessionAttributes": {},
        
        "response": {
            
            
            "outputSpeech": {
            "type": "PlainText",
            "text": songIntroText
               },
               
            "directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "12345",
                            "url": mp3,
                            "offsetInMilliseconds": 0
                        }
                    }
                }
                
            ],
            "shouldEndSession": True
          }
        }

#-----------------PAUSE-------------------------~~~~~~~~~

     if   event['request']['intent']['name'] == "AMAZON.PauseIntent" :
       
       
       return {
        "sessionAttributes": {},
        
        "response": {
            
            
         
            "directives": [
                {
                   "type": "AudioPlayer.Stop"
                }
                
            ],
            "shouldEndSession": True
          }
        }

#----------------------------------------------------------
     
     else:
         animeID = animeNumber(returnAnimeName(event))
          
         text = "Opening {} of {} is {}".format(returnOpNum(event),returnAnimeName(event),getto(returnOpNum(event),animeID))
         
         outputSpeech = {"type": "PlainText","text":text}
         
         
         
         
    
         
     reprompt = {"type": "PlainText", "text":"come again?"}
    
    
    
    
    r = {"outputSpeech":outputSpeech,"reprompt": reprompt,"shouldEndSession":True}
    response = {"version":"1.0","sessionAttributes": {}, "response":r}
   
   
 
   
   
    return response
 
 
def main():
    print animeMp3("fullmeteal alchemist")
 
 
 
 
if __name__ == '__main__':
    main()