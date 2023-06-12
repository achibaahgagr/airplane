import pygame
from random import *
#小型敌机
class SmallEnemy(pygame.sprite.Sprite):
     
     def __init__(self, bg_size):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load('enemy1.png').convert_alpha()
          self.active = True
          self.rect = self.image.get_rect()
          self.width, self.height = bg_size[0], bg_size[1]
          self.speed = 2
          self.mask = pygame.mask.from_surface(self.image)
          #设置小型敌机能够出现范围的矩形大小
          self.rect.left, self.rect.top = \
                          randint(0, self.width - self.rect.width), \
                          randint(-5 * self.rect.height, 0)
     #设置敌机移动
     def move(self):
          if self.rect.top < self.height:
               self.rect.top += self.speed
          else:
               self.reset()

     def reset(self):
          self.active = True
          self.rect.left, self.rect.top = \
                          randint(0, self.width - self.rect.width), \
                          randint(-7 * self.rect.height, 0)

#中型敌机
class MidEnemy(pygame.sprite.Sprite):
     energy = 8
     
     def __init__(self, bg_size):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load('enemy2.png').convert_alpha()
          self.rect = self.image.get_rect()
          self.width, self.height = bg_size[0], bg_size[1]
          self.speed = 1
          self.active = True
          self.hit = False
          self.mask = pygame.mask.from_surface(self.image)
          self.energy = MidEnemy.energy
          self.rect.left, self.rect.top = \
                          randint(0, self.width - self.rect.width), \
                          randint(-10 * self.height, -self.height)
     #设置敌机移动
     def move(self):
          if self.rect.top < self.height:
               self.rect.top += self.speed
          else:
               self.reset()

     def reset(self):
          self.active = True
          self.energy = MidEnemy.energy
          self.rect.left, self.rect.top = \
                          randint(0, self.width - self.rect.width), \
                          randint(-10 * self.height, -self.height)
#大型敌机
class BigEnemy(pygame.sprite.Sprite):
     energy = 20
     def __init__(self, bg_size):
          pygame.sprite.Sprite.__init__(self)

          self.image = pygame.image.load('enemy3_n1.png').convert_alpha()
          #self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
          self.rect = self.image.get_rect()
          self.width, self.height = bg_size[0], bg_size[1]
          self.speed = 1
          self.active = True
          self.hit = False
          self.mask = pygame.mask.from_surface(self.image)
          self.energy = BigEnemy.energy
          self.rect.left, self.rect.top = \
                          randint(0, self.width - self.rect.width), \
                          randint(-30 * self.height, -5 * self.height)

     def move(self):
          if self.rect.top < self.height:
               self.rect.top += self.speed
          else:
               self.reset()

     def reset(self):
          self.active = True #使敌人重新出现，randint在指定坐标范围内生成随机值
          self.energy = BigEnemy.energy
          self.rect.left, self.rect.top = \
                          randint(0, self.width - self.rect.width), \
                          randint(-30 * self.height, -5 * self.height)
