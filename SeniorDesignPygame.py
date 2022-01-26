#import pygame library
import pygame
import random

#Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Define a player object by extending pygame.sprite.Sprite
#The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (
                random.randit(SCREEN_WIDTH +20, SCREEN_WIDTH +100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randit(5,20)

    #Move the sprite based on speed
    #Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#Initialize
pygame.init()

#drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Instantiate player
player = Player()

#Move the sprite based on user keypresses
def update(self, pressed_keys):
    if pressed_keys[K_UP]:
        self.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
        self.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
        self.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
        self.rect.move_ip(5, 0)

    #Keep player on screen
    if self.rect.left < 0:
        self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
        self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
        self.rect.bottom = SCREEN_HEIGHT

#Run until user quit
running = True

#Main loop
while running:

    #Check every event in the queue
    for event in pygame.event.get():
        #Check if user pressed a key
        if event.type == KEYDOWN:
            #Check if key was escape. If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        #Check if user clicked window close
        elif event.type == pygame .QUIT:
            running = False
            
    #Get set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    #Update player sprite based on user keypresses
    player.update(pressed_keys)

    #Fill background with black
    screen.fill((0, 0, 0))

    #Draw the player on the screen
    screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    #Create a surface and pass ina tuple containing length and width
    surf = pygame.Surface((50, 50))

    screen.blit(player.surf, player.rect)

    #Put the center of surf at the center of the display
    surf_center = (
        (SCREEN_WIDTH-surf.get_width())/2,
        (SCREEN_HEIGHT-surf.get_height())/2
    )

    #Flip the display
    pygame.display.flip()

#Done! Time to quit.
pygame.quit()