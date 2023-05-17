import pygame as pg
from pygame.math import Vector2

display_size: Vector2 = Vector2(140,100)
display_scale: int = 5

bracket_size: Vector2 = Vector2(4,16)
bracket_speed: int = 40
bracket_color: str = "#FFFFFF"

ball_start_position: Vector2 = display_size / 2
ball_size: Vector2 = Vector2(4, 4)
ball_speed: int = 30
ball_color: str = "#FFFFFF"

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
    def __init__(self):
        global display_scale
        global ball_size
        global ball_start_position

        self._rect = pg.Rect(ball_start_position, ball_size)
        self._drawable_rect = pg.Rect(ball_start_position * display_scale, ball_size * display_scale)
        self._direction = Vector2(1,1)

    @property
    def position(self):
        return self._rect.topleft

    @position.setter
    def position(self, new_position):
        global display_scale

        self._rect.topleft = new_position
        self._drawable_rect.topleft = new_position * display_scale

    def update(self, delta_time: float):
        global ball_speed
        self.position += self._direction * ball_speed * delta_time

    def render(self):
        global display
        global ball_color

        pg.draw.rect(display, ball_color, self._drawable_rect)

    def collided(self, bracket: Bracket) -> bool:
        return self._rect.colliderect(Bracket.hitbox)

clock = pg.time.Clock()

exit = False

player_bracket = Bracket(Vector2(1,1))
ball = Ball()

objects = [player_bracket, ball]

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

    ball.update(delta_time)

    # render

    display.fill((0,0,0))

    for obj in objects:
        obj.render()

    pg.display.update()

pg.quit()