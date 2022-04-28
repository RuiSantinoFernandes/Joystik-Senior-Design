from guizero import App, Text, Picture, PushButton
import pygame
import time
import random
import sys
import Classes
import os

#functions and games


def snake_game():
    print("code for snake game")


def asteroid_game():
    #print("code for asteroid game")
    pygame.init()


# setting up frames per second
    FPS = 30
    FramePerSec = pygame.time.Clock()

# creating colors
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

# Other variables
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    ENEMY_MOVEMENT = [-20, 20]
    PLAYER_ID = 1
    ENEMY_ID = 5
    POWER_UPS = {"DOUBLE_BARREL": False, "INVINCIBLE": False}

# creating different sounds for different projectiles
    sounds = 'sounds'
    bullet_sound = pygame.mixer.Sound(os.path.join(sounds, 'bullet_sound.wav'))
    laser_sound = pygame.mixer.Sound(os.path.join(sounds, 'laser_sound.wav'))
    rocket_sound = pygame.mixer.Sound(os.path.join(sounds, 'rocket_sound.wav'))
    player_hit_sound = pygame.mixer.Sound(
        os.path.join(sounds, 'player_hit_sound.wav'))
    invincible_hit_sound = pygame.mixer.Sound(
        os.path.join(sounds, 'invincible_hit_sound.wav'))


# Creating black screen
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    DISPLAYSURF.fill(BLACK)
    pygame.display.set_caption("Starships")


# creating sprite groups
    enemies = pygame.sprite.Group()
    players = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # setting up player sprites
    # ****will need to be changed once we add 2 player capability
    P1 = Classes.Player_Ship(PLAYER_ID)
    PLAYER_ID += 1
    all_sprites.add(P1)
    players.add(P1)


# adding events, currently only spawning new enemies
    ADD_FIGHTER = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_FIGHTER, 2000)
    ADD_TANKER = pygame.USEREVENT + 2
    pygame.time.set_timer(ADD_TANKER, 10000)
    ADD_ZIPPER = pygame.USEREVENT + 3
    pygame.time.set_timer(ADD_ZIPPER, 15000)
    ADD_MOTHER_SHIP = pygame.USEREVENT + 4
    pygame.time.set_timer(ADD_MOTHER_SHIP, 40000)
    GENERATE_POWERUP = pygame.USEREVENT + 5
    pygame.time.set_timer(GENERATE_POWERUP, 20000)
    KILL_POWERUP = pygame.USEREVENT + 6


