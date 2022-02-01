import pygame, sys
from pygame.locals import *
import random, time

#creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)

#Other variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
ENEMY_MOVEMENT = [45, 120]




class Player_Ship(pygame.sprite.Sprite):
    def __init__(self, ID):

        #attributes for player ship
        self.health = 3
        self.ID = ID
        self.proj_type = 'B'
        self.can_shoot = 0
        self.score = 0

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





class Fighter(pygame.sprite.Sprite):
    def __init__(self, ID, movement = 100, size = 50):
        
        #attributes for enemy_ship

        #we don't want ships moving at every iteration of game loop so we need to slow it down
        self.tick_adjuster = 0
        #generates a random number from ENEMY_MOVEMENT upon tick_adjuster >= 100
        self.how_far_move = 0
        #either -1 (moving left) or 1 (moving right)
        self.left_or_right = 1
        #True when we have hit if statement in move(), false when we are on first hit
        self.moving = False
        #Health of enemy
        self.health = 1
        #how many points are awarded upon kill
        self.worth = 1
        #same concept as tick adjuster
        self.time_to_shoot = 0
        self.how_often_shoot = 100
        #keeps track of type of projectile
        self.proj_type = 'B'
        #controls how often ship moves
        self.movement = movement
        #attribute for how large the enemy is
        self.size = size
        #ID number for ship, not really using right now but could be good to have
        self.ID = ID
        
        #drawing simple red square for enemy
        super().__init__()
        self.draw()

    def draw(self):
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(25, SCREEN_WIDTH), random.randint(25, 300))

    def move(self)
        #we want to randomize enemy movement though not at 60 FPS
        #using an adjuster that slows down actual movement
        if self.tick_adjuster >= self.movement:
            #if first time in if statement with respect to entering, self.moving will be false
            #when it is, we need to generate a new movement
            if self.moving == False:
                self.moving = True
                self.how_far_move = random.choice(ENEMY_MOVEMENT)
                self.left_or_right = random.choice([-1,1])
            #if we are at left bound we don't want to randomize movement
            if self.rect.left <= 50:
                self.rect.move_ip(100, 0)
            #similiarly for right bound
            elif self.rect.right >= SCREEN_WIDTH - 50:
                self.rect.move_ip(-100, 0)
            #randomizing either moving left and right
            else:
                #moves ship 15 units either right or left. Note that this isn't affected by any
                #time slowing mechanisms since we want this to be smooth movement.
                self.rect.move_ip(15 * self.left_or_right, 0)
                self.how_far_move -= 15
                #if we run out of movement, we need to stop movement by zeroing tick adjuster and set moving to false
    
                if self.how_far_move <= 0:
                    self.tick_adjuster = 0
                    self.moving = False
            
            
        #else we add 1 tick
        else:
            self.tick_adjuster += 1

        #similar concept for movement, we want enemies to shoot alot slower periodically than they move
        if self.time_to_shoot >= self.how_often_shoot:
            self.time_to_shoot = 0
            return True
        else:
            self.time_to_shoot += 1

class Tanker(Fighter):
    def __init__(self, ID, movement = 150, size = 100, health = 5, how_often_shoot = 150, proj_type = 'R'):
        super().__init__(ID, movement, size, health, how_often_shoot, proj_type)

class Zipper(Fighter):
    def __init__(self, ID, movement = 50, size = 25, health = 2, how_often_shoot = 50, proj_type = 'L'):
        super().__init__(ID, movement, size, health, how_often_shoot, proj_type)


































                  
