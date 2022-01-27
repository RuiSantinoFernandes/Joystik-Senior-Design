import pygame, sys
from pygame.locals import *
import random, time, Classes


#initializing game
pygame.init()

#setting up frames per second
FPS = 30
FramePerSec = pygame.time.Clock()

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
PLAYER_ID = 1
ENEMY_ID = 5

#Creating black screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Starships")


#creating sprite groups

enemies = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#setting up sprites
P1 = Classes.Player_Ship(PLAYER_ID)
PLAYER_ID += 1
all_sprites.add(P1)
players.add(P1)


#adding a new user event ****to be done
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 3000)

#adding functionality to display number of lives left
font = pygame.font.SysFont('arial', 22)
health_text = font.render('Health: ' + str(P1.health), True, GREEN)



while True:
    
    #cycles throgh all events occuring
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                new_bullet = Classes.Bullet(P1.rect.center)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        if event.type == ADD_ENEMY:
            new_enemy = Classes.Enemy_Ship(ENEMY_ID)
            ENEMY_ID += 1
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    
    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(health_text, (100, 550))
    
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        shoot = entity.move()
        if shoot != None:
            new_bullet = Classes.Bullet(entity.rect.center, False)
            bullets.add(new_bullet)
            all_sprites.add(new_bullet)
    
    #loops to figure out owner of bullet
    for bullet in bullets:
        #if from player we only want to consider collisions with enemy
        if bullet.from_player:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    if enemy.health <= 1:
                        enemy.kill()
                    else:
                        enemy.health -= 1
        #else only want to consider collisions with player
        else:
            for player in players:
                if bullet.rect.colliderect(player.rect):
                    #if on 1 health kill player
                    if player.health <= 1:
                        health_text = font.render('Health: 0', True, GREEN)
                        player.kill()
                    #else just reduce
                    else:
                        player.health -= 1
                        health_text = font.render('Health: ' + str(P1.health), True, GREEN)
    
    
    pygame.display.update()
    FramePerSec.tick(FPS)
    

