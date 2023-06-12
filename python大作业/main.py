import pygame
import sys
import traceback
#从Pygame的locals子模块中导入所有常量
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
from random import *

#pygame初始化
pygame.init()
pygame.mixer.init()

#设置背景尺寸（根据背景图片尺寸设置）
bg_size = width, height = 480, 650
screen = pygame.display.set_mode(bg_size)

#标题
pygame.display.set_caption('星际大战')

#初始飞机数量,可直接修改
enemy3_num = 12
enemy2_num = 8
enemy1_num = 2

#字体颜色设置
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#加载背景图片
background = pygame.image.load('background.jpg').convert_alpha()

#载入游戏音乐
pygame.mixer.music.load('game_music.ogg')
pygame.mixer.music.set_volume(0.3)#将声音参数设置为原来的0.3
bullet_sound = pygame.mixer.Sound('bullet.wav')
bullet_sound.set_volume(0.3)
bomb_sound = pygame.mixer.Sound('use_bomb.wav')
bomb_sound.set_volume(0.3)
supply_sound = pygame.mixer.Sound('supply.wav')
supply_sound.set_volume(0.3)
get_bomb_sound = pygame.mixer.Sound('get_bomb.wav')
get_bomb_sound.set_volume(0.3)
get_bullet_sound = pygame.mixer.Sound('get_bullet.wav')
get_bullet_sound.set_volume(0.3)
upgrade_sound = pygame.mixer.Sound('upgrade.wav')
upgrade_sound.set_volume(0.3)
enemy3_fly_sound = pygame.mixer.Sound('enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.3)
enemy1_down_sound = pygame.mixer.Sound('enemy1_down.wav')
enemy1_down_sound.set_volume(0.3)
enemy2_down_sound = pygame.mixer.Sound('enemy2_down.wav')
enemy2_down_sound.set_volume(0.3)
enemy3_down_sound = pygame.mixer.Sound('enemy3_down.wav')
enemy3_down_sound.set_volume(0.3)
me_down_sound = pygame.mixer.Sound('me_down.wav')
me_down_sound.set_volume(0.3)
update_sound = pygame.mixer.Sound('upgrade.wav')
supply_sound = pygame.mixer.Sound('supply.wav')
get_bomb_sound = pygame.mixer.Sound('get_bomb.wav')
get_bullet_sound = pygame.mixer.Sound('get_bullet.wav')

#添加小型敌机
def add_small_enemies(group1, group2, number):
     for i in range(number):
          e1 = enemy.SmallEnemy(bg_size)
          group1.add(e1)
          group2.add(e1)
#添加中型敌机
def add_mid_enemies(group1, group2, number):
     
     for i in range(number):
          e2 = enemy.MidEnemy(bg_size)
          group1.add(e2)
          group2.add(e2)
#添加大型敌机
def add_big_enemies(group1, group2, number):
     for i in range(number):
          e3 = enemy.BigEnemy(bg_size)
          group1.add(e3)
          group2.add(e3)

#设置速度，分别表示一个精灵组和速度的增量
def increase_speed(target, inc):

     for each in target:
          each.speed += inc

def main():
     #播放背景音乐，循环播放
     pygame.mixer.music.play(-1)

     #生成控制机
     me = myplane.MyPlane(bg_size)

     # 生成敌方飞机，
     #通过 group1 和 group2 交替将敌机加入到实际游戏中的两个精灵组中
     #以便后续方便控制敌人的显示和碰撞检测。
     enemies = pygame.sprite.Group()

     # 生成大型敌机
     big_enemies = pygame.sprite.Group()
     add_big_enemies(big_enemies, enemies, enemy3_num)

     # 生成中型敌机
     mid_enemies = pygame.sprite.Group()
     add_mid_enemies(mid_enemies, enemies, enemy2_num)
     
     # 生成小型敌机
     small_enemies = pygame.sprite.Group()
     add_small_enemies(small_enemies, enemies, enemy1_num)

     # 生成普通子弹
     bullet1 = []
     bullet1_index = 0
     BULLET1_NUM = 4
     for i in range(BULLET1_NUM):
          bullet1.append(bullet.Bullet1(me.rect.midtop)) #在飞机顶部中央生成子弹

     # 生成超级子弹
     bullet2 = []
     bullet2_index = 0
     BULLET2_NUM = 8#创建8个子弹对象，并将其添加到 bullet2 列表中
     for i in range(BULLET2_NUM // 2):
          bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
          bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
          #在循环中，Bullet2 类的实例被创建
          #BULLET2_NUM 是子弹的总数，为了平均分布在左右两侧，
          #循环迭代次数为 BULLET2_NUM 除以 2 的结果


     # 用于延迟
     delay = 100

     clock = pygame.time.Clock()
     
     #中弹图片索引
     e1_destroy_index = 0
     e2_destroy_index = 0
     e3_destroy_index = 0
     me_destroy_index = 0

     # 统计得分
     score = 0
     score_font = pygame.font.Font('MSYH.TTF', 36)

     # 是否暂停游戏
     paused = False
     pause_nor_image = pygame.image.load('pause_nor.png').convert_alpha()
     pause_pressed_image = pygame.image.load('pause_pressed.png').convert_alpha()
     resume_nor_image = pygame.image.load('resume_nor.png').convert_alpha()
     resume_pressed_image = pygame.image.load('resume_pressed.png').convert_alpha()
     pause_rect = pause_nor_image.get_rect()
     pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
     pause_image = pause_nor_image

     # 难度级别
     level = 1

     # 炸弹
     bomb_image = pygame.image.load('bomb.png').convert_alpha()
     bomb_rect = bomb_image.get_rect()
     bomb_font = pygame.font.Font('MSYH.TTF', 40)
     bomb_num = 3

     # 生命数量
     life_image = pygame.image.load('life.png').convert_alpha()
     life_rect = life_image.get_rect()
     life_font = pygame.font.Font('MSYH.TTF', 40)
     life_num = 3

     # 每30秒发放一个补给包
     bullet_supply = supply.Bullet_Supply(bg_size)
     bomb_supply = supply.Bomb_Supply(bg_size)
     life_supply = supply.Life_Supply(bg_size)
     SUPPLY_TIME = USEREVENT  # 自定义计时事件
     pygame.time.set_timer(SUPPLY_TIME, 15 * 1000)

     # 超级子弹定时器
     DOUBLE_BULLET_TIME = USEREVENT + 1

     # 是否使用超级子弹
     is_double_bullet = False

     #  无敌时间计时器
     INVINCIBLE_TIME = USEREVENT + 2

     # 防止重复打开记录文件
     recorded = False
     
     running = True

     # 是否播放大型敌机fly的音效
     play_fly_sound = False 

     while running:
          # 监听用户事件
          for event in pygame.event.get():
               if event.type == QUIT:  # 判断用户是否点击了关闭按钮
                    pygame.quit()
                    sys.exit()

               # 暂停
               elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and pause_rect.collidepoint(event.pos):
                         paused = not paused
                         if paused:
                              pygame.time.set_timer(SUPPLY_TIME, 0)
                              pygame.mixer.music.pause()
                              pygame.mixer.pause()
                         else:
                              pygame.time.set_timer(SUPPLY_TIME, 15 * 1000)
                              pygame.mixer.music.unpause()
                              pygame.mixer.unpause()

               elif event.type == MOUSEMOTION: #鼠标按钮，是否暂停
                    if pause_rect.collidepoint(event.pos):
                         if paused:
                              pause_image = resume_pressed_image
                         else:
                              pause_image = pause_pressed_image
                    else:
                         if paused:
                              pause_image = resume_nor_image
                         else:
                              pause_image = pause_nor_image

               elif event.type == KEYDOWN:
                    # 非停止状态下按下空格才释放炸弹，将敌机清空
                    if not paused and event.key == K_SPACE:
                         if bomb_num > 0:
                              bomb_num -= 1
                              bomb_sound.play()
                              for each in enemies:
                                   if each.rect.bottom > 0:
                                        each.active = False

               elif event.type == SUPPLY_TIME:  #补给
                    supply_sound.play()
                    random_supply = choice([1, 2, 3])
                    if random_supply == 1:
                         bomb_supply.reset()
                    elif random_supply == 2:
                         bullet_supply.reset()
                    else:
                         life_supply.reset()

               elif event.type == DOUBLE_BULLET_TIME: #超级子弹
                    is_double_bullet = False
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

               elif event.type == INVINCIBLE_TIME: #无敌时间
                    me.invincible = False
                    pygame.time.set_timer(INVINCIBLE_TIME, 0)

          # 根据得分增加难度，五个等级
          if level == 1 and score > 50:
               level = 2
               update_sound.play()
               # 增加
               add_small_enemies(small_enemies, enemies, 2)
               add_mid_enemies(mid_enemies, enemies, 1)
               add_big_enemies(big_enemies, enemies, 1)
          elif level == 2 and score > 100:
               level = 3
               update_sound.play()
               # 增加
               add_small_enemies(small_enemies, enemies, 2)
               add_mid_enemies(mid_enemies, enemies, 2)
               add_big_enemies(big_enemies, enemies, 0)
               #提升速度
               increase_speed(small_enemies, 1)
          elif level == 3 and score > 250:
               level = 4
               update_sound.play()
               # 增加
               add_small_enemies(small_enemies, enemies, 3)
               add_mid_enemies(mid_enemies, enemies, 2)
               add_big_enemies(big_enemies, enemies, 1)
               #提升速度
               increase_speed(mid_enemies, 1)
          elif level == 4 and score > 500:
               level = 5
               update_sound.play()
               # 增加
               add_small_enemies(small_enemies, enemies, 3)
               add_mid_enemies(mid_enemies, enemies, 2)
               add_big_enemies(big_enemies, enemies, 1)
               #提升速度
               increase_speed(small_enemies, 1)
               increase_speed(mid_enemies, 1)

          screen.blit(background, (0, 0))
                              
          if life_num and not paused:
               # 检测用户的键盘操作
               key_pressed = pygame.key.get_pressed()
               
               if  key_pressed[K_UP]:
                    me.moveUp()
               if  key_pressed[K_DOWN]:
                    me.moveDown()
               if  key_pressed[K_LEFT]:
                    me.moveLeft()
               if  key_pressed[K_RIGHT]:
                    me.moveRight()

               # 绘制全屏炸弹补给并检测是否获得
               if bomb_supply.active:
                    bomb_supply.move()
                    screen.blit(bomb_supply.image, bomb_supply.rect)
                    #检测我方飞机是否与生命值道具相撞，如果相撞了，
                    #则在游戏界面上消除该道具，并增加一个生命值。
                    if pygame.sprite.collide_mask(bomb_supply, me):
                         get_bomb_sound.play()
                         if bomb_num < 3:
                              bomb_num += 1
                         bomb_supply.active = False

               # 绘制医疗箱补给并检测是否获得
               if life_supply.active:
                    life_supply.move()
                    screen.blit(life_supply.image, life_supply.rect)
                    if pygame.sprite.collide_mask(life_supply, me):
                         get_bomb_sound.play()
                         if life_num < 3:
                              life_num += 1
                         life_supply.active = False

               # 绘制超级子弹补给并检测是否获得
               if bullet_supply.active:
                    bullet_supply.move()
                    screen.blit(bullet_supply.image, bullet_supply.rect)
                    if pygame.sprite.collide_mask(bullet_supply, me):
                         get_bullet_sound.play()
                         # 发射超级子弹
                         is_double_bullet = True
                         pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                         bullet_supply.active = False
                         
               # 发射子弹，每10帧一发
               if not(delay % 10):
                    bullet_sound.play()
                    if is_double_bullet:#双倍子弹，重置bullet2中两个子弹对的位置
                         bullets = bullet2
                         #使用bullet2_index 确保在 bullet2 列表中循环使用子弹对象
                         bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                         bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                         bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                    else:
                         bullets = bullet1
                         bullets[bullet1_index].reset(me.rect.midtop)
                         bullet1_index = (bullet1_index + 1) % BULLET1_NUM

               #检测子弹是否击中敌机
               for b in bullets:
                    enemies_hit = []
                    if b.active:
                         b.move()
                         screen.blit(b.image, b.rect)
                         enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                         #pygame.sprite.collide_mask 指定了使用精灵掩模（mask）来检测碰撞
                    if enemies_hit:
                         b.active = False
                         for e in enemies_hit:
                              e.hit = True
                              if e in mid_enemies or e in big_enemies:
                                   e.energy -= 1
                                   if e.energy == 0:
                                        e.active = False
                              else:
                                   e.active = False
                         
               # 绘制大型敌机
               #初始化认为不需要播放大型敌机飞行的音效
               play_fly_sound = False
               for each in big_enemies:
                    if each.active:  #检测值是否为True
                         each.move()
                         screen.blit(each.image, each.rect)
                         #绘制血槽，在 screen 上绘制了一条
                         #从敌机 (each.rect.left, each.rect.top-5) 位置开始，
                         #到 (each.rect.right, each.rect.top-5) 位置结束的一条黑色线
                         pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 4)
                         #当生命大于20%显示绿色，否则显示红色
                         #宽度为4
                         energy_remain = each.energy / enemy.BigEnemy.energy
                         if energy_remain > 0.2:
                              energy_color = GREEN
                         else:
                              energy_color = RED
                         pygame.draw.line(screen, energy_color,(each.rect.left, each.rect.top - 5), (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                         # 即将出现在画面中播放音效
                         # 只要处于这个范围内，就播放飞行音效
                         if each.rect.bottom > -50 and each.rect.top < bg_size[1]:
                              play_fly_sound = True
                         
                    else:
                         # 毁灭
                         if not (delay % 3):
                              if e3_destroy_index == 0:
                                   enemy3_down_sound.play()
                              if e3_destroy_index == 0:
                                   score += 10
                                   each.reset()

               # 决定是否播放大型敌机飞行音效
               if play_fly_sound:
                    enemy3_fly_sound.play(-1)
                    play_fly_sound = False
               else:
                    enemy3_fly_sound.stop()

               #绘制中型敌机
               for each in mid_enemies:
                    if each.active:
                         each.move()
                         screen.blit(each.image, each.rect)

                         #绘制血槽
                         pygame.draw.line(screen, BLACK,(each.rect.left, each.rect.top - 5),(each.rect.right, each.rect.top - 5),2)
                         #当生命大于20%显示绿色，否则显示红色
                         energy_remain = each.energy / enemy.MidEnemy.energy
                         if energy_remain > 0.2:
                              energy_color = GREEN
                         else:
                              energy_color = RED
                         pygame.draw.line(screen, energy_color,(each.rect.left, each.rect.top - 5),(each.rect.left + each.rect.width * energy_remain,each.rect.top - 5), 2)
                    else:
                         # 毁灭
                         if not (delay % 3):
                              if e2_destroy_index == 0:
                                   enemy2_down_sound.play()
                              if e2_destroy_index == 0:
                                   score += 6
                                   each.reset()

               #绘制小型敌机
               for each in small_enemies:
                    if each.active:
                         each.move()
                         screen.blit(each.image, each.rect)
                    else:
                         # 毁灭
                         if not (delay % 3):
                              if e1_destroy_index == 0:
                                   enemy1_down_sound.play()
                              if e1_destroy_index == 0:
                                   score += 1
                                   each.reset()

               # 检测控制机是否发生碰撞，使用了 PyGame 中的碰撞检测函数 spritecollide，
               #检测我方飞机对象 me 是否与敌方飞机组 enemies 中的任意一个发生了碰撞。
               #不删除与我方飞机碰撞的敌机
               enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
               #它是一个二维的数组，包含了精灵图形中哪些像素属于有效像素。
               #在做碰撞检测时，每个精灵都会有一个对应的掩码，
               #可以检测两个精灵是否重叠（即有部分重合的像素）
               if enemies_down and not me.invincible: #判断控制机是否发生碰撞
                    me.active = False 
                    for e in enemies_down:
                         e.active = False

               # 绘制控制机
               if me.active:
                         screen.blit(me.image, me.rect)
               else:
                    # 毁灭
                    if not (delay % 3):
                         if me_destroy_index == 0:
                              me_down_sound.play()
                         screen.blit(me.destroy_images[me_destroy_index], me.rect)
                         me_destroy_index = (me_destroy_index + 1) % 4
                         if me_destroy_index == 0:
                              life_num -= 1
                              me.reset()
                              pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

               # 绘制炸弹
               bomb_text = bomb_font.render('x %d' % bomb_num, True, WHITE)
               text_rect = bomb_text.get_rect()
               screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
               screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

               # 绘制生命数量
               if life_num:
                    life_text = life_font.render('x %d' % life_num, True, WHITE)
                    ltext_rect = life_text.get_rect()
                    screen.blit(life_image, (340, height - 10 - life_rect.height))
                    screen.blit(life_text, (350 + life_rect.width, height - 5 - life_rect.height))

               # 绘制得分
               score_text = score_font.render('得分 : %s' % str(score), True, WHITE)
               screen.blit(score_text, (10, 5))

          # 绘制游戏结束画面
          elif life_num == 0:
               # 停止背景音乐
               pygame.mixer.music.stop()

               # 停止音效
               pygame.mixer.stop()

               # 停止补给
               pygame.time.set_timer(SUPPLY_TIME, 0)

               #读取历史最高分
               if not recorded:
                    recorded = True
                    with open('record.txt', 'r') as f:
                         record_score = int(f.read())
                    if score > record_score:
                         with open('record.txt', 'w') as f:
                              f.write(str(score))

               # 绘制结束界面，通过pygame.font模块生成score_font和gameover_font对象，
               # 分别用于显示得分和游戏结束界面的字体，其中字体文件为’MSYH.TTF’。
               score_font = pygame.font.Font('MSYH.TTF', 36)
               gameover_font = pygame.font.Font('MSYH.TTF', 36)
               #加载again.png和gameover.png两个PNG格式的图片作为重新开始游戏和结束游戏的按钮图像
               #并使用convert_alpha()方法将其转换为带有alpha通道的Surface对象，以显示透明背景。
               again_image = pygame.image.load('again.png').convert_alpha()
               gameover_image = pygame.image.load('gameover.png').convert_alpha()
               #使用score_font和record_score渲染一个最高得分的文本，并在左上角位置(10, 10)绘制：
               record_score_text = score_font.render('最高得分 : %d' % record_score, True, WHITE)
               screen.blit(record_score_text, (10, 10))


               #使用gameover_font和score分别渲染两个得分的文本，并在游戏结束界面展示。
               #gameover_text1表示"你的得分"，gameover_text2表示本局游戏所获得的得分。
               #获取两个文本区域的矩形大小并确定其在屏幕上的位置，再使用blit方法将其绘制出来。 
               gameover_text1 = gameover_font.render('你的得分', True, WHITE)
               gameover_text1_rect = gameover_text1.get_rect()
               gameover_text1_rect.left, gameover_text1_rect.top = \
                                         (width - gameover_text1_rect.width) // 2, height // 2 - 80
               screen.blit(gameover_text1, gameover_text1_rect)

               gameover_text2 = gameover_font.render(str(score), True, WHITE)
               gameover_text2_rect = gameover_text2.get_rect()
               gameover_text2_rect.left, gameover_text2_rect.top = \
                                         (width - gameover_text2_rect.width) // 2, \
                                         gameover_text1_rect.bottom + 10
               screen.blit(gameover_text2, gameover_text2_rect)
               #使用get_rect方法获取图片的矩形大小和位置信息，
               #(width - rect.width) // 2将图片水平居中
               again_rect = again_image.get_rect()
               again_rect.left, again_rect.top = \
                                (width - again_rect.width) // 2, \
                                gameover_text2_rect.bottom + 20
               screen.blit(again_image, again_rect)

               gameover_rect = gameover_image.get_rect()
               gameover_rect.left, gameover_rect.top = \
                                   (width - gameover_rect.width) // 2, \
                                   again_rect.bottom + 10
               screen.blit(gameover_image, gameover_rect)
               # 检测用户操作，重新开始或者结束游戏
               # 检测是否按下左键
               if pygame.mouse.get_pressed()[0]:  # 表示按下左键
                    # 获取鼠标坐标
                    pos = pygame.mouse.get_pos()
                    if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                         main()
                    elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
                         pygame.quit()
                         sys.exit()

          screen.blit(pause_image, pause_rect)

          delay -= 1
          if not delay:
               delay = 100

          pygame.display.flip()
          clock.tick(60)
if __name__ == '__main__':
     try:
          main()
     except SystemExit:
          pass
     except:          
          traceback.print_exc()
          pygame.quit()
          input()
