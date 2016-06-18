# first python game with pygame
#
# character moves around a screen controlled with arrow keys
# window is resizable
# gameloop has 5 ms hard wait
# sprite changes temporarily when border is touched

import sys, pygame, time
from pygame.locals import *

def main():
    pygame.init()

    size = width, height = 255, 255
    white = 255, 255, 255
    move_dict = {K_UP : (0, -1),
                 K_DOWN : (0, 1),
                 K_LEFT : (-1, 0),
                 K_RIGHT : (1, 0)}

    screen = pygame.display.set_mode((size),HWSURFACE|DOUBLEBUF|RESIZABLE)

    character = pygame.image.load("character1.png")
    character_surp = pygame.image.load("character2.png")
    # assume sprite for same character have same dimensions
    character_rect = character.get_rect()

    current_sprite = character
    hit_counter = 0
    hit_duration = 8

    while 1:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    pygame.quit()
                except:
                    sys.exit()
            elif event.type == VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                screen.blit(current_sprite,(0,0))
                pygame.display.flip()
                width, height = event.dict['size']

        if hit_counter > 0:
            current_sprite = character_surp
            hit_counter -= 1
        elif hit_counter == 0:
            current_sprite = character
            
        keys = pygame.key.get_pressed()
        if keys[K_UP] and character_rect.top >= 0:
            character_rect.move_ip(move_dict[K_UP])
        if keys[K_DOWN] and character_rect.bottom <= height:
            character_rect.move_ip(move_dict[K_DOWN])
        if keys[K_LEFT] and character_rect.left >= 0:
            character_rect.move_ip(move_dict[K_LEFT])
        if keys[K_RIGHT] and character_rect.right <= width:
            character_rect.move_ip(move_dict[K_RIGHT])

        if character_rect.top < 0 or character_rect.bottom > height \
        or character_rect.left < 0 or character_rect.right > width:
            hit_counter = hit_duration

        time.sleep(0.005)
        screen.fill(white)
        screen.blit(current_sprite, character_rect)
        pygame.display.flip() # use flip with double buffered window

if __name__ == "__main__":
    main()
