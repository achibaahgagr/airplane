import pygame
#控制机
class MyPlane(pygame.sprite.Sprite): #继承sprit类
     def __init__(self, bg_size): #设置形参，导入背景参数
          pygame.sprite.Sprite.__init__(self)
          #导入控制机
          self.image = pygame.image.load('me1.png').convert_alpha()
          self.destroy_images = []
          self.destroy_images.extend([\
               pygame.image.load('me_destroy_1.png'),\
               pygame.image.load('me_destroy_2.png'),\
               pygame.image.load('me_destroy_3.png'),\
               pygame.image.load('me_destroy_4.png'),])
          #获取rect
          self.rect = self.image.get_rect()
          self.width, self.height = bg_size[0], bg_size[1]
          #控制机初始位置
          self.rect.left, self.rect.top = \
                          (self.width - self.rect.width) // 2, \
                          self.height - self.rect.height - 60
          self.speed = 10   #控制机速度
          self.active = True
          self.invincible = False #无敌状态标志
          self.mask = pygame.mask.from_surface(self.image)  #将传入图片非透明部分标记为mask

     def moveUp(self): #向上走
          if self.rect.top > 0:
               self.rect.top -= self.speed
          else:
               self.rect.top = 0

     def moveDown(self):  #向下走
          if self.rect.bottom < self.height - 60: 
               self.rect.top += self.speed
          else:
               self.rect.bottom = self.height - 60

     def moveLeft(self): #向左走
          if self.rect.left > 0: 
               self.rect.left -= self.speed
          else:
               self.rect.left = 0

     def moveRight(self): #向右走
          if self.rect.right < self.width: 
               self.rect.left += self.speed
          else:
               self.rect.right = self.width

     def reset(self):
          self.rect.left, self.rect.top = \
                          (self.width - self.rect.width) // 2, \
                          self.height - self.rect.height - 60
          self.active = True
          self.invincible = True
