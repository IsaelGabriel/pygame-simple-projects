import pygame as pg
from pygame.math import Vector2 as vec

display_size: tuple = (80,40)
display_scale: int = 10

reduced_surface: pg.surface = pg.Surface(display_size)
display: pg.display = pg.display.set_mode(vec(display_size) * display_scale)
display_rect = pg.Rect((0,0), vec(display_size) * display_scale)

clock: pg.time.Clock = pg.time.Clock()

ground_height = 5

player: dict = {
    "size": (5, 10),
    "jump_force": 5.0,
    "color": "#00FF00"
}

player["position"] = vec(5, display_size[1] - ground_height - player["size"][1])
player["rect"] = pg.Rect(player["position"], player["size"])

game = True

while game:
    delta_time = clock.tick(40) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
            break

    display.fill((0,0,0))

    pg.draw.rect(reduced_surface, player["color"], player["rect"])
    display.blit(pg.transform.scale(reduced_surface, display_rect.size), display_rect)

    pg.display.update()

pg.quit()