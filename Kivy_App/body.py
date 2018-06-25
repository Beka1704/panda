from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from kivy.graphics import Color, Rectangle

cl1 = [45.0/255.0, 58.0/255.0, 58.0/255.0]
cl2 = [43.0/255.0, 168.0/255.0, 74.0/255.0]
cl3 = [36.0/255.0, 130.0/255.0, 50.0/255.0]


class L1_Boxlayout(BoxLayout):

    def __init__(self, **kwargs):
        super(L1_Boxlayout, self).__init__(**kwargs)
        #self.rect = Rectangle((0,0)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl1[0], cl1[1], cl1[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
            #self.rect.source = "Panda.png"
            
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


class L2_Boxlayout(BoxLayout):
    
    def __init__(self, **kwargs):
        super(L2_Boxlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl2[0], cl2[1], cl2[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size    

class L3_Boxlayout(BoxLayout):
    
    def __init__(self, **kwargs):
        super(L3_Boxlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl3[0], cl3[1], cl3[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size    

class L1_Gridlayout(GridLayout):
    def __init__(self, **kwargs):
        super(L1_Gridlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl1[0], cl1[1], cl2[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size    

class L2_Gridlayout(GridLayout):
    def __init__(self, **kwargs):
        super(L2_Gridlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl2[0], cl2[1], cl2[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size    

class L3_Gridlayout(GridLayout):

    def __init__(self, **kwargs):
        super(L3_Gridlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl3[0], cl3[1], cl3[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size    
    
class L1_Floatlayout(FloatLayout):

    def __init__(self, **kwargs):
        super(L1_Floatlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl1[0], cl1[1], cl1[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


class L2_Floatlayout(FloatLayout):
    
    def __init__(self, **kwargs):
        super(L2_Floatlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl2[0], cl2[1], cl2[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    

    
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size    

class L3_Floatlayout(FloatLayout):
    
    def __init__(self, **kwargs):
        super(L3_Floatlayout, self).__init__(**kwargs)
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            Color(cl3[0], cl3[1], cl3[2], 1) # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)    
