
def transform(self, x, y):
    return self.transform_2D(x, y)
    #return self.transform_perspective(x, y)
    
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