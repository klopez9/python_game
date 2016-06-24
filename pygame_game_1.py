# first python game with pygame
#
# character controlled with player input
# enemy blob moves horizontally and shoots bullet periodically
# character can also shoot bullet at enemy
# if the player's bullet connects, enemy is randomly respawned

import os, pygame, pyganim, random, sys, time
from pygame.locals import *

class Character_Sprite_Anim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('character_1.png').convert_alpha()
        self.rect = self.image.get_rect()

        anim_interval = 700
        
        self.walking_anim = pyganim.PygAnimation([('character_1.png', anim_interval),
                                                  ('character_2.png', anim_interval)])
        self.walking_anim.convert_alpha()
        self.walking_anim.play()
        
        self.surprised_anim = pyganim.PygAnimation([('character_surprised_1.png', anim_interval),
                                                    ('character_surprised_2.png', anim_interval)])
        self.surprised_anim.convert_alpha()
        self.surprised_anim.play()

        self.current_anim = self.walking_anim
        self.facing_left = False

class Enemy_Sprite_Anim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('enemy_character_1.png').convert_alpha()
        self.rect = self.image.get_rect()

        anim_interval = 700
        
        self.walking_left_anim = pyganim.PygAnimation([('enemy_character_1.png', anim_interval),
                                                       ('enemy_character_2.png', anim_interval)])
        self.walking_left_anim.convert_alpha()
        self.walking_left_anim.play()
        
        self.walking_right_anim = self.walking_left_anim.getCopy()
        self.walking_right_anim.flip(True, False)
        self.walking_right_anim.makeTransformsPermanent()
        self.walking_right_anim.play()
        
        self.shooting_left_anim = pyganim.PygAnimation([('enemy_character_shoot_1.png', anim_interval),
                                                        ('enemy_character_shoot_2.png', anim_interval)])
        self.shooting_left_anim.convert_alpha()
        self.shooting_left_anim.play()
        
        self.shooting_right_anim = self.shooting_left_anim.getCopy()
        self.shooting_right_anim.flip(True, False)
        self.shooting_right_anim.makeTransformsPermanent()
        self.shooting_right_anim.play()

        self.shoot_interval = 95
        self.shoot_duration = 0
        self.shoot_anim_duration = 80
        self.bullet = None
        
        self.current_anim = self.walking_right_anim
        self.facing_left = False

    def shoot(self):
        if self.bullet == None:
            self.bullet = Bullet_Sprite(self.facing_left)
            if self.facing_left:
                self.bullet.rect.topright = (self.rect.left, self.rect.centery)
                self.current_anim = self.shooting_left_anim
            else:
                self.bullet.rect.topleft = (self.rect.right, self.rect.centery)
                self.current_anim = self.shooting_right_anim

    def switch_direction(self):
        self.facing_left = not self.facing_left
        if self.facing_left:
            if self.shoot_duration > self.shoot_anim_duration:
                self.current_anim = self.shooting_left_anim
            else:
                self.current_anim = self.walking_left_anim
        else:
            if self.shoot_duration > self.shoot_anim_duration:
                self.current_anim = self.shooting_right_anim
            else:
                self.current_anim = self.walking_right_anim

class Bullet_Sprite(pygame.sprite.Sprite):

    def __init__(self, left):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('bullet_small.png').convert_alpha()
        if left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        
        self.going_left = left
        
