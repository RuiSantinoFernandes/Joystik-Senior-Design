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
        self.health = 5
        self.ID = ID
        self.proj_type = 'B'
        self.can_shoot = 0
        self.score = 0
        
        #drawing player ship
        super().__init__()
        self.image = pygame.image.load("Ship_Images/Blue_Ship.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        #we only want to allow a player to move in a direction if they are within the screen bounds
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
    def __init__(self, ID, movement = 50, size = 50, health = 3, how_often_shoot = 100, proj_type = 'B', picture = "Blue_Ship.png"):
        
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
        self.health = health
        #how many points are awarded upon kill
        self.worth = health
        #same concept as tick adjuster
        self.time_to_shoot = 0
        self.how_often_shoot = how_often_shoot
        #keeps track of type of projectile
        self.proj_type = proj_type
        #controls how often ship moves
        self.movement = movement
        #attribute for how large the enemy is
        self.size = size
        #ID number for ship, not really using right now but could be good to have
        self.ID = ID
        #image type
        self.picture = picture
        #drawing simple red square for enemy
        super().__init__()
        self.draw()

    def draw(self):
        self.image = pygame.image.load("Ship_Images/" + self.picture)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH), random.randint(50, 300))

    def move(self):
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
            if self.rect.left <= 50 and self.left_or_right == -1:
                self.left_or_right = 1
            #similiarly for right bound
            elif self.rect.right >= SCREEN_WIDTH - 50 and self.left_or_right == 1:
                self.left_or_right = -1
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
    def __init__(self, ID, movement = 100, size = 100, health = 10, how_often_shoot = 150, proj_type = 'R', picture = "Green_Ship.png"):
        super().__init__(ID, movement, size, health, how_often_shoot, proj_type, picture)

class Zipper(Fighter):
    def __init__(self, ID, movement = 25, size = 75, health = 5, how_often_shoot = 50, proj_type = 'L', picture = "Red_Ship.png"):
        super().__init__(ID, movement, size, health, how_often_shoot, proj_type, picture)

class Mother_Ship(Fighter):
    def __init__(self, ID, movement = 25, size = 150, health = 30, how_often_shoot = 50, proj_type = 'R', picture = "Green_Ship.png"):
        super().__init__(ID, movement, size, health, how_often_shoot, proj_type, picture)


#Types of projectiles

class Bullet(pygame.sprite.Sprite):

    def __init__(self, ship_center, from_player = True, player = 'P1', damage = 2, speed = 50, width = 5, height = 15):
        #attributes for bullet
        self.damage = damage
        self.from_player = from_player
        self.player = player
        self.speed = speed
        self.is_power_up = False
        if from_player:
            self.speed = speed * -1
        
        #creating bullet
        super().__init__()
        self.image = pygame.Surface([width, height])
        if damage == 2:
            self.image.fill(WHITE)
        elif damage == 1:
            self.image.fill(RED)
        else:
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


class Laser(Bullet):

    def __init__(self, ship_center, from_player = True, player = 'P1', damage = 1, speed = 100, width = 5, height = 30):
        super().__init__(ship_center, from_player, player, damage, speed, width, height)

class Rocket(Bullet):

    def __init__(self, ship_center, from_player = True, player = 'P1', damage = 5, speed = 10, width = 15, height = 25):
        super().__init__(ship_center, from_player, player, damage, speed, width, height)


#Types of power ups

class Power_Up(pygame.sprite.Sprite):

    def __init__(self, player = 'P1', power_up = None):
        self.player = player
        self.power_up = power_up
        self.is_power_up = True
        self.from_player = False

        super().__init__()
        self.image = pygame.Surface([100, 10])
        if self.power_up == "DB":
            self.image.fill(GREEN)
        elif self.power_up == "IV":
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), 0)

        

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Double_Barrel(Power_Up):

    def __init__(self, player = 'P1', power_up = "DB"):
        super().__init__(player, power_up)

class Invincible(Power_Up):

    def __init__(self, player = 'P1', power_up = "IV"):
        super().__init__(player, power_up)
       

    


































                  
