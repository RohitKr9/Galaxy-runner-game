from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

import random
from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, Clock
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.clock import Clock


class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    #from spaceship_path_check import is_out

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    NB_V_LINES = 4
    NB_H_LINES = 10
    NB_TILES= 5
    V_LINES_SPACING = 0.2 #isko hum percetage me rakhe hai

    spaceship = None
    spaceship_width = 0
    spaceship_height = 0
    spaceship_base_y = 0

    lines = []
    horizontal_lines = []
    tiles = []
    tile_index = []

    curr_offset_y = 0
    curr_offset_x = 0
    curr_loop_count = 0
    speed_x_const = 6
    speed_y_const = 0.3

    speed_x_sign = 1
    speed_x = 0
    speed_y = 0
    x_flag = False
    
    #tile_index_flag = False #this flag is for updating the tile_index list when there is change in curr_loop_count

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_game, 0)

    def initialize_game(self, dt):
            print(f"Window size after delay: {self.width} x {self.height}")

            print("inside __init__")
            self.init_vetical_lines()
            self.init_horizontal_lines()
            self.init_tiles()
            self.generate_tile_index()
            self.init_spaceship()

            self.spaceship_width = 0.05 * self.width
            self.spaceship_height = 0.07 * self.height
            self.spaceship_base_y = 0.04 * self.height
            print(f"Window size: {self.width} x {self.height}")
            self.update_spaceship()

            if platform in ['win', 'linux', 'macosx']:
                self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
                self._keyboard.bind(on_key_down=self.on_keyboard_down)
                self._keyboard.bind(on_key_up=self.on_keyboard_up)

            Clock.schedule_interval(self.update, 1.0 / 6.0)

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

    def init_spaceship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.spaceship = Triangle()

    def update_spaceship(self):
        mid_x = self.width/2
        mid_y = self.spaceship_base_y + self.spaceship_height
        x1 = mid_x - self.spaceship_width/2
        x2 = mid_x + self.spaceship_width/2
        y1 = y2 = self.spaceship_base_y
        #print(f"mid_lrngth___{self.width/2}")
        #print(f"{x1}, {y1}, {mid_x}, {mid_y}, {x2}, {y2}")
        self.spaceship.points = [x1, y1, mid_x, mid_y, x2, y2]
    
    def get_line_x_from_index(self,index):    #this will return coordinate_x of that line at that index of index system
        spacing = self.V_LINES_SPACING * self.width                   #for 6 vertical lines index will be (-2 -1 0 1 2 3)
        coordinate_x_index_0 = self.center_x - spacing/2
        return coordinate_x_index_0 + (index * spacing) #- self.curr_offset_x
    
    def get_line_y_from_index(self, index): 
        spacing = self.height / (self.NB_H_LINES + 1) #ye spacing hai horizontals line ka  
        return spacing * index #- self.curr_offset_y  #here index is always positive, we are taking it as 0 1 2 3 4 5...

    def get_quad_xy_from_index(self, x, y):
        t_x = self.get_line_x_from_index(x) - self.curr_offset_x
        t_y = self.get_line_y_from_index(y) - self.curr_offset_y
        return t_x, t_y

    def update_vertical_lines(self):
        offset = -(int(self.NB_V_LINES / 2))
        spacing = self.V_LINES_SPACING * self.width
        index_left = int(-(self.NB_V_LINES / 2) + 1)
        index_right = int(self.NB_V_LINES / 2)
        for i in range(index_left, index_right+1):
    
            x1 = self.get_line_x_from_index(i) - self.curr_offset_x
           
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

            tr_x1 = self.get_line_x_from_index(index_left) - self.curr_offset_x
            tr_x2 = self.get_line_x_from_index(index_right) - self.curr_offset_x
            tr_y1 = self.get_line_y_from_index(i) - self.curr_offset_y
            tr_y2 = self.get_line_y_from_index(i) - self.curr_offset_y

            tr_x1, tr_y1 = self.transform(tr_x1, tr_y1)
            tr_x2, tr_y2 = self.transform(tr_x2, tr_y2)
            self.horizontal_lines[i].points = [tr_x1, tr_y1, tr_x2, tr_y2]
            self.horizontal_spacing = self.perspective_point_y - tr_y1         #Ye horizontal_spacing kya kar rha hai
 
    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.NB_TILES):
                self.tiles.append(Quad())

    def generate_tile_index(self):
        for i in range(self.NB_TILES):
            self.tile_index.append((0,i))

    def add_tile_on_motion(self):
        for i in range(self.NB_TILES):
            if self.tiles[i].points[3] < 0:
                del self.tile_index[0]

        
        index_left = int(-(self.NB_V_LINES / 2) + 1)
        index_right = int(self.NB_V_LINES / 2) - 1

        for i in range(self.NB_TILES - len(self.tile_index)):
            
            base_tile_index = self.tile_index[-1]
            diff = self.tile_index[-1][0] - self.tile_index[-3][0]
            #we will check boundry condition
            if base_tile_index[0] == index_left:
                if diff == 0: 
                    r = random.randint(0, 1)
                    index = (0, 0)
                    if r == 0: 
                        index = (base_tile_index[0], base_tile_index[1] + 1 )
                    else : 
                        index = (base_tile_index[0] + 1, base_tile_index[1] )
                    
                    self.tile_index.append(index)
                else :
                    self.tile_index.append((base_tile_index[0], base_tile_index[1] + 1 )) 

            elif base_tile_index[0] == index_right:
                if diff == 0: 
                    r = random.randint(-1, 0)
                    index = (0, 0)
                    if r == 0: 
                        index = (base_tile_index[0], base_tile_index[1] + 1 )
                    else : 
                        index = (base_tile_index[0] - 1, base_tile_index[1] )
                    
                    self.tile_index.append(index)
                else :
                    self.tile_index.append((base_tile_index[0], base_tile_index[1] + 1 )) 
            
            else:
                if diff == 0: 
                    r = random.randint(-1, 1)
                    index = (0, 0)
                    if r == 0: 
                        index = (base_tile_index[0], base_tile_index[1] + 1 )
                    elif r == -1: 
                        index = (base_tile_index[0] - 1, base_tile_index[1] )
                    else : 
                        index = (base_tile_index[0] + 1, base_tile_index[1] )
                
                    self.tile_index.append(index)

                else:
                    self.tile_index.append((base_tile_index[0], base_tile_index[1] + 1 )) 

    def get_tile_extremes(self):

        spaceship_base = self.spaceship_base_y
        left = self.width/2 - 30
        right = self.width/2 + 30
       
        for i in range(3):
           
            y, Y = self.tiles[i].points[1], self.tiles[i].points[3]
            if(spaceship_base < Y and spaceship_base > y):
                
                left = min(self.tiles[i].points[0], left)
                right = max(self.tiles[i].points[6], right)
        return left, right

    def is_out(self):
        ship_left = self.spaceship.points[0]
        ship_right = self.spaceship.points[4]

        left, right = self.get_tile_extremes()

        #print(f"Ship Left: {ship_left}, Ship Right: {ship_right}")
        print(f"Screen Left: {left}, Screen Right: {right}")

        if ship_left < left or ship_right > right :
            return True
        return  False

    def update_tiles(self):
        for i in range(self.NB_TILES):
            tile = self.tiles[i]
            ti_x = self.tile_index[i][0]
            ti_y = self.tile_index[i][1]- self.curr_loop_count 

            x1, y1 = self.get_quad_xy_from_index(ti_x, ti_y)
            x2, y2 = self.get_quad_xy_from_index(ti_x, ti_y + 1)
            x3, y3 = self.get_quad_xy_from_index(ti_x + 1, ti_y + 1)
            x4, y4 = self.get_quad_xy_from_index(ti_x + 1, ti_y)

            x1, y1 = self.transform(x1, y1)
            x2, y2 = self.transform(x2, y2)
            x3, y3 = self.transform(x3, y3)
            x4, y4 = self.transform(x4, y4)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]


    def update(self, dt):

        self.speed_x = (self.speed_x_const/900) * self.width
        self.speed_y = (self.speed_y_const/400) * self.height

        self.spaceship_width = 0.05 * self.width
        self.spaceship_height = 0.07 * self.height
        self.spaceship_base_y = 0.04 * self.height

        if self.is_out() :
            print ("Game Over")
            self.speed_y_const = 0

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_spaceship()
        self.curr_offset_y += self.speed_y

        if self.x_flag == True:
            self.curr_offset_x += self.speed_x_sign * self.speed_x

        spacing = self.height / (self.NB_H_LINES + 1)

        if self.curr_offset_y > spacing: 
            self.curr_offset_y = 0
            self.curr_loop_count += 1
            self.add_tile_on_motion()
            print(self.tile_index[0][0])
            print(self.tile_index[1][0])
            print(self.get_tile_extremes())
            print("  .....   ")

        # if self.curr_loop_count >= self.NB_TILES:    #Is condition k karan apna infinite tile generation fail ho rha hoga
        #     self.curr_loop_count = 0

class GalaxyApp(App):
    pass

GalaxyApp().run()
    
