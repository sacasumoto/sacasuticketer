import StringExtractor as SE
import time

def recent_txt(url,time):
    slug = SE.get_tournament_slug_from_smashgg_urls(url)
    string = SE.create_str_recent(slug,time)
    file = open("recent.txt", "a+",encoding='utf-8')
    file.seek(0)
    file.truncate()
    file.write(string)
    file.close()

def upcoming_txt(url):
    slug = SE.get_tournament_slug_from_smashgg_urls(url)
    string = SE.create_str_upcoming(slug)
    file = open("upcoming.txt", "a+",encoding='utf-8')
    file.seek(0)
    file.truncate()
    file.write(string)
    file.close()

def ongoing_txt(url):
    slug = SE.get_tournament_slug_from_smashgg_urls(url)
    string = SE.create_str_ongoing(slug)
    file = open("ongoing.txt", "a+",encoding='utf-8')
    file.seek(0)
    file.truncate()
    file.write(string)
    file.close()

def repeat_recent_txt(url,time1,time2):
    recent_txt(url,time1)
    print("Waiting...")
    time.sleep(time2)
    
    
    
