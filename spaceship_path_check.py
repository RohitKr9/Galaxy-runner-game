def get_tile_extremes(self):
    left = self.tiles[0].points[0]
    right = self.tiles[0].points[6]
    return left, right

def is_out(self):
    ship_left = self.spaceship.points[0]
    ship_right = self.spaceship.points[4]

    left, right = self.get_tile_extremes()

    if ship_left < left or ship_right > right :
        return True
    return  False