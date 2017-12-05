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

def get_tournament_slug_from_smashgg_urls(url):
    return(url.split("/")[4])


def get_tournament_info(slug):
    tournament_url = "https://api.smash.gg/tournament/" + slug
    t = requests.get(tournament_url, verify='cacert.pem')
    tournament_data = t.json()
    tournament_name = tournament_data["entities"]["tournament"]["name"]
    
    timezone = tournament_data["entities"]["tournament"]["timezone"]
    if timezone != True:
        timezone = 'America/Los_Angeles'
        

    # Scrape event page in case event ends earlier than tournament
##    if slug == 'the-road-to-genesis':
    if 'weds-night-fights' in slug:
        event_url = "https://api.smash.gg/tournament/" + slug + "/event/" + "smash-melee"
    elif 'training-mode-tuesdays-13' == slug:
        event_url = "https://api.smash.gg/tournament/" + slug + "/event/" + "tmt-top-8"
    else:
        event_url = "https://api.smash.gg/tournament/" + slug + "/event/" + "melee-singles"
    try:
        e = requests.get(event_url, verify='cacert.pem')
        event_data = e.json()
        event_id = event_data["entities"]["event"]["id"]
    except:
        event_url = "https://api.smash.gg/tournament/" + slug + "/event/" + "melee-singles"
        e = requests.get(event_url, verify='cacert.pem')
        event_data = e.json()
        event_id = event_data["entities"]["event"]["id"]

    timestamp = event_data["entities"]["event"]["endAt"]
    if not timestamp:
        timestamp = tournament_data["entities"]["tournament"]["endAt"]
    # Get local date
    date = datetime.fromtimestamp(timestamp, pytz.timezone(timezone)).date()
    date = str(date)

    ## Get standings
    if 'training-mode-tuesdays' in slug:
        attendee_url = 'https://api.smash.gg/tournament/'+slug+'/attendees?filter=%7B"eventIds"%3A'+str(event_id)+'%7D'
        a_data = requests.get(attendee_url, verify='cacert.pem').json()
        count = a_data["total_count"]
    else:
        try:
            standing_string = "/standings?expand[]=attendee&per_page=100"
            standing_url = event_url + standing_string
            s = requests.get(standing_url,verify='cacert.pem')
            s_data = s.json()
            count = s_data["total_count"]
        except:
            attendee_url = 'https://api.smash.gg/tournament/'+slug+'/attendees?filter=%7B"eventIds"%3A'+str(event_id)+'%7D'
            a_data = requests.get(attendee_url, verify='cacert.pem').json()
            count = a_data["total_count"]
    return([tournament_name,event_id,count,str(date)])
    
def create_smashgg_api_urls(slug):
    """from master url creates list of api urls for pools and bracket"""

    if 'weds-night-fights' in slug:
        url = "https://api.smash.gg/tournament/" + slug + "/event/smash-melee?expand[0]=groups&expand[1]=phase"
    elif 'training-mode-tuesdays-13' == slug:
        url = "https://api.smash.gg/tournament/" + slug + "/event/tmt-top-8?expand[0]=groups&expand[1]=phase"
    else:
        url = 'http://api.smash.gg/tournament/' + slug + '/event/melee-singles?expand[0]=groups&expand[1]=phase'
    try:
        data = requests.get(url,verify='cacert.pem').json()
        groups = data["entities"]["groups"]
    except:
        url = 'http://api.smash.gg/tournament/' + slug + '/event/melee-singles?expand[0]=groups&expand[1]=phase'
        data = requests.get(url,verify='cacert.pem').json()
        groups = data["entities"]["groups"]
        
    urlList = []
    for i in range(len(groups)):
        iD = str(groups[i]["id"])
        urlList.append("http://api.smash.gg/phase_group/" + iD + "?expand[0]=sets&expand[1]=entrants")

    if 'red-bull-smash-gods-and-gatekeepers-2' in slug:
        url = "https://api.smash.gg/tournament/" + slug + "/event/forsaken-bracket?expand[0]=groups&expand[1]=phase"
        data = requests.get(url,verify='cacert.pem').json()
        groups = data["entities"]["groups"]
        for i in range(len(groups)):
            iD = str(groups[i]["id"])
            urlList.append("http://api.smash.gg/phase_group/" + iD + "?expand[0]=sets&expand[1]=entrants")

    return(urlList)

def get_tournament_timezone(slug):
    tournament_url = "https://api.smash.gg/tournament/" + slug
    t = requests.get(tournament_url, verify='cacert.pem')
    tournament_data = t.json()
    tournament_name = tournament_data["entities"]["tournament"]["name"]
    
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


def create_str_upcoming(slug):
    final = ''
    urlList = create_smashgg_api_urls(slug)
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

def create_str_ongoing(slug):
    final = ''
    urlList = create_smashgg_api_urls(slug)
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
def create_str_recent(slug,time):
    final = ''
    urlList = create_smashgg_api_urls(slug)
    tz = requests.get("https://api.smash.gg/tournament/"+slug,verify='cacert.pem').json()['entities']['tournament']['timezone']
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
                        final += str_set
        except KeyError as K:
            continue
    return(final)



        




    
