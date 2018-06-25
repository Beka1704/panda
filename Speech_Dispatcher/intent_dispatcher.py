from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from Speech_Dispatcher import utils
#import Speech_Dispatcher.utils.mapping_reader
import os
import pkg_resources
import importlib
from Speech_Dispatcher import intent_handler
#import Speech_Dispatcher.intent_handler.birthday_handler
from Speech_Dispatcher.utils import mapping_reader
from multiprocessing import Queue


class intent_dispatcher():

    intent_clf = None
    intent_mapping = None

    handler = {}


    def __init__(self, outbound, inbound):
        #path = 'classifiers/text_cat/REAMDE.md'  # always use slash
        outboundlinepath = pkg_resources.resource_filename(__name__, 'intent_classifier.pkl')

        
        self.intent_clf = joblib.load(outboundlinepath)
        mappingpath = pkg_resources.resource_filename(__name__, 'intent_mapping.csv')
        self.intent_mapping = mapping_reader.read_intent_mapping(mappingpath)
        self.load_handler()
        self.outbound = outbound
        self.inbound = inbound
        print(self.handler)


    
    def dispatch(self, utterance):
        print(utterance)
        #words = " ".join("wordlist")
        intent_num = self.intent_clf.predict([utterance])[0]
        print(intent_num)
        if intent_num in self.intent_mapping:
            intent = self.intent_mapping[intent_num]
            print(intent)
            if  intent in self.handler:
                obj = self.handler[intent]
                data = obj.handle(utterance)
                print(data)
                if data is not None:
                    self.outbound.put(data)
            else:
                self.outbound.put({'type':'StatusMessage','content:':'Found no worker to handle '+intent})
                print('Missing matching intent handler! Intent:'+intent)
        else:
            self.outbound.put({'type':'StatusMessage','content:':'Did not understand intent of '+utterance})
            print('Missing matching intent name! Intent Number:'+str(intent_num))
        #print(self.intent_mapping[intent_num])


    def load_handler(self):
        #fileDir = os.path.dirname(os.path.realpath('__file__'))
        #directory = os.fsencode(directory_in_str)
        directory = pkg_resources.resource_filename(__name__, "/intent_handler/")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".py") and not 'init' in filename: 
                #i = importlib.import_module(directory+'.'+filename.partition(".")[0])
                i = importlib.import_module("Speech_Dispatcher.intent_handler."+filename.partition(".")[0])
                self.handler[filename.partition(".")[0]] = i.handler()
                self.handler[filename.partition(".")[0]].test()
                # print(os.path.join(directory, filename))
                continue
            else:
                continue
        print(self.handler)