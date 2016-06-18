# first python game with pygame
#
# character moves around a screen controlled with arrow keys
# color background and bush sprite also present
# window is no longer resizable
# gameloop duration is controlled by Clock.tick()
# sprites are animated with pyganim on a 1 second interval

import sys, pygame, time, pyganim
from pygame.locals import *

def main():
    pygame.init()

    WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 255, 255
    fps = 30
    move_rate = 240 // fps
    move_dict = {K_UP : (0, -1*move_rate),
                 K_DOWN : (0, 1*move_rate),
                 K_LEFT : (-1*move_rate, 0),
                 K_RIGHT : (1*move_rate, 0)}
    mainClock = pygame.time.Clock()

    screen = pygame.display.set_mode((WINDOW_SIZE))
    pygame.display.set_caption('Messing Around')

    character_rect = pygame.image.load("character1.png").convert_alpha().get_rect()
    character_anim = pyganim.PygAnimation([('character1.png', 1000),
                                           ('character2.png', 1000)])
    character_anim.convert_alpha()
    character_anim.play()
    
    bush_rect_1 = pygame.image.load("bush1.png").convert_alpha().get_rect()    
    bush_rect_2 = bush_rect_1.copy()
    bush_rect_3 = bush_rect_1.copy()
    bush_anim = pyganim.PygAnimation([('bush1.png', 1000),
                                      ('bush2.png', 1000)])
    bush_anim.convert_alpha()
    bush_anim.play()
    
    bg = pygame.image.load("background.png").convert()
    bg = pygame.transform.scale(bg, WINDOW_SIZE)
    bg_rect = bg.get_rect()

    sprite_anim_list = [(character_anim, character_rect),
                        (bush_anim, bush_rect_1.move(WINDOW_WIDTH//10, 2*WINDOW_HEIGHT//5)),
                        (bush_anim, bush_rect_2.move(6*WINDOW_WIDTH//8, 1*WINDOW_HEIGHT//8)),
                        (bush_anim, bush_rect_3.move(WINDOW_WIDTH//2, 9*WINDOW_HEIGHT//10))]

    while 1:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        keys = pygame.key.get_pressed()
        if keys[K_UP] and character_rect.top >= 0:
            character_rect.move_ip(move_dict[K_UP])
        if keys[K_DOWN] and character_rect.bottom <= WINDOW_HEIGHT:
            character_rect.move_ip(move_dict[K_DOWN])
        if keys[K_LEFT] and character_rect.left >= 0:
            character_rect.move_ip(move_dict[K_LEFT])
        if keys[K_RIGHT] and character_rect.right <= WINDOW_WIDTH:
            character_rect.move_ip(move_dict[K_RIGHT])

        screen.blit(bg, bg_rect)
        for (sprite_anim, rect) in sprite_anim_list:
            sprite_anim.blit(screen, (rect.topleft))
        pygame.display.update()
        mainClock.tick(fps)

if __name__ == "__main__":
    main()
