def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    self.x_flag = True

    if keycode[1] == 'a':
        self.speed_x_sign = -(abs(self.speed_x_sign))
    elif keycode[1] == 'd':
        self.speed_x_sign = abs(self.speed_x_sign)
    elif keycode[1] == 'left':
        self.speed_x_sign = -(abs(self.speed_x_sign))
    elif keycode[1] == 'right':
        self.speed_x_sign = abs(self.speed_x_sign)
    return True
    
def on_keyboard_up(self, keyboard, keycode):
    self.x_flag = False
    return True

def on_touch_down(self, touch):
    self.x_flag = True
    if touch.x < self.width/2:
        self.speed_x_sign = -(abs(self.speed_x_sign))
    else :
        self.speed_x_sign = abs(self.speed_x_sign)

def on_touch_up(self, touch):
    self.x_flag = False