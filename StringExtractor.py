import requests
import pytz as pytz
from datetime import datetime
"""
Copyright (c) 2015 Andrew Nestico

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Thanks to Andrew Nestico

"""


'''Smash.GG Code'''


"https://api.smash.gg/tournament/weds-night-fights-2017-spring-season-2-4?expand[0]=event"


tournament_events_url = "https://api.smash.gg/tournament/%s?expand[0]=event"
event_url = "https://api.smash.gg/tournament/%s/event/%s?expand[0]=groups&expand[1]=phase"
phase_url = "http://api.smash.gg/phase_group/%s?expand[0]=sets&expand[1]=entrants"




def get_tournament_slug_from_smashgg_urls(url):
    return(url.split("/")[4])


def get_tournament_event_slugs(slug):
    tournament_data = requests.get(tournament_events_url % slug,
                                   verify="cacert.pem").json()
    event_slugs = []
    event_dict = {}
    for event in tournament_data["entities"]["event"]:
##        event_slugs.append(event["slug"].split("/")[-1])
        event_dict[event["name"]] = event["slug"].split("/")[-1]
    return(event_dict)

def get_tournament_timezone(slug):
    tournament_url = "https://api.smash.gg/tournament/" + slug
    t = requests.get(tournament_url, verify='cacert.pem')
    tournament_data = t.json()    
    timezone = tournament_data["entities"]["tournament"]["timezone"]
    return(timezone)

# L = ["melee-singles","smash-melee",tmt-top-8"]



    
def create_smashgg_api_urls(slug, event_slug):
    urlList = []
    data = requests.get(event_url % (slug, event_slug), verify="cacert.pem").json()
    groups = data["entities"]["groups"]
    for phase in range(len(groups)):
        ID = str(groups[phase]["id"])
        urlList.append(phase_url % ID)
    return(urlList)

def get_tournament_timezone(slug):
    tournament_url = "https://api.smash.gg/tournament/" + slug
    t = requests.get(tournament_url, verify='cacert.pem')
    tournament_data = t.json()    
    timezone = tournament_data["entities"]["tournament"]["timezone"]
    return(timezone)

    


'''String Creations'''

#Upcoming: Any match not yet started
'"startAt" time correspodning probably when bracket starts'
#Ongoing: Any match started but not yet completed
'"startedAt" time corresponding to when a match is called'
#Recent Results: Any match completed since X amount of time.
'"completedAt" time corresponding to when a match is finished'
'''
"startAt":1469228400,"startedAt":1469228780,"completedAt":1469229945
or 'null'
"fullRoundText":"Losers Round 1","midRoundText":"Losers 1","shortRoundText":"L1"
"wPlacement":9,"lPlacement":13




'''


def create_str_upcoming(slug, event_slug):
    final = ''
    urlList = create_smashgg_api_urls(slug, event_slug)
    for url in urlList:
        try:
            data = requests.get(url,verify='cacert.pem').json()
            entrants = data["entities"]["entrants"]
            entrant_dict = {}
            for entrant in entrants:
                entrant_dict[entrant["id"]] = entrant["name"]
            sets = data["entities"]["sets"]
            for set in sets:
                if set["entrant1Id"] != None and set["entrant2Id"] != None:
                    if set["completedAt"] == None and set["startedAt"] == None:
                            player1 = entrant_dict[set["entrant1Id"]]
                            player2 = entrant_dict[set["entrant2Id"]]
                            str_set = '{} v.s. {}, '.format(player1,player2)
                            final += str_set
        except KeyError:
            continue
    return(final)

def create_str_ongoing(slug, event_slug):
    final = ''
    urlList = create_smashgg_api_urls(slug, event_slug)
    for url in urlList:
        try:
            data = requests.get(url,verify='cacert.pem').json()
            entrants = data["entities"]["entrants"]
            entrant_dict = {}
            for entrant in entrants:
                entrant_dict[entrant["id"]] = entrant["name"]
            sets = data["entities"]["sets"]
            for set in sets:
                if set["entrant1Id"] != None and set["entrant2Id"] != None:
                    if set["completedAt"] == None and set["startedAt"] != None:
                            player1 = entrant_dict[set["entrant1Id"]]
                            player2 = entrant_dict[set["entrant2Id"]]
                            str_set = '{} v.s. {}, '.format(player1,player2)
                            final += str_set
        except KeyError:
            continue
    return(final)

#time in seconds
def create_str_recent(slug, event_slug, time):
    final = ''
    urlList = create_smashgg_api_urls(slug, event_slug)
    tz = get_tournament_timezone(slug)
    currentTime = int(datetime.now(pytz.timezone(tz)).timestamp())
    for url in urlList:
        try:
            data = requests.get(url,verify='cacert.pem').json()
            entrants = data["entities"]["entrants"]
            entrant_dict = {}
            for entrant in entrants:
                entrant_dict[entrant["id"]] = entrant["name"]
            sets = data["entities"]["sets"]
            for set in sets:
                if set["entrant1Id"] != None and set["entrant2Id"] != None and set["completedAt"] != None:
                    matchTime = set["completedAt"]
                    difference = currentTime - matchTime
                    if difference < time: 
                        player1Score = set["entrant1Score"]
                        player2Score = set["entrant2Score"]
                        player1ID = set["entrant1Id"]
                        player2ID = set["entrant2Id"]
                        player1 = entrant_dict[player1ID]
                        player2 = entrant_dict[player2ID]
                        regular = ''
                        gf = ''
                        if set["isGF"]:
                            if type(player1Score) == int and type(player2Score)== int:
                                if player1Score > -1 and player2Score > -1:
                                    str_set = '{} v.s. {}({}-{}), '.format(player1,player2,player1Score,player2Score)
                            else:
                                winnerID = entrant_dict[set["winnerId"]]
                                loserID = entrant_dict[set["loserId"]]
                                if winnerID == player1ID:
                                    str_set = '{} v.s. {}(W-L), '.format(player1,player2)
                                else:
                                    str_set = '{} v.s. {}(L-W), '.format(player1,player2)
                            gf += str_set                            
                        else:
                            if type(player1Score) == int and type(player2Score)== int:
                                if player1Score > -1 and player2Score > -1:
                                    str_set = '{} v.s. {}({}-{}), '.format(player1,player2,player1Score,player2Score)
                            else:
                                winnerID = entrant_dict[set["winnerId"]]
                                loserID = entrant_dict[set["loserId"]]
                                if winnerID == player1ID:
                                    str_set = '{} v.s. {}(W-L), '.format(player1,player2)
                                else:
                                    str_set = '{} v.s. {}(L-W), '.format(player1,player2)
                            regular += str_set
                        final += regular + gf
        except KeyError as K:
            continue
    return(final)



        




    
