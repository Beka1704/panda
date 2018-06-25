from datetime import datetime

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy.clock import Clock
from Kivy_App import body

class Clock_Display(body.L1_Gridlayout):
    def __init__(self, **kwargs):
        super(Clock_Display, self).__init__(**kwargs)
        self.cols = 1
        self.row = 2
        self.clock = Label(text=datetime.now().time().strftime('%H:%M:%S'),font_size='84sp')
        self.date = Label(text=datetime.now().date().isoformat(),font_size='62sp')
        self.add_widget(self.clock)
        self.add_widget(self.date)
        self.spacing = [5,5]
        Clock.schedule_interval(self.update, 1.0)
        
    def update(self, dt):
        self.clock.text = text=datetime.now().time().strftime('%H:%M')
        self.date.text =datetime.now().date().isoformat()

        
