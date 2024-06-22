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

def on_touch_down(self, touch):
    self.x_flag = True
    if touch.x < self.width/2:
        self.speed_x = -(abs(self.speed_x))
    else :
        self.speed_x = abs(self.speed_x)

def on_touch_up(self, touch):
    self.x_flag = False