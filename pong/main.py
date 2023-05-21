import pygame as pg
from pygame.math import Vector2

display_size: Vector2 = Vector2(140,100)
display_scale: int = 5

bracket_size: Vector2 = Vector2(4,16)
bracket_speed: int = 30
bracket_color: str = "#FFFFFF"

ball_start_position: Vector2 = display_size / 2
ball_size: Vector2 = Vector2(4, 4)
ball_speed: int = 30
ball_acceleration: int = 1
ball_color: str = "#FFFFFF"

display = pg.display.set_mode(display_size * display_scale)

class Bracket:
    def __init__(self, initial_position: Vector2):
        global bracket_size
        global display_scale
        self._rect = pg.Rect(initial_position, bracket_size)
        self._drawable_rect = pg.Rect(initial_position * display_scale, bracket_size * display_scale)
        self._position = initial_position
    
    @property
    def position(self) -> Vector2:
        return self._position
    
    @position.setter
    def position(self, new_position: Vector2):
        global display_size
        global display_scale
        
        if new_position[0] < 0:
            new_position[0] = 0
        elif new_position[0] + self._rect.width > display_size[0]:
            new_position[0] = display_size[0] - self._rect.width
            
        if new_position[1] < 0:
            new_position[1] = 0
        elif new_position[1] + self._rect.height > display_size[1]:
            new_position[1] = display_size[1] - self._rect.height

        self._position = new_position
        self._rect.topleft = new_position
        self._drawable_rect.topleft = new_position * display_scale
    
    def render(self):
        global display
        global bracket_color
        pg.draw.rect(display, bracket_color, self._drawable_rect)

    @property
    def y(self) -> float:
        return self._position[1]
    
    @y.setter
    def y(self, new_y):
        global display_size
        global display_scale

        self.position = Vector2(self._position[0], new_y)

    @property
    def centery(self) -> float:
        return self.position[1] + (self._rect.height / 2)
    
    @centery.setter
    def centery(self, new_y):
        global display_size
        global display_scale

        self.position = Vector2(self.position[0], new_y - (self._rect.height / 2))


    @property
    def hitbox(self) -> pg.rect:
        return self._rect


class Ball:
    def __init__(self):
        global display_scale
        global ball_size
        global ball_start_position
        global ball_speed

        self._rect = pg.Rect(ball_start_position, ball_size)
        self._drawable_rect = pg.Rect(ball_start_position * display_scale, ball_size * display_scale)
        self._direction = Vector2(1, 1)
        self._speed = ball_speed

    @property
    def position(self) -> Vector2:
        return self._rect.topleft

    @position.setter
    def position(self, new_position: Vector2):
        global display_scale

        self._rect.topleft = new_position
        self._drawable_rect.topleft = new_position * display_scale

    def update(self, delta_time: float):
        global ball_acceleration
        global ball_size
        global bracket_size
        global display_size

        if self.position[0] < bracket_size[0] or self.position[0] + ball_size.x > display_size[0] - bracket_size[0]:
            self.reset_ball()

        if self.position[1] <= 0 or self.position[1] + ball_size.y >= display_size[1]:
            self.invert_y()

        self.position += self._direction * self._speed * delta_time

    def render(self):
        global display
        global ball_color

        pg.draw.rect(display, ball_color, self._drawable_rect)

    def collided(self, bracket: Bracket) -> bool:
        collision: bool = self._rect.colliderect(bracket.hitbox)
        
        if collision:
            global ball_acceleration
            self._speed += ball_acceleration
        
        return collision
    
    def invert_x(self):
        self._direction = Vector2(-self._direction.x, self._direction.y)
    
    def invert_y(self):
        self._direction = Vector2(self._direction.x, -self._direction.y)
    
    def invert_direction(self):
        self._direction = Vector2(-self._direction.x, -self._direction.y)

    def reset_ball(self):
        global ball_start_position
        global ball_speed

        self._speed = ball_speed
        self.position = ball_start_position
        self.invert_direction()

clock = pg.time.Clock()

exit = False

bracket_1 = Bracket(Vector2(0, 1))
bracket_2 = Bracket(Vector2(display_size[0] - bracket_size[0], 1))
ball = Ball()

objects = [ball, bracket_1, bracket_2]

while not exit:
    delta_time = clock.tick(30)/1000
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True

    # player bracket movement

    keys = pg.key.get_pressed()
    
    if keys[pg.K_w] and not keys[pg.K_s]:
        bracket_1.y -= bracket_speed * delta_time
    elif keys[pg.K_s] and not keys[pg.K_w]:
        bracket_1.y += bracket_speed * delta_time

    if keys[pg.K_UP] and not keys[pg.K_DOWN]:
        bracket_2.y -= bracket_speed * delta_time
    elif keys[pg.K_DOWN] and not keys[pg.K_UP]:
        bracket_2.y += bracket_speed * delta_time

    # ball logic

    if ball.collided(bracket_1):
        ball.position = Vector2(bracket_size[0], ball.position[1])
        ball.invert_x()
    elif ball.collided(bracket_2):
        ball.position = Vector2(display_size[0] - bracket_size[0] - ball_size[0], ball.position[1])
        ball.invert_x()

    ball.update(delta_time)

    # render

    display.fill((0,0,0))

    for obj in objects:
        obj.render()

    pg.display.update()

pg.quit()