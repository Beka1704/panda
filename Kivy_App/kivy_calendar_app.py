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

class event_times(body.L3_Gridlayout):
    #layout = GridLayout(cols=2)
    def __init__(self, event, **kwargs):
        super(event_times, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 20
        self.padding = 10
        self.add_widget(Label(text=event['start'],font_size='14sp'))
        self.add_widget(Label(text="until ",font_size='14sp'))
        self.add_widget(Label(text=event['end'],font_size='14sp'))




class event_list(body.L2_Boxlayout):
    #layout = GridLayout(cols=2)
    def __init__(self, events,day, **kwargs):
        super(event_list, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 20
        self.padding = 10
        self.add_widget(Label(text=day,font_size='22sp'))
        for event in events:
            subject = event['subject']
            start = event['start']
            end = event['end']
            out_str = start + " - "+end+"     "+subject
            self.add_widget(Label(text=out_str,font_size='18sp', halign="left"))
            #self.add_widget(event_times(event))

class days(body.L1_Boxlayout):
    def __init__(self,content, **kwargs):
        self.spacing = 5
        self.padding = 5
        super(days, self).__init__(**kwargs)
        self.orientation = "vertical"
        print(content)
        calendar = content['calendar'] 
        for day in calendar:
            self.add_widget(event_list(calendar[day], day))

        
      

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