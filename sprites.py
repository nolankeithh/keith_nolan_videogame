import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import os
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'theBird.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0
        # assign player a certain amount of health until reaches death...
        self.hitpoints = 50
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        # collide function betwen sprites
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        ghits = pg.sprite.collide_rect(self, self.game.ground)
        if hits or ghits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
        # when the sprite makes any contact with mob class it will lose 10 hipoints
        mobhits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        if mobhits:
            self.hitpoints -= 10
            if self.hitpoints == 0:
                # end game once hit 0 health
                pg.quit()

    def update(self):
        # CHECKING FOR COLLISION WITH MOBS HERE>>>>>
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos


# platforms

class Platform(Sprite):
    # setup platforms for player to reach (move back and forth)
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            # assign speed for the platforms horizontally
            self.speed = 3
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
# creating mob class to assign variables to
class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.game = game
        #displayed image for mobs
        self.image = pg.image.load(os.path.join(img_folder, 'thePig.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
    def update(self):
        if self.rect.x < self.game.player.rect.x:
            self.rect.x +=1
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -=1
        if self.rect.y < self.game.player.rect.y:
            self.rect.y +=1
        if self.rect.y > self.game.player.rect.y:
            self.rect.y -=1  
    