import pygame as pg

display_size: tuple = (80,40)
display_scale: int = 10

display: pg.display = pg.display.set_mode(pg.math.Vector2(display_size) * display_scale)

clock: pg.time.Clock = pg.time.Clock()

game = True

while game:
    delta_time = clock.tick(40) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
            break

pg.quit()