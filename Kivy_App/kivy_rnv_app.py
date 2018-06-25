import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


from Kivy_App import body

import pkg_resources




class departure_list(body.L2_Gridlayout):
    #layout = GridLayout(cols=2)
    def __init__(self, departures, **kwargs):
        super(departure_list, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 20
        self.padding = 10
        for departure in departures:
            line = 'Line '+ departure['line']
            self.add_widget(Label(text=line,font_size='14sp'))
            self.add_widget(Label(text=str((departure['time'])),font_size='14sp'))

class directions(body.L1_Boxlayout):
    def __init__(self,content, **kwargs):
        self.spacing = 10
        self.padding = 10
        super(directions, self).__init__(**kwargs)
        self.orientation = "vertical"
        station = content['station']
        self.add_widget(Label(text='Connections from '+station,font_size='22sp'))
        print('==========================================================')
        print(type(content['departures']))
        print(content['departures'])
        departures = {}
        for dep in content['departures']:
            if(dep['direction'] not in departures): departures[dep['direction']] = []
            departure = {'line':dep['lineLabel'],'time':dep['time']}
            departures[dep['direction']].append(departure)
        for direction, departures in departures.items():
            self.add_widget(Label(text='In direction of '+direction,font_size='18sp'))
            self.add_widget(departure_list(departures))
    
    

#class e8App(App):
#    def build(self):
#        fl = FloatLayout()
#        two_grid = Two_grid(pos_hint={'top':0.99, 'x':0.0}, size_hint=[1,0.3])
#        grid_widget = MyW(pos_hint={'top':0.7, 'x':0.0}, size_hint=[1,0.7])
#        fl.add_widget(two_grid)
#        fl.add_widget(grid_widget)
#        return fl

#if __name__ == '__main__':
#    e8App().run()