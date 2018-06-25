import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from Kivy_App import body

import pkg_resources


        
class Container(body.L1_Boxlayout):
    def __init__(self, content, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.add_widget(Label(text=content,font_size='28sp',text_size = self.size))
    
    

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