""" GameSprites.py 
    ALPHA sprint for platform
    game.
    Nate Wilson
"""

import pygame
import random
from pygame.math import Vector2 as vector

# The Player class
class HeroCat(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("moose.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rawr_sound = pygame.mixer.Sound("rawr.ogg")
        self.eat_sound = pygame.mixer.Sound("nomchomp.ogg")
        self.rect.center = (400,400)
        self.pos = vector(self.rect.center)
        self.vel = vector(0,0)
        self.acc = vector(0,0)
        self.lives = 3
        
    def jump(self):
        self.vel.y = -30
        
    def update(self, screen):
        self.acc = vector(0,2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -1
        if keys[pygame.K_RIGHT]:
            self.acc.x = 1
        
        # equations for moving
        self.acc.x += self.vel.x * -0.12
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        # Wrap around screen
        if self.pos.x > screen.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screen.get_width()

    def rawr(self):
        self.rawr_sound.play()

    def eat(self):
        self.eat_sound.play()


# The Enemy class
class EnemyCat(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        # my own artwork
        self.image = pygame.image.load("enemy.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,screen.get_width())
        self.rect.centery = 0
        self.dy = random.randint(2,5)
        
    def update(self, screen):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.rect.centerx = random.randint(0,screen.get_width())
            self.rect.centery = 0

# The Platform
class Platforms(pygame.sprite.Sprite):
    def __init__(self, screen,length, width,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((length, width))
        self.image.fill((100,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
# The Treat
class Treats(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 100, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,screen.get_width())
        self.rect.centery = random.randint(45,400)
        
        

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        self.score = 0
        self.font = pygame.font.SysFont("Comic Sans MS",40)

    def update(self,screen):
        self.text = "Lives: %d Treats: %d / 10"%(self.lives, self.score)
        self.image = self.font.render(self.text,1, (255,0,0))
        self.rect = self.image.get_rect()
