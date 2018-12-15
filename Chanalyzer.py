#!/usr/bin/python
import sys
from youtube_api_init import *
import json
import pprint
import re

#video query on pawan kalyan
# Query N videos with description "pawan kalyan" by date 
##### Janasena keywords ######
JSPKeywords = {'HighLevelQueryKeyWord':('Pawan Kalyan', 'Janasena', 'Jana Sena', 'JSP', 'Pawan', 'nagireddy'),
               'ChannelLevelQueryKeyWords': ("pawan", "jana sena", "janasena", "pappu", "kalyan", "jail", "powerstar", "janasain", "addepalli", "sai", "JSP", "Vishnu", "NRI venkat", "sena", "sunkara", "dileep") }
###### Janasena keywords #####
####TDP Keyworkds######
TDPKeywords = {'HighLevelQueryKeyWord':('TDP', 'Chandrababu', 'Nara', 'CBN', 'Lokesh', 'TV5', 'Telugu', 'NTR', 'Chandra Babu', 'Jupudi', 'Varla' ,'Ramayya', 'Rajendraprasad', 'Tammullu', "Kathi", "Mahesh", "Sri Reddy", "Garuda"),
               'ChannelLevelQueryKeyWords': ("chandrababu", "lokesh", "TDP", "Balakrishna", "ABN", "mahakutami", "newsmarg", "yamini", "Balayya", "yaamini", "NTR", "Rajendra", "Kambhampati", "Rammohan", "Jupudi", "Lanka", "Dinakar", "Varla Ramayya", "Sambasiva", "IVR", "Tammareddy", "Actor Sivaji", "Sivaji", "Tammullu", "Garuda", "Nara", "sadineni", "diwakar", "srireddy", "kathi", "kodi", "operation") }
###### TDP keywords #####

####YCP Keyworkds######
YCPKeywords = {'HighLevelQueryKeyWord':('YCP', 'YS Jagan', 'Roja', 'Ambati', 'Jagan', 'Anil Kumar', 'YSRCP'),
               'ChannelLevelQueryKeyWords': ("jagan", "roja", "sankalpa", "ambati", "ycp", "ys", "vijay sai", "ysrcp", "pellillu", "marriage", "note for vote", "yellow media", "Sakshi") }
###### TDP keywords #####
####Kaushal Keyworkds######
KaushalKeywords = {'HighLevelQueryKeyWord':('Kaushal', 'kaushal', 'Koushal', 'Kaushal Army', 'Bigboss'),
               'ChannelLevelQueryKeyWords': ("kaushal", "army", "Koushal", "manda") }
###### TDP keywords #####

def FindBiasedChannels (Keywords, PercThreshold):
    max_videos = 50
    BiasedChannels = set([])
    for keyword in Keywords['HighLevelQueryKeyWord']:
        videoQuery = youtube_search(keyword, max_results=50,order='date')
        vQueryJson = videoQuery[1]
        pp = pprint.PrettyPrinter(indent=4)
        for item in vQueryJson:
            channelInfo = item['snippet']['channelId']
            channelQuery = youtube_search(channelId=channelInfo, max_results=max_videos, order='date')
            hits = 0
            for citem in channelQuery[1]:
                #print(citem['snippet']['description'])
                description = citem['snippet']['description']
                for keyword in Keywords['ChannelLevelQueryKeyWords']:
                    if re.search(keyword, description, re.IGNORECASE):
                        hits += 1
                        break     

            #print("Number of hits in channel", item['snippet']['channelTitle'], " ", hits)
            percentHit = (float(hits) / max_videos) * 100 
            #print("percentHit:", percentHit)
            if percentHit > PercThreshold:
                BiasedChannels.add((str(item['snippet']['channelTitle']), percentHit))
    
    print("List of youtube channels endorsed by this party:-")
    for i in BiasedChannels:
        print i

## main function
PercentThreshold = 30
FindBiasedChannels(Keywords=JSPKeywords, PercThreshold = PercentThreshold)
FindBiasedChannels(Keywords=TDPKeywords, PercThreshold = PercentThreshold)
FindBiasedChannels(Keywords=YCPKeywords, PercThreshold = PercentThreshold)
