from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, Clock
from kivy.graphics import Color,Line


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    NB_V_LINES = 14
    NB_H_LINES = 7
    V_LINES_SPACING = 0.2 #isko hum percetage me rakhe hai

    lines = []
    horizontal_lines = []

    curr_offset_y = 0
    curr_offset_x = 0
    speed_x = 12
    x_flag = False
    speed_y = 2

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("inside __init__")
        self.init_vetical_lines()
        self.init_horizontal_lines()

        if platform in ['win', 'linux', 'macosx']:
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.x_flag = True

        if keycode[1] == 'a':
            self.speed_x = -(abs(self.speed_x))
        elif keycode[1] == 's':
            self.speed_x = abs(self.speed_x)
        elif keycode[1] == 'left':
            self.speed_x = -(abs(self.speed_x))
        elif keycode[1] == 'right':
            self.speed_x = abs(self.speed_x)
        return True
    
    def on_keyboard_up(self, keyboard, keycode):
        self.x_flag = False
        return True

    def on_size(self, *args):
        self.perspective_point_x = self.width / 2
        self.perspective_point_y = self.height * 0.75

    def on_perspective_point_x(self, widget, value):
        pass

    def on_perspective_point_y(self, widget, value):
        pass

    def init_vetical_lines(self):
        print("inside init_vertical")
        with self.canvas:
            Color(1,1,1)
            #yha hum sirf line ko initiate karege, update agle fun me karege
            for i in range(self.NB_V_LINES):
                self.lines.append(Line())

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.NB_H_LINES):
                self.horizontal_lines.append(Line())
    
    def update_vertical_lines(self):
        offset = -(int(self.NB_V_LINES / 2))
        spacing = self.V_LINES_SPACING * self.width
        for i in range(self.NB_V_LINES):
            x1 = self.center_x + offset * spacing
            x1 += spacing/2 #ye isleye keye hai kyon ki hume sadak bicho bich chayeye na ki 2 lane sadak (nahi to gadi kha rakhoge, left meya right me)

            tr_x1, tr_y1 = self.transform(x1, 0)
            tr_x2, tr_y2 = self.transform(x1,self.height)
            tr_x1 -= self.curr_offset_x
            #tr_x2 -= self.curr_offset_x
            self.lines[i].points = [tr_x1, tr_y1, tr_x2, tr_y2]
            offset += 1

    def update_horizontal_lines(self):
        spacing = self.height / (self.NB_H_LINES + 1) #ye spacing hai horizontals line ka
        num = 1
        
        spacing_of_vertical_lines = self.width * self.V_LINES_SPACING
        
        for i in range(self.NB_H_LINES):
            tr_x1 = self.center_x - (spacing_of_vertical_lines * (self.NB_V_LINES / 2)) + spacing_of_vertical_lines / 2 
            tr_x2 = self.center_x + (spacing_of_vertical_lines * ((self.NB_V_LINES / 2)-1)) + spacing_of_vertical_lines / 2 
            tr_x1 -= self.curr_offset_x
            tr_x2 -= self.curr_offset_x
            tr_y1 = spacing * num - self.curr_offset_y
            tr_y2 = spacing * num - self.curr_offset_y

            tr_x1, tr_y1 = self.transform(tr_x1, tr_y1)
            tr_x2, tr_y2 = self.transform(tr_x2, tr_y2)
            self.horizontal_lines[i].points = [tr_x1, tr_y1, tr_x2, tr_y2]
            num += 1
            self.horizontal_spacing = self.perspective_point_y - tr_y1
            
        #print("this is horixonntal spacing"+str(self.horizontal_spacing))


    #now we will write transform function
    def transform(self, x, y):
        #return self.transform_2D(x, y)
        return self.transform_perspective(x, y)
    
    def transform_2D(self, x, y):
        return int(x), int(y)
    
    def transform_perspective(self, x, y): #sara calculation yha hai(DHYAN SE)

        linear_y = y * self.perspective_point_y/self.height

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - linear_y
        factor_y = diff_y/self.perspective_point_y
        factor_y = pow(factor_y, 3)
        tr_x = self.perspective_point_x + diff_x * factor_y # yha x to sahi transform ho gya par y transformation k leye hum expontial function use karege taki nazdik ka bda aur dur ka chota dekhe
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

        return int(tr_x), int(tr_y)
    
    def on_touch_down(self, touch):
        self.x_flag = True
        if touch.x < self.width/2:
            self.speed_x = -(abs(self.speed_x))
        else :
            self.speed_x = abs(self.speed_x)

    def on_touch_up(self, touch):
        self.x_flag = False
    
    def update(self, dt):
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.curr_offset_y += self.speed_y

        if self.x_flag == True:
            self.curr_offset_x += self.speed_x

        spacing = self.height / (self.NB_H_LINES + 1)

        if self.curr_offset_y > spacing: self.curr_offset_y = 0



class GalaxyApp(App):
    pass

GalaxyApp().run()
    