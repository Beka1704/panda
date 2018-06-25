from  Speech_Dispatcher.utils import mapping_reader
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import os
import pkg_resources
from word2number import w2n
from datetime import date
from datetime import datetime
import requests
import json

class handler():

    months = {'January':'01','Feburary':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
    days = {'First':'01', 'Second':'02', 'Third':'03', 'Fourth':'04', 'Fifth':'05', 'Sixth':'06', 'Seventh':'07', 'Eigth':'08', 'Ninth':'09', 'Twenty-First':'21', 'Twenty-Second':'22', 'Twenty-Third':'23', 'Twenty-Fourth':'24', 'Twenty-Fifth':'25', 'Twenty-Sixth':'26', 'Twenty-Seventh':'27', 'Twenty-Eigth':'28', 'Twenty-Ninth':'29', 'Eleventh':'11', 'Twelth':'12', 'Thirteenth':'13', 'Fourteenth':'14', 'Fifteenth':'15', 'Sixteenth':'16', 'Seventeenth':'17', 'Eighteenth':'18', 'Nineteenth':'19', 'Twentieth':'20', 'Thirtieth':'30', 'Thirty-First':'31'}

    def __init__(self):
        #self.clf = joblib.load('calendar_classifier.pkl')
        #self.intent_mapping = utils.mapping_reader.read_intent_mapping('rnv_mapping.csv')
        fileDir = pkg_resources.resource_filename('Speech_Dispatcher', "/Pipelines/")
        self.clf = joblib.load(os.path.join(fileDir,'calendar_classifier.pkl'))
        self.intent_mapping = mapping_reader.read_intent_mapping(os.path.join(fileDir,'calendar_classmapping.csv'))

    def handle(self, utterance):
        method = self.clf.predict([utterance])[0]
        query_date = self.utterance_to_date(utterance)
        print(query_date)
        if query_date is not None:
            view = self.query_calendar_view(query_date) 
            if view is None:
                return {'utterance':utterance,'type':'error','content':'Something went wrong in Outlook connection','message':'Something went wrong in Outlook connection','language':"en-US"}
            else:
                return {'utterance':utterance,'type':'calendar','content':{'calendar':view}}
        else:
            return {'utterance':utterance,'type':'error','content':'Sorry, I Didn\'t understand the date correctly'+str(method),'message':'Sorry, I Didn\'t understand the date correctly','language':"en-US"}    

    def test(self):
        print("Hello Calendar")

    def query_calendar_view(self, date):
        #2018-01-09T12:00:00
        ms_date_str = date.strftime("%Y-%m-%d")#T%H:%M:%S")
        print(ms_date_str)
        try:
            res = requests.get('http://127.0.0.1:5000/get_benjamins_events?date='+ms_date_str)
        except:
            return None #{'utterance':utterance,'type':'Error','content':'Sorry, unexpected error when sending request to RNV','message':'Sorry, unexpected error'}
        print(res.text)
        return json.loads(res.text)


    def utterance_to_date(self, utterance):
        monthStr = None 
        dayStr = None
        for m in self.months:
            if m.upper() in utterance: 
                monthStr = m
                break
        for d in self.days:
            if d.upper() in utterance: 
                dayStr = d
                break

        if monthStr is None or dayStr is None: return None
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        year = now.year
        date_str = str(year)+'.'+self.months[monthStr]+'.'+str(self.days[dayStr])
        query_date = datetime.strptime(str(year)+'.'+self.months[monthStr]+'.'+str(self.days[dayStr]), '%Y.%m.%d')
        if query_date <  now:
            query_date = datetime.strptime(str(year+1)+'.'+self.months[monthStr]+'.'+str(self.days[dayStr]), '%Y.%m.%d')
        return query_date
    