import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = score_font.render(f'Score: {current_time}', False, 'Red')
    score_rect = score_surf.get_rect(center = (400, 30))
    screen.blit(score_surf, score_rect)
    return current_time

def obs_movement(obs_list):
    if obs_list:
        for obs_rect in obs_list:
            obs_rect.x -= 5
            screen.blit(alien_surf, obs_rect)

        obs_list = [obs for obs in obs_list if obs.x > -100]

        return obs_list
    else:
        return []

def col(player, obs):
    if obs:
        for obs_rect in obs:
            if player.colliderect(obs_rect):
                return False
    return True

#initialize pygame and create display screen
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Escape the Apocalypse!")
clock = pygame.time.Clock()
score_font = pygame.font.Font(None, 35)
escape_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0

escape_surf = score_font.render('Escape!', False, 'Red')
escape_rect = escape_surf.get_rect(center=(400, 30))

ground_surface = pygame.image.load('graphics/ground.png').convert()
background_surface = pygame.image.load('graphics/background.png').convert()

instruct_surf = score_font.render('Space to jump and start. F for Fireball. Don\'t touch the aliens!', False, 'White')
instruct_rect = instruct_surf.get_rect(center = (400, 50))

alien_surf = pygame.image.load('graphics/alien.png').convert_alpha()
alien_rect = alien_surf.get_rect(midbottom = (600, 275))

obs_rect_list = []

player_surf = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 275))
player_gravity = 0

player_start_surf = pygame.image.load('graphics/player.png').convert_alpha()
player_start_surf = pygame.transform.rotozoom(player_start_surf, 0, 2)
player_start_rect = player_start_surf.get_rect(center = (400, 200))

fireball_surf = pygame.image.load('graphics/fireball.png').convert_alpha()
fireball_rectangle = fireball_surf.get_rect(midleft = (player_rect.midright))
fireball = False

start_surf = pygame.image.load('graphics/start.png')
start_rect = start_surf.get_rect(center = (400, 100))
start_bool = True

# Timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer, 1400)

while True:
    for event in pygame.event.get(): # gets all events
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 275:
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.collidepoint(event.pos) and player_rect.bottom >= 275:
                player_gravity = -20

            if event.type == pygame.KEYDOWN and event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                fireball = True

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                alien_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obs_timer and game_active:
            obs_rect_list.append(alien_surf.get_rect(midbottom = (randint(900, 1100), 275)))

    if game_active:
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (0, 275))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 275:
            player_rect.bottom = 275
        screen.blit(player_surf, player_rect)

        obs_rect_list = obs_movement(obs_rect_list)

        game_active = col(player_rect, obs_rect_list)

        if fireball:
            screen.blit(fireball_surf, fireball_rectangle)
            fireball_rectangle.x += 4

        # collision
        if alien_rect.colliderect(player_rect):
            game_active = False

        for obs in range(len(obs_rect_list)):
            if fireball_rectangle.colliderect(obs_rect_list[obs]) and fireball:
                obs_rect_list.remove(obs_rect_list[obs])
                fireball = False
                fireball_rectangle.midleft = (player_rect.midright)
                break
    else:
        fireball = False
        screen.fill('Maroon')
        obs_rect_list.clear()
        player_gravity = 0

        if score != 0:
            instruct_surf = score_font.render(f'Last score: {score}', False, 'White')
            instruct_rect = instruct_surf.get_rect(center = (400, 100))
        screen.blit(player_start_surf, player_start_rect)
        screen.blit(instruct_surf, instruct_rect)



    # draw all our elements
    # update everything
    pygame.display.update()
    clock.tick(60) # set framerate ceiling

