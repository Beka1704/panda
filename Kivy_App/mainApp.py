import kivy
#from pico_tss import pico
from Kivy_App import pico

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from kivy.graphics import Color, Rectangle

from kivy.clock import Clock

from Kivy_App import kivy_birthday_app
from Kivy_App import kivy_rnv_app
from Kivy_App import kivy_calendar_app
from Kivy_App import kivy_error_app

from Kivy_App import clockDisplay
from Kivy_App import body

from multiprocessing import Queue
from queue import Empty
import pkg_resources
from datetime import datetime
from datetime import timedelta

class Main(body.L1_Boxlayout):
    #layout = GridLayout(cols=2)
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

class Header(BoxLayout):
    h_c = [252.0/255.0, 255.0/255.0, 252.0/255.0]
    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
        pi = pkg_resources.resource_filename(__name__, 'Raspi.png')
        panda = pkg_resources.resource_filename(__name__, 'Panda.png')
        self.cols = 3
        self.row = 1
        self.add_widget(Image(source=pi))
        self.add_widget(Label(text=u'パイ-パンダ', font_name='TakaoPMincho',font_size='42sp'))
        self.add_widget(Image(source=panda))
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(self.h_c[0], self.h_c[1], self.h_c[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

        
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


class Footer(BoxLayout):
    f_c = [252.0/255.0, 255.0/255.0, 252.0/255.0]
    
    def __init__(self, **kwargs):
        super(Footer, self).__init__(**kwargs)
        self.cols = 3
        self.row = 1
        self.utterance = Label()
        self.add_widget(self.utterance)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(self.f_c[0], self.f_c[1], self.f_c[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.rect.source = "Panda.png"
        self.bind(pos=self.update_rect, size=self.update_rect)    

        
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
        
    

class AssistantFrame(App):
    def __init__(self,inbound, outbound, **kwargs):
        self.inbound = inbound
        self.outbound = outbound
        super(AssistantFrame, self).__init__(**kwargs)
    
 
    def build(self):
        self.fl = FloatLayout()
        self.fl.size = [800,600]
        self.header = Header(pos_hint={'top':1, 'x':0.0}, size_hint=[1,0.1])
        self.main = Main(orientation='horizontal', pos_hint={'top':0.9, 'x':0.0}, size_hint=[1,0.8])
        self.footer = Footer(orientation='horizontal', pos_hint={'top':0.1, 'x':0.0})#, size_hint=[1,0.1])
        self.main.add_widget(clockDisplay.Clock_Display())
        self.fl.add_widget(self.header)
        self.fl.add_widget(self.main)
        self.fl.add_widget(self.footer)
        self.last_update = datetime.now()
        Clock.schedule_interval(self.update, 1.0)
        return self.fl
    
    def update(self, dt):
        try:
            message = self.inbound.get(block = False)
            print(message)
            if message is not None:
                self.last_update = datetime.now()
                if 'utterance' in message:
                    self.footer.utterance = message['utterance']
                if(message['type'] == 'Birthday'):
                    for c in self.main.children:
                        self.main.remove_widget(c)
                    self.main.add_widget(kivy_birthday_app.Container(message['content'],size_hint=[1,1]))
                    self.outbound.put("Done")
                if(message['type'] == 'RNV'):
                    for c in self.main.children:
                        self.main.remove_widget(c)
                    self.main.add_widget(kivy_rnv_app.directions(message['content'],size_hint=[1,1]))
                if(message['type'] == 'calendar'):
                    for c in self.main.children:
                        self.main.remove_widget(c)
                    self.main.add_widget(kivy_calendar_app.days(message['content'],size_hint=[1,1]))
                if(message['type'] == 'Error'):
                    for c in self.main.children:
                        self.main.remove_widget(c)
                    self.main.add_widget(kivy_error_app.Container(message['content'],size_hint=[1,1]))
                if ('message' in message):
                    pico.say(message['message'],message['language'])
                
                
                self.outbound.put("Done")
                Clock.schedule_once(self.reload_clock_display, 70)

        except Empty:
            print("No Message")

    def reload_clock_display(self, dt):
        print("Reload clock")
        now = datetime.now()
        print("Now:"+str(now)+" update:"+str(self.last_update))
        print(str(now - self.last_update))
        print(str((now - self.last_update).total_seconds()))
        if (now - self.last_update).total_seconds() > 60:
            
            for c in self.main.children:
                self.main.remove_widget(c)
            self.main.add_widget(clockDisplay.Clock_Display())
            print('Added Clock Widget')






#if __name__ == '__main__':
#    AssistantFrame().run()