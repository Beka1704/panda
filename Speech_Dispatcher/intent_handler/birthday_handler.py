from datetime import datetime
from datetime import timedelta
import os
import pkg_resources


class handler():

    def __init__(self, *args, **kwargs):
        self.birthday_list = self.read_birthdays()
       

    
    def handle(self, utterance):
        found = False
        for k in self.birthday_list:
            if k.upper() in utterance:
                found = True
                birthday = self.birthday_list[k]
                today = datetime.today()
                next_birthday  = datetime(today.year,birthday.month,birthday.day)
                if(next_birthday < today):
                    next_birthday = datetime(today.year+1,birthday.month,birthday.day)
                days_left = (next_birthday - today).days
                msg = k+"s Geburtags ist in "+str(days_left)+" Tagen"
                print(msg)
                return ({'message':msg,'language':"de-DE",'utterance':utterance,'type':'Birthday','content':{'name':k,'days':days_left}})
        if not found: 
            print('Name not found!')
            return({'type':'Error','content':'Name not found - STT understood: '+utterance, 'message':'Entschuldigung, ich habe den Namen nicht verstanden!',"language":"de-DE"})


       

    def test(self):
        print("Hello Birthday")

    def read_birthdays(self):
        #fileDir = os.path.dirname(os.path.realpath('__file__'))
        birthdays_csv = pkg_resources.resource_filename(__name__, "/Config/birthdays.csv")
        mapping = {}
        content = None
        with open(birthdays_csv,'r') as file:
            content = file.readlines()
        if content is None: 
            return False #Put proper exception here
        content = [x.strip('\n') for x in content] 
        for c in content:
            #print(c)
            line = c.split(',')
            #print(line)
            mapping[line[0]] = datetime.strptime(line[1],"%d.%m.%Y")
        return mapping
