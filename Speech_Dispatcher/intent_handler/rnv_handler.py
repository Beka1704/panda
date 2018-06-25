from Speech_Dispatcher.utils import mapping_reader
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import pkg_resources
import os
import requests
import json


class handler():
    #stations = {'Bahnhof':'2481','Marktplatz':'2496','West':'2507','Friedrich':'2487','Kirche':'2498'}
    
    def __init__(self):
        directory = pkg_resources.resource_filename('Speech_Dispatcher', "/Pipelines/")
        fileDir = directory
        self.clf = joblib.load(os.path.join(fileDir,'rnv_classifier.pkl'))
        self.intent_mapping =mapping_reader.read_intent_mapping(os.path.join(fileDir,'rnv_classmapping.csv'))
        self.stations = self.read_stations()
    
    def handle(self, utterance):
        
        #method = self.clf.predict([utterance])[0]
        #return {'type':'RNV','content':'Identified RNV Intent '+str(method)}
        for s, station in self.stations.items():
            if s.upper() in utterance:
                hafas = station[0]
                url = 'http://rnv.the-agent-factory.de:8080/easygo2/api/regions/rnv/modules/stationmonitor/element?hafasID={0}&time=null'.format(hafas)
                try:
                   response = requests.get(url, headers={'RNV_API_TOKEN':'dl8fmbpjjhd1ebbipodmkgda0j'})
                except:
                    return {'utterance':utterance,'type':'Error','content':'Sorry, unexpected error when sending request to RNV','message':'Sorry, unexpected error', 'language':"en-US"}
                if response.status_code == 200:
                    doc = json.loads(response.text)
                    monitor = {'station':station[1]}
                    monitor['departures'] = doc['listOfDepartures']
                    return {'utterance':utterance,'type':'RNV','content':monitor}
                else:
                    return {'utterance':utterance,'type':'Error','content':response.text()}
        return {'utterance':utterance,'type':'Error','content':'Sorry, I didn\'t catch the station!','message':'Sorry, I didn\'t catch the station!','language':"en-US"}

    def test(self):
        print("Hello RNV")

    def read_stations(self):
        station_csv = pkg_resources.resource_filename(__name__, "/Config/stations.csv")
        mapping = {}
        with open(station_csv,'r') as file:
            content = file.readlines()
        if content is None: 
            return False #Put proper exception here
        content = [x.strip('\n') for x in content] 
        for c in content:
            #print(c)
            line = c.split(',')
            #print(line)
            mapping[line[0]] = line[1:]
        return mapping
    