class Bush_Sprite_Anim(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('bush_1.png').convert_alpha()
        self.rect = self.image.get_rect()

        anim_interval = 1000
        
        self.current_anim = pyganim.PygAnimation([('bush_1.png', anim_interval),
                                          ('bush_2.png', anim_interval)])
        self.current_anim.convert_alpha()
        self.current_anim.play()

class Game_State:

    def __init__(self, x=500, y=500):
        self.window_size = self.window_width, self.window_height = x, y
        self.screen = pygame.display.set_mode((x, y))
        pygame.display.set_caption('My Pygame Game 1')
        
        self.fps = 30
        self.game_clock = pygame.time.Clock()

    def clock_tick(self):
        self.game_clock.tick(self.fps)
    
def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    gs = Game_State()
    
    move_rate = 240 // gs.fps
    move_dict = {K_UP : (0, -1*move_rate),
                 K_DOWN : (0, 1*move_rate),
                 K_LEFT : (-1*move_rate, 0),
                 K_RIGHT : (1*move_rate, 0)}

    character = Character_Sprite_Anim()
    enemy = Enemy_Sprite_Anim()
    bushes = [Bush_Sprite_Anim(), Bush_Sprite_Anim(), Bush_Sprite_Anim()]
    sword = pygame.image.load('greatsword.png').convert_alpha()
    sword_rect = sword.get_rect().move(gs.window_width//3, 0)
    
    bg = pygame.image.load('background.png').convert()

    enemy.rect.move_ip(gs.window_width//3, gs.window_height//3)
    bushes[0].rect.move_ip(gs.window_width//10, 2*gs.window_height//5)
    bushes[1].rect.move_ip(6*gs.window_width//8, 1*gs.window_height//8)
    bushes[2].rect.move_ip(gs.window_width//2, 9*gs.window_height//10)
    sprite_anim_list = [character,
                        enemy,
                        bushes[0],
                        bushes[1],
                        bushes[2]]

    character_bullet = None

    while 1:
        # pump and get events
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # process player input
        keys = pygame.key.get_pressed()
        if keys[K_UP] and character.rect.top > 0:
            character.rect.move_ip(move_dict[K_UP])
        if keys[K_DOWN] and character.rect.bottom < gs.window_height:
            character.rect.move_ip(move_dict[K_DOWN])
        if keys[K_LEFT] and character.rect.left > 0:
            character.facing_left = True
            character.rect.move_ip(move_dict[K_LEFT])
        if keys[K_RIGHT] and character.rect.right < gs.window_width:
            character.facing_left = False
            character.rect.move_ip(move_dict[K_RIGHT])
        if keys[K_SPACE] and character_bullet == None:
            character_bullet = Bullet_Sprite(character.facing_left)
            if character.facing_left:
                character_bullet.rect.topright = (character.rect.left, character.rect.centery)
                character_bullet.rect.move_ip(move_rate, 0) #offset start position
            else:
                character_bullet.rect.topleft = (character.rect.right, character.rect.centery)
                character_bullet.rect.move_ip(-1*move_rate, 0) #offset start position

        # it's supposedly faster to supply screen as scale() arg rather than
        # using gs.screen.blit(bg, (0,0)) to blit background onto screen
        pygame.transform.scale(bg, (gs.window_size), gs.screen)

        # stick the sword somewhere
        gs.screen.blit(sword, sword_rect.topleft)

        # enemy movement behavior
        if enemy.facing_left:
            if enemy.rect.left > 0:
                enemy.rect.move_ip(-1*move_rate/4, 0)
            else:
                enemy.switch_direction()
        else:
            if enemy.rect.right < gs.window_width:
                enemy.rect.move_ip(move_rate/4, 0)
            else:
                enemy.switch_direction()

        # enemy shoot behavior
        if enemy.shoot_duration == 0:
            #enemy.shoot_duraton = enemy.shoot_interval
            setattr(enemy, 'shoot_duration', enemy.shoot_interval)
            enemy.shoot()
        elif enemy.shoot_duration > 0:
            #enemy.shoot_duration -= 1
            setattr(enemy, 'shoot_duration', enemy.shoot_duration - 1)
            if enemy.shoot_duration == enemy.shoot_anim_duration:
                if enemy.facing_left:
                    #enemy.current_anim = enemy.walking_left_anim
                    setattr(enemy, 'current_anim', enemy.walking_left_anim)
                else:
                    #enemy.current_anim = enemy.walking_right_anim
                    setattr(enemy, 'current_anim', enemy.walking_right_anim)

        # process character's bullet
        if character_bullet != None:
            if character_bullet.rect.left < 0 or character_bullet.rect.right > gs.window_width:
                character_bullet = None
            elif pygame.sprite.collide_rect(character_bullet, enemy):
                character_bullet = None
                enemy.rect.top = random.randint(0, gs.window_height - enemy.rect.height)
                enemy.rect.left = random.randint(0, gs.window_width - enemy.rect.width)
                enemy.facing_left = bool(random.getrandbits(1))
                enemy.switch_direction() # this will update the animation
            else:
                if character_bullet.going_left:
                    character_bullet.rect.move_ip(-1*move_rate, 0)
                else:
                    character_bullet.rect.move_ip(move_rate, 0)
                gs.screen.blit(character_bullet.image, character_bullet.rect.topleft)

        # process enemy's bullet
        if enemy.bullet != None:
            if enemy.bullet.rect.left < 0 or enemy.bullet.rect.right > gs.window_width:
                enemy.bullet = None
            else:
                if enemy.bullet.going_left:
                    enemy.bullet.rect.move_ip(-1*move_rate, 0)
                else:
                    enemy.bullet.rect.move_ip(move_rate, 0)
                gs.screen.blit(enemy.bullet.image, enemy.bullet.rect.topleft)

        # if character and enemy collide, undo character move;
        # this has the effect of freezing the character in place
        # if the enemy passes over the character during its animation
        if pygame.sprite.collide_rect(character, enemy):
            if keys[K_UP] and character.rect.top > 0:
                character.rect.move_ip(move_dict[K_DOWN])
            if keys[K_DOWN] and character.rect.bottom < gs.window_height:
                character.rect.move_ip(move_dict[K_UP])
            if keys[K_LEFT] and character.rect.left > 0:
                character.rect.move_ip(move_dict[K_RIGHT])
            if keys[K_RIGHT] and character.rect.right < gs.window_width:
                character.rect.move_ip(move_dict[K_LEFT])

        # blit sprites
        for sprite in sprite_anim_list:
            sprite.current_anim.blit(gs.screen, (sprite.rect.topleft))

        # update and tick
        pygame.display.update()
        gs.game_clock.tick(gs.fps)

if __name__ == "__main__":
    main()
