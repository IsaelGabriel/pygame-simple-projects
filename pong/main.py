import pygame as pg
from pygame.math import Vector2

display_size: Vector2 = Vector2(70,50)
display_scale: int = 10

bracket_size = Vector2(2,8)
bracket_speed = 5
bracket_color = "#FFFFFF"


display = pg.display.set_mode(display_size * display_scale)

class bracket:
    def __init__(self, initial_position: Vector2):
        global bracket_size
        global display_scale
        self._rect = pg.Rect(initial_position, bracket_size)
        self._drawable_rect = pg.Rect(initial_position * display_scale, bracket_size * display_scale)
    
    @property
    def position(self):
        return self._rect.topleft
    
    @position.setter
    def position(self, new_position: Vector2):
        global display_scale
        self._rect.topleft = new_position
        self._drawable_rect.topleft = new_position * display_scale
    
    def render(self):
        global display
        global bracket_color
        pg.draw.rect(display, bracket_color, self._drawable_rect)



clock = pg.time.Clock()


exit = False

test_bracket = bracket(Vector2(2,2))

while not exit:
    delta_time = clock.tick(30)/1000
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True

    display.fill((0,0,0))

    test_bracket.render()

    pg.display.update()

pg.quit()