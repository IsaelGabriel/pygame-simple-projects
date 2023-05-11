import pygame as pg

display = pg.display.set_mode((400,400))

exit = False

while not exit:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                exit = True

    pg.display.update()

pg.quit()