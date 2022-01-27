import pygame, sys
from pygame.locals import *
import random, time

#creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
ENEMY_MOVEMENT = [-20, 20]


class Player_Ship(pygame.sprite.Sprite):
    def __init__(self, ID):

        #attributes for player ship
        self.health = 3
        self.ID = ID

        #drawing simple blue square for player
        #note I will leave the different types of ships as colored rectangles for now
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 450:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -15)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,15)
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-15, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(15, 0)

#Enemy class and children

class Enemy_Ship(pygame.sprite.Sprite):
    def __init__(self, ID):

        #attributes for enemy_ship
        self.tick_adjuster = 0
        self.health = 1
        self.time_to_shoot = 0
        self.how_often_shoot = 100
        self.ID = ID
        
        #drawing simple red square for enemy
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, 300))

    def move(self):
        #we want to randomize enemy movement though not at 60 FPS
        #using an adjuster that slows down actual movement
        if self.tick_adjuster >= 4:
            #if we are at left bound we don't want to randomize movement
            if self.rect.left <= 50:
                self.rect.move_ip(100, 0)
            #similiarly for right bound
            elif self.rect.right >= SCREEN_WIDTH - 50:
                self.rect.move_ip(-100, 0)
            #randomizing either moving left and right
            else:
                speed = random.choice(ENEMY_MOVEMENT)
                self.rect.move_ip(speed, 0)
            self.tick_adjuster = 0
            
        #else we add 1 tick
        else:
            self.tick_adjuster += 1

        #similar concept for movement, we want enemies to shoot alot slower periodically than they move
        if self.time_to_shoot >= self.how_often_shoot:
            self.time_to_shoot = 0
            return True
        else:
            self.time_to_shoot += 1

        

        
            

#Bullet class and children

class Bullet(pygame.sprite.Sprite):

    def __init__(self, ship_center, from_player = True):
        #attributes for bullet
        self.damage = 1
        self.speed = 0
        self.from_player = from_player
        if from_player:
            self.speed = -50
        else:
            self.speed = 50
        
        #creating bullet
        super().__init__()
        self.image = pygame.Surface([5, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = ship_center

    def move(self):
        #check to see if bullet is still on screen
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()
        else:
            #normal bullets move in a straight line
            self.rect.move_ip(0, self.speed)
