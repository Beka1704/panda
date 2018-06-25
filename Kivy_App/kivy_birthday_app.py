import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from Kivy_App import body

import pkg_resources

class MyW(body.L2_Gridlayout):
    #layout = GridLayout(cols=2)
    def __init__(self,days,name, **kwargs):
        src = pkg_resources.resource_filename(__name__, 'Raspi.png')
        if(name == "Erik"): 
            src = pkg_resources.resource_filename(__name__, 'doreamon_sleeping_small.jpeg')
        if(name == "Ai"):
            src = pkg_resources.resource_filename(__name__, 'TotoroSleeping.png')
        super(MyW, self).__init__(**kwargs)
        self.cols = (int(days/10))
        #self.row = 10
        for i in range(0,days):
            self.add_widget(Image(source=src))


class Two_grid(body.L2_Boxlayout):
    def __init__(self,name, days, **kwargs):
        super(Two_grid, self).__init__(**kwargs)
        #self.cols = 1
        #self.row = 2
        #self.spacing = [5,5]
        self.orientation = "vertical"
        src = pkg_resources.resource_filename(__name__, 'Raspi.png')
        if(name == "Erik"): 
            src = pkg_resources.resource_filename(__name__, 'doreamon_sleeping_small.jpeg')
        if(name == "Ai"):
            src = pkg_resources.resource_filename(__name__, 'TotoroSleeping.png')

        self.add_widget(Image(source=src, size_hint=[1,1]))
        self.add_widget(Label(text=str(days)+' times to sleep until '+name+'\'s birthday!'))

        
class Container(body.L1_Boxlayout):
    def __init__(self, content, **kwargs):
        super(Container, self).__init__(**kwargs)
        name = content['name']
        days = content['days']
        two_grid = Two_grid(name, days,pos_hint={'top':0.99, 'x':0.0}, size_hint=[1,0.3])
        grid_widget = MyW(days,name, pos_hint={'top':0.68, 'x':0.0}, size_hint=[1,0.7])
        self.add_widget(two_grid)
        self.add_widget(grid_widget)

    
    

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