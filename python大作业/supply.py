import pygame
from random import *
#超级子弹
class Bullet_Supply(pygame.sprite.Sprite):
     def __init__(self, bg_size):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load('bullet_supply.png').convert_alpha()
          self.rect = self.image.get_rect()
          self.width, self.height = bg_size[0], bg_size[1]
          #随机生成一个在 0 到 (self.width - self.rect.width) 之间的整数
          #该值作为敌机矩形左侧的 x 坐标值。
          self.rect.left, self.rect.bottom = \
                          randint(0, self.width - self.rect.width), -100
          self.speed = 5
          self.active = False
          self.mask = pygame.mask.from_surface(self.image)

     def move(self):
          if self.rect.top < self.height:
               self.rect.top += self.speed
          else:
               self.active = False

     def reset(self):
          self.active = True
          self.rect.left, self.rect.bottom = \
                          randint(0, self.width - self.rect.width), -100

#炸弹
class Bomb_Supply(pygame.sprite.Sprite):
     def __init__(self, bg_size):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load('bomb_supply.png').convert_alpha()
          self.rect = self.image.get_rect()
          self.width, self.height = bg_size[0], bg_size[1]
          self.rect.left, self.rect.bottom = \
                          randint(0, self.width - self.rect.width), -100
          self.speed = 5
          self.active = False
          self.mask = pygame.mask.from_surface(self.image)

     def move(self):
          if self.rect.top < self.height:
               self.rect.top += self.speed
          else:
               self.active = False

     def reset(self):
          self.active = True
          self.rect.left, self.rect.bottom = \
                          randint(0, self.width - self.rect.width), -100
#医疗箱
class Life_Supply(pygame.sprite.Sprite):
     def __init__(self, bg_size):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load('life_supply.png').convert_alpha()
          self.rect = self.image.get_rect()
          self.width, self.height = bg_size[0], bg_size[1]
          self.rect.left, self.rect.bottom = \
                          randint(0, self.width - self.rect.width), -100
          self.speed = 5
          self.active = False
          self.mask = pygame.mask.from_surface(self.image)

     def move(self):
          if self.rect.top < self.height:
               self.rect.top += self.speed
          else:
               self.active = False

     def reset(self):
          self.active = True
          self.rect.left, self.rect.bottom = \
                          randint(0, self.width - self.rect.width), -100
                          
