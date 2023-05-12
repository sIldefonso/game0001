import pygame
import json
from pygame import mixer, font
import random

def move_left(spaceship):
    spaceship["pos_x"] -= spaceship["move_velocity"]

def move_right(spaceship):
    spaceship["pos_x"] += spaceship["move_velocity"]

def run_action(spaceship, shots_list, mixer):
    shots_list.insert(0, (spaceship["pos_x"] + spaceship["image"].get_width() / 2, spaceship["pos_y"]))
    mixer.Sound(spaceship["laser_sound"]).play()

def update_score(spaceship, points):
        spaceship["score"] += points

# Start the game
pygame.init()

# Get settings info
with open('settings.json', 'r') as fp:
    position = (0,0)
    settings = json.load(fp)
    spaceship = {
        "image" : pygame.image.load(settings["spaceship"]["image"]),
        "pos_x" : settings["spaceship"]["spaceship_pos_x"],
        "pos_y" : settings["spaceship"]["spaceship_pos_y"],
        "move_velocity" : settings["spaceship"]["move_velocity"],
        "laser_sound" : settings["spaceship"]["laser"],
        "score" : 0
    }

# Timer
clock = pygame.time.Clock()
start_ticks=pygame.time.get_ticks() 

# background
image = pygame.image.load(settings["environment"]['image'])
image_scroll = pygame.image.load(settings["environment"]['image'])

canvas = pygame.display.set_mode((settings["environment"]['width'], settings["environment"]['height']))
pygame.display.set_caption(settings["environment"]['title'])
score = 0
scroll = 0
exit = False

# shots list
shots_list = []
shot_image = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.circle(shot_image, (255, 0, 0), shot_image.get_rect().center, shot_image.get_width() // 2)

# background sound
mixer.init()
mixer.music.load(settings["environment"]["sound"])
mixer.music.play()

# Enemies
random_position = (random.seed(int(settings["environment"]['width']) ), 
                   random.seed(int(settings["environment"]['height']))
                  )
obstacles_list = []
obstacles_list.append(pygame.Surface((40, 40), pygame.SRCALPHA))



while not exit:
    canvas.fill(0)
    scroll += 5
    position = (position[0], position[1] + scroll)
    position_scroll = (position[0], position[1] - image.get_height() + scroll)
    canvas.blit(image, dest = position)
    canvas.blit(image_scroll, dest = position)
    seconds=(pygame.time.get_ticks() + start_ticks)/1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        # Key Press Events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left(spaceship)
            elif event.key == pygame.K_RIGHT:
                move_right(spaceship)
            elif event.key == pygame.K_SPACE:
                run_action(spaceship, shots_list, mixer)

    # Re-render shots flow
    for i, bullet_pos in enumerate(shots_list):
        shots_list[i] = bullet_pos[0], bullet_pos[1] - 5
        if shot_image.get_rect(center = bullet_pos).left < 0:
            del shots_list[i:]
            break
    for bullet_pos in shots_list:
        canvas.blit(shot_image, shot_image.get_rect(center = bullet_pos))   
    
    # Re-render Spaceship
    canvas.blit(spaceship["image"], (spaceship["pos_x"], spaceship["pos_y"]))   

    # Re-render obstacles
    # for obstacle in obstacles_list:
    #     canvas.blit(obstacle, obstacle.get_rect(center = random_position))   
    #     print(obstacle)

    # Score
    text = str(spaceship["score"])
    font = pygame.font.SysFont(None, 48)
    img_score = font.render(text, True, (255, 255, 0))
    canvas.blit(img_score, (10, 10))

    # Timer
    img_timer = font.render(str(int(seconds)), True, (255, 255, 0))
    canvas.blit(img_timer, (settings["environment"]['width'] / 2, 10))
    
    # Update scene
    if abs(scroll) > image.get_width():
        position = (0,0)
        position_scroll = (0, 0 - image.get_height())
        scroll = 0          
    pygame.display.update()