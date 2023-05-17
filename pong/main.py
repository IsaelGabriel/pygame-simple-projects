import pygame as pg
from pygame.math import Vector2

display_size: Vector2 = Vector2(70,50)
display_scale: int = 10

bracket_size = Vector2(2,8)
bracket_speed = 20
bracket_color = "#FFFFFF"


display = pg.display.set_mode(display_size * display_scale)

class Bracket:
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

    @property
    def y(self):
        return self._rect.y
    
    @y.setter
    def y(self, new_y):
        global display_scale
        self._rect.y = new_y
        self._drawable_rect.y = new_y * display_scale

    @property
    def hitbox(self):
        return self._rect


class Ball:
    def __init__(self, position: Vector2, size: Vector2, speed: int):
        global display_scale

        self._rect = pg.Rect(position, size)
        self._drawable_rect = pg.Rect(position * display_scale, size * display_scale)
        self._direction = Vector2(1,1)
        self._speed = 15

    @property
    def position(self):
        return self._rect.topleft

    @position.setter
    def position(self, new_position):
        global display_scale

        self._rect.topleft = new_position
        self._drawable_rect.topleft = new_position * display_scale

    def update_ball(self, delta_time: float):
        self.position = self._direction * self._speed * delta_time

    def collided(self, bracket: Bracket) -> bool:
        return self._rect.colliderect(Bracket.hitbox)

clock = pg.time.Clock()

exit = False

player_bracket = Bracket(Vector2(1,1))

objects = [player_bracket]

while not exit:
    delta_time = clock.tick(30)/1000
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True

    # object logic

    keys = pg.key.get_pressed()
    
    if keys[pg.K_UP] and not keys[pg.K_DOWN]:
        player_bracket.y -= bracket_speed * delta_time
    elif keys[pg.K_DOWN] and not keys[pg.K_UP]:
        player_bracket.y += bracket_speed * delta_time

    # render

    display.fill((0,0,0))

    for obj in objects:
        obj.render()

    pg.display.update()

pg.quit()