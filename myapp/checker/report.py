import requests
from .error import Error
from nltk.corpus import stopwords
import re
languagecheckurl = 'http://localhost:8082/v2/check'
class Report:
    def __init__(self, essay):
        global languagecheckurl
        payload = {"text":essay,"language":"en-US", "enabledOnly":"false"}
        response = requests.post(languagecheckurl,data = payload)
        self.errors = [Error(m) for m in response.json()['matches']]
        self.wordCount = len(re.sub(r"[.,?!;():\"\']", " ", essay).split())
        self.spellingErrorCount = len(list(filter(lambda x:x.errorType()=='spelling', self.errors)))
        self.grammarErrorCount = len(self.errors)-self.spellingErrorCount
        #add properties for average worldlenght, sentence length, readability index etc.
        self.score = 10-((self.spellingErrorCount * 0.25) + (self.grammarErrorCount * 0.25))
        if self.score < 0:
            self.score = 0
    def reprJSON(self):
        return dict(score = self.score,errors = [e.reprJSON() for e in self.errors],
        wordCount = self.wordCount, spellingErrorCount = self.spellingErrorCount, 
        grammarErrorCount = self.grammarErrorCount)

    
    