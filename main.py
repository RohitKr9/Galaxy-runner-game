from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, Clock
from kivy.graphics import Color,Line, Quad


class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    NB_V_LINES = 14
    NB_H_LINES = 10
    NB_TILES= 6
    V_LINES_SPACING = 0.2 #isko hum percetage me rakhe hai

    lines = []
    horizontal_lines = []
    tiles = []

    tile_coordinates = []

    curr_offset_y = 0
    curr_offset_x = 0
    curr_loop_count = 0
    speed_x = 5
    x_flag = False
    speed_y = 1

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("inside __init__")
        self.init_vetical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.generate_tile_coordinate()

        if platform in ['win', 'linux', 'macosx']:
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_size(self, *args):
        self.perspective_point_x = self.width / 2
        self.perspective_point_y = self.height * 0.75

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

    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.NB_TILES):
                self.tiles.append(Quad())

    def get_line_x_from_index(self,index):    #this will return coordinate_x of that line at that index of index system
        spacing = self.V_LINES_SPACING * self.width                   #for 6 vertical lines index will be (-2 -1 0 1 2 3)
        coordinate_x_index_0 = self.center_x - spacing/2
        return coordinate_x_index_0 + (index * spacing) - self.curr_offset_x
    
    def get_line_y_from_index(self, index): 
        spacing = self.height / (self.NB_H_LINES + 1) #ye spacing hai horizontals line ka  
        return spacing * index - self.curr_offset_y  #here index is always positive, we are taking it as 0 1 2 3 4 5...

    def get_quad_xy_from_index(self, x, y):
        ti_x = self.get_line_x_from_index(x)
        ti_y = self.get_line_y_from_index(y)
        return ti_x, ti_y

    def update_vertical_lines(self):
        offset = -(int(self.NB_V_LINES / 2))
        spacing = self.V_LINES_SPACING * self.width
        index_left = int(-(self.NB_V_LINES / 2) + 1)
        index_right = int(self.NB_V_LINES / 2)
        for i in range(index_left, index_right+1):
    
            x1 = self.get_line_x_from_index(i)
           
            tr_x1, tr_y1 = self.transform(x1, 0)
            tr_x2, tr_y2 = self.transform(x1,self.height)
            #tr_x1 -= self.curr_offset_x

            self.lines[i - index_left].points = [tr_x1, tr_y1, tr_x2, tr_y2]

    def update_horizontal_lines(self):
        
        for i in range(self.NB_H_LINES):
            # tr_x1 = self.center_x - (spacing_of_vertical_lines * (self.NB_V_LINES / 2)) + spacing_of_vertical_lines / 2 
            # tr_x2 = self.center_x + (spacing_of_vertical_lines * ((self.NB_V_LINES / 2)-1)) + spacing_of_vertical_lines / 2 
            # tr_x1 -= self.curr_offset_x
            # tr_x2 -= self.curr_offset_x

            index_left = int(-(self.NB_V_LINES / 2) + 1)
            index_right = int(self.NB_V_LINES / 2)

            tr_x1 = self.get_line_x_from_index(index_left)
            tr_x2 = self.get_line_x_from_index(index_right)
            tr_y1 = self.get_line_y_from_index(i)
            tr_y2 = self.get_line_y_from_index(i)

            tr_x1, tr_y1 = self.transform(tr_x1, tr_y1)
            tr_x2, tr_y2 = self.transform(tr_x2, tr_y2)
            self.horizontal_lines[i].points = [tr_x1, tr_y1, tr_x2, tr_y2]
            self.horizontal_spacing = self.perspective_point_y - tr_y1         #Ye horizontal_spacing kya kar rha hai

    def generate_tile_coordinate(self):
        for i in range(self.NB_TILES):
            self.tile_coordinates.append((0,i))

    def update_tile_coordinate(self):       #ye function infinite generate karne me help karega
        print(self.curr_loop_count)
        #self.tile_coordinates[self.curr_loop_count - 2] = (0, self.NB_TILES)     #yha kuch gadbad dikh rha hai
        self.update_tile_coordinate_helper()

    def update_tile_coordinate_helper(self):  #this you have written today

        temp_count = self.curr_loop_count
        while(temp_count != 0):    #this is the logic of rotating of array by temp_count 
            k1 = 0
            k2 = self.tile_coordinates[self.NB_TILES - 1]
            for i in range(self.NB_TILES-1, 0, -1):
                k1 = self.tile_coordinates[self.NB_TILES - 2]
                self.tile_coordinates[self.NB_TILES - 2] = k2
                k2 = k1
            temp_count -= 1

    def update_tiles(self):
        for i in range(self.NB_TILES):
            tile = self.tiles[i]
            t_x = self.tile_coordinates[i][0]
            t_y = self.tile_coordinates[i][1] - self.curr_loop_count #yha tu minus kyon kar rha hai curr_loop_count, ye tumahra tile movement tak koi help nahi karega
                                                                     # yhe pe fatega, Dhyan rakhna
            x1, y1 = self.get_quad_xy_from_index(t_x, t_y)
            x2, y2 = self.get_quad_xy_from_index(t_x, t_y + 1)
            x3, y3 = self.get_quad_xy_from_index(t_x + 1, t_y + 1)
            x4, y4 = self.get_quad_xy_from_index(t_x + 1, t_y)

            x1, y1 = self.transform(x1, y1)
            x2, y2 = self.transform(x2, y2)
            x3, y3 = self.transform(x3, y3)
            x4, y4 = self.transform(x4, y4)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update(self, dt):
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_tile_coordinate()   # ye kyon call kar rahe ho
        self.curr_offset_y += self.speed_y

        if self.x_flag == True:
            self.curr_offset_x += self.speed_x

        spacing = self.height / (self.NB_H_LINES + 1)

        if self.curr_offset_y > spacing: 
            self.curr_offset_y = 0
            self.curr_loop_count += 1
            #self.update_tile_coordinate()     ----> hume yha se isko trigger karna chayeye, jab bhi mera curr_loop_count update ho tab yr trigger ho

        if self.curr_loop_count >= self.NB_TILES:    #Is condition k karan apna infinite tile generation fail ho rha hoga
            self.curr_loop_count = 0

class GalaxyApp(App):
    pass

GalaxyApp().run()
    