# adding display for health left
    font = pygame.font.SysFont('arial', 22)
    game_over_font = pygame.font.SysFont('arial', 80, True)
    health_text = font.render('Health: ' + str(P1.health), True, GREEN)
    score_text = font.render('Score: ' + str(P1.score), True, GREEN)
    game_over_text = game_over_font.render('Game Over', True, BLACK)

    while True:

        # cycles throgh all events occuring
        for event in pygame.event.get():
          # quits if we x out of game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
          # catches if key is pressed
            if event.type == KEYDOWN:
              # if space, player shoots
                if event.key == K_SPACE:
                    if POWER_UPS["DOUBLE_BARREL"]:
                        left_proj = None
                        right_proj = None
                        if P1.proj_type == 'B':
                            left_proj = Classes.Bullet(
                                (P1.rect.x - 15, P1.rect.y))
                            right_proj = Classes.Bullet(
                                (P1.rect.x + 15, P1.rect.y))
                            pygame.mixer.Sound.play(bullet_sound)
                        elif P1.proj_type == 'L':
                            left_proj = Classes.Laser(
                                (P1.rect.x - 15, P1.rect.y))
                            right_proj = Classes.Laser(
                                (P1.rect.x + 15, P1.rect.y))
                            pygame.mixer.Sound.play(laser_sound)
                        elif P1.proj_type == 'R':
                            left_proj = Classes.Rocket(
                                (P1.rect.x - 15, P1.rect.y))
                            right_proj = Classes.Rocket(
                                (P1.rect.x + 15, P1.rect.y))
                            pygame.mixer.Sound.play(rocket_sound)

                        projectiles.add(left_proj, right_proj)
                        all_sprites.add(left_proj, right_proj)

                    else:
                        new_proj = None
                      # creates projectile of current playernprojectile type and plays sound of type
                        if P1.proj_type == 'B':
                            new_proj = Classes.Bullet(P1.rect.center)
                            pygame.mixer.Sound.play(bullet_sound)
                        elif P1.proj_type == 'L':
                            new_proj = Classes.Laser(P1.rect.center)
                            pygame.mixer.Sound.play(laser_sound)
                        elif P1.proj_type == 'R':
                            new_proj = Classes.Rocket(P1.rect.center)
                            pygame.mixer.Sound.play(rocket_sound)

                        projectiles.add(new_proj)
                        all_sprites.add(new_proj)
              # if enter, we know to change type of projectile (currently only cycles through)
                if event.key == K_RETURN:
                    if P1.proj_type == 'B':
                        P1.proj_type = 'L'
                    elif P1.proj_type == 'L':
                        P1.proj_type = 'R'
                    else:
                        P1.proj_type = 'B'

          # catching when event timer runs out to add enemy of respective type
            if event.type == ADD_FIGHTER:
                new_enemy = Classes.Fighter(ENEMY_ID)
                ENEMY_ID += 1
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            if event.type == ADD_TANKER:
                new_enemy = Classes.Tanker(ENEMY_ID)
                ENEMY_ID += 1
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            if event.type == ADD_ZIPPER:
                new_enemy = Classes.Zipper(ENEMY_ID)
                ENEMY_ID += 1
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            if event.type == ADD_MOTHER_SHIP:
                new_enemy = Classes.Mother_Ship(ENEMY_ID)
                ENEMY_ID += 1
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

          # catching when event timer runs out to generate a powerup
            if event.type == GENERATE_POWERUP:
                new_powerup = random.choice(list(POWER_UPS.keys()))
                if new_powerup == "DOUBLE_BARREL":
                    new_powerup = Classes.Double_Barrel()
                elif new_powerup == "INVINCIBLE":
                    new_powerup = Classes.Invincible()
                projectiles.add(new_powerup)
                all_sprites.add(new_powerup)

            if event.type == KILL_POWERUP:
                for power_up in POWER_UPS:
                    POWER_UPS[power_up] = False

        DISPLAYSURF.fill(BLACK)

    # updating health
        DISPLAYSURF.blit(health_text, (100, 550))
    # updating score
        DISPLAYSURF.blit(score_text, (100, 570))

    # cycling through all sprites, handles movement of sprite irregardless of type
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            shoot = entity.move()
          # catches when move returns True if entity is projectile from enemy
          # same logic as player projectile
            if shoot != None:
                new_proj = None
                if entity.proj_type == 'B':
                    new_proj = Classes.Bullet(entity.rect.center, False)
                    pygame.mixer.Sound.play(bullet_sound)
                elif entity.proj_type == 'L':
                    new_proj = Classes.Laser(entity.rect.center, False)
                    pygame.mixer.Sound.play(laser_sound)
                else:
                    new_proj = Classes.Rocket(entity.rect.center, False)
                    pygame.mixer.Sound.play(rocket_sound)
              # adjusting speed of enemy projectiles to be half speed of its respective type
                projectiles.add(new_proj)
                all_sprites.add(new_proj)

    # loops to figure out if projectile has collided with a ship and who is owner of proj
        for proj in projectiles:
          # if from player we only want to consider collisions with enemy
            if proj.from_player:
                for enemy in enemies:
                    if proj.rect.colliderect(enemy.rect):
                        proj.kill()
                      # if sub 0 health kill enemy
                        if enemy.health - proj.damage <= 0:
                            P1.score += enemy.worth
                            score_text = font.render(
                                'Score: ' + str(P1.score), True, GREEN)
                            enemy.kill()
                        else:
                            enemy.health -= proj.damage
          # if from enemy we only want to consider collisions with player
            else:
                for player in players:
                    if proj.rect.colliderect(player.rect):
                        proj.kill()
                        if proj.is_power_up:
                            if proj.power_up == "DB":
                                POWER_UPS["DOUBLE_BARREL"] = True
                            elif proj.power_up == "IV":
                                POWER_UPS["INVINCIBLE"] = True
                            pygame.time.set_timer(KILL_POWERUP, 10000)

                        elif POWER_UPS["INVINCIBLE"] == True:
                            pygame.mixer.Sound.play(invincible_hit_sound)

                      # if sub 0 health kill player
                        elif player.health - proj.damage <= 0:
                            health_text = font.render('Health: 0', True, GREEN)
                            player.kill()
                            DISPLAYSURF.fill(RED)
                            DISPLAYSURF.blit(game_over_text, (325, 250))
                            pygame.display.update()
                            for entity in all_sprites:
                                entity.kill()
                            time.sleep(3)
                            pygame.quit()
                            sys.exit()
                      # else just reduce
                        else:
                            pygame.mixer.Sound.play(player_hit_sound)
                            player.health -= proj.damage
                            health_text = font.render(
                                'Health: ' + str(P1.health), True, GREEN)

        pygame.display.update()
        FramePerSec.tick(FPS)


def collision_game():
    print("code for collision game")


# initial GUI
app = App(title="Joystik")
welcome_message = Text(app, text="Welcome to Joystik!",
                       size=20, color="lightgreen")
python_choice = PushButton(app, command=snake_game, text="SNAKE GAME")
python_choice = PushButton(app, command=asteroid_game, text="ASTEROID GAME")
python_choice = PushButton(app, command=collision_game, text="COLLISION GAME")
#my_logo = Picture(app, image="logo.PNG")

# display everything
app.display()
