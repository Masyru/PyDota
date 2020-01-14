from random import randrange

import sys


import pygame as pg
from pygame.math import Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)

    def handle_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_F11:
                sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.vel.x = 5
            elif event.key == pg.K_a:
                self.vel.x = -5
            elif event.key == pg.K_w:
                self.vel.y = -5
            elif event.key == pg.K_s:
                self.vel.y = 5
        elif event.type == pg.KEYUP:
            if event.key == pg.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pg.K_w:
                self.vel.y = 0
            elif event.key == pg.K_s:
                self.vel.y = 0

    def update(self):
        # Move the player.
        self.pos += self.vel
        self.rect.center = self.pos

    def add_screen(self, screen):
        self.screen = screen


class Camera:
    def __init__(self, focused_player):
        self.player = focused_player
        self.screen_size = pg.display.Info().current_w, pg.display.Info().current_h
        x, y = self.screen_size
        self.camera = Vector2(self.screen_size)

    def count_camera_pos(self):
        x, y = self.screen_size
        heading = self.player.pos - self.camera
        # Follow the player with the camera.
        # Move the camera by a fraction of the heading vector's length.
        self.camera += heading * 0.05
        # The actual offset that we have to add to the positions of the objects.
        offset = -self.camera + Vector2(x // 2, y // 2)  # + 400, 300 to center the player.
        self.player.screen.fill((30, 30, 30))
        # Blit all objects and add the offset to their positions.
        for background_rect in self.background_rects:
            topleft = background_rect.topleft + offset
            pg.draw.rect(self.player.screen, (200, 50, 70), (topleft, background_rect.size))

        self.player.screen.blit(self.player.image, self.player.rect.topleft + offset)

    def add_rects(self, rects):
        self.background_rects = rects


def create_map(width, height):
    pass


def main():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((60, 3300), all_sprites)
    player.add_screen(screen)
    camera = Camera(player)

    background_rects = [pg.Rect(randrange(-3000, 3001), randrange(-3000, 3001), 20, 20)
                        for _ in range(500)]
    camera.add_rects(background_rects)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            player.handle_event(event)

        all_sprites.update()
        # A vector that points from the camera to the player.
        # heading = player.pos - camera
        # # Follow the player with the camera.
        # # Move the camera by a fraction of the heading vector's length.
        # camera += heading * 0.05
        # # The actual offset that we have to add to the positions of the objects.
        # offset = -camera + Vector2(400, 300)  # + 400, 300 to center the player.
        camera.count_camera_pos()

        pg.display.flip()
        clock.tick(60)


main()

pg.quit()