import StringExtractor as SE
import time

def recent_txt(slug, event_slug,time):
    string = SE.create_str_recent(slug, event_slug,time)
    file = open("recent.txt", "a+",encoding='utf-8')
    file.seek(0)
    file.truncate()
    file.write(string)
    file.close()

def upcoming_txt(slug, event_slug):
    string = SE.create_str_upcoming(slug, event_slug)
    file = open("upcoming.txt", "a+",encoding='utf-8')
    file.seek(0)
    file.truncate()
    file.write(string)
    file.close()

def ongoing_txt(slug, event_slug):
    string = SE.create_str_ongoing(slug, event_slug)
    file = open("ongoing.txt", "a+",encoding='utf-8')
    file.seek(0)
    file.truncate()
    file.write(string)
    file.close()

