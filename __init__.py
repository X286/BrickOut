# -*- coding: utf-8 -*-
import random
import math
import ConfigParser
import pygame

from PIL import Image
from lvl_fSorted import lvl_open
from baseObj import GameObj, SpriteGroup
from addSurface import ImgPil

# Конфигурация программы.
conf = ConfigParser.RawConfigParser()
conf.read('BreakConf.conf')
# Цвет задника
background_colour = pygame.Color('#000000')
# Разрешение окна
(width, height) = (int(conf.get('screen_res', 'x')),\
                   int(conf.get('screen_res', 'y')))
# Где лежат уровни
LConf = conf.get('lvl_folder', 'lvl')
# и фонты
fonts = conf.get('fonts', 'def_font')

class Text (object):
    def __init__(self, size, color= '#FF0000'):
        self.__myfont = pygame.font.Font(conf.get("res_folder", "res_fonts")+conf.get("fonts","def_font"), size)
        self.text = 'say my name'
        self.colour = pygame.Color(color)
        self.isBold = 0
    def writeOn (self, scr, (x, y)):
        sruf = self.__myfont.render(self.text, self.isBold, self.colour)
        scr.blit(sruf, (x, y))


class Wall (GameObj):
    def __init__(self,x, y, width, height, color = '#FF0000'):
        super(Wall, self).__init__(x, y, width, height, color)

    def draw(self, surface):
        surface.blit(self.image, [self.rect.x, self.rect.y])

    def collision(self, ball):
        col = self.direction_to_rect(ball.rect)
        if col == 0:
            ball.rect.x +=ball.speed
            ball.angle = float(2*math.pi - ball.angle)
        if col == 2:
                ball.rect.x -= ball.speed
                ball.angle = float(2 * math.pi - ball.ar - ball.angle)
        if col == 1:
            ball.rect.y -= ball.speed
            ball.angle = float(math.pi - ball.angle)

        if col == 3:
            ball.rect.y += ball.speed
            ball.angle = float (math.pi - ball.angle)


class BrickTop (Wall):
    def __init__(self, x, y, width, height, color='#FF0000', chance = 0.20):
        super(BrickTop, self).__init__(x, y, width, height, color)
        self.bonus = None
        self.hits = 1
        self.score = 100
        self.chance = chance
        self.__setBonus()

    def __setBonus (self):
        procentage = round(self.chance / 1, 2)
        if random.random() <= procentage:
            if (random.random() > 0.50):
                positive_or_negative = True

            else:
                positive_or_negative = False
            createdBonus = Bonus(self.rect.x, self.rect.y, self.rect.width / 2, self.rect.height / 2)
            createdBonus.positive_or_negative = positive_or_negative
            if createdBonus.positive_or_negative is True:
                choiced = random.choice(createdBonus.positive_list)
                createdBonus.choice = createdBonus.positive_list.index(choiced)
                createdBonus.setSurface(choiced)
            else:
                choiced = random.choice(createdBonus.negative_list)
                createdBonus.choice = createdBonus.negative_list.index(choiced)
                createdBonus.setSurface(choiced)

            self.bonus = createdBonus

    def collision(self, ball, bonusG, BrickTopGroup):
        if self.rect.left < ball.rect.centerx <=self.rect.right:
            if self.bonus is not None:
                bonusG.add(self.bonus)
            self.remove(BrickTopGroup) # Группа спрайтовая группа
            ball.angle = float(math.pi - ball.angle)

        elif self.rect.top <= ball.rect.centery <= self.rect.bottom:
            if self.bonus is not None:
                bonusG.add(self.bonus)
            self.remove(BrickTopGroup)
            ball.angle = float(2 * math.pi - ball.ar - ball.angle)


class Bonus(BrickTop):

    def __init__(self, x, y, width, height, color='#FF0000'):
        super(Bonus, self).__init__(x, y, width, height, color)
        #Время действия бонуса (сек) 0 - постоянный бонус
        # Добавочная скорость, например скорость шара 3 + self.speed
        self.falling_speed = 3
        self.positive_or_negative = True
        self.choice = -1
        self.color = color
        self.positive_list = []
        self.positive_name = ['1000points', 'BigBall', 'BigSizePaddle', 'addBall']
        self.negative_list = []
        self.negative_name = ['smallball', 'smallpaddle']
        self.__fill_list()

    def __fill_list (self):
        def setbonussurf(merg, cut):
            merg.paste(cut, (0, 0))
            return merg
        self.positive_list = [
            ImgPil(img, (0, 0, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)), #1000 points
            ImgPil(img, (41, 0, 40, 20),  (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),# BigBall
            ImgPil(img, (82, 21, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)), # BigSizePaddle
            ImgPil(img, (41, 42, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)) #addBAll
        ]
        self.negative_list = [
            ImgPil(img, (82, 63, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)), #small ball
            ImgPil(img, (82, 84, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20))  #small paddle
        ]


    def update(self, screenheigth, bonusgroup, playerG, ballG):
        self.rect.y += self.falling_speed
        if self.rect.y > screenheigth:
            self.remove(bonusgroup)

        self.collide_g (bonusgroup, playerG, ballG)

    def collide_g (self, bonusgroup, playerG, ballG):
        di = pygame.sprite.groupcollide(bonusgroup, playerG, True, False)
        if len (di) is not 0:
            TakeBonus.play(0)
            for player in playerG:
                for b in di.keys():
                    if b.positive_or_negative is True:
                        if b.choice == 0:
                            player.score += 1000
                        if b.choice == 1:
                            for ball in ballG:
                                ball.setSurface(pygame.transform.scale(ball.image, (ball.image.get_width()+5, ball.image.get_height()+5)))
                        if b.choice == 2:
                            player.setSurface(pygame.transform.scale(player.image, (player.image.get_width()+10, player.image.get_height())))
                        if b.choice == 3:
                            ball_surf = ImgPil(img, (81, 105, 14, 14), (14, 14), ballcut).convert_to_pygame_surface(
                                (14, 14))
                            oneball = Ball(width / 2, height / 2, 14, 14)
                            oneball.setSurface(ball_surf)
                            ballG.add(oneball)

                    else:
                        if b.choice == 0:
                            for ball in ballG:
                                if ball.rect.width > 14 and ball.rect.height > 14:
                                    ball.setSurface(pygame.transform.scale(ball.image, (
                                    ball.image.get_width() - 5, ball.image.get_height()-5)))
                                else:
                                    player.score -= 500
                        if b.choice == 1:
                            player.setSurface(pygame.transform.scale(player.image, (
                            player.image.get_width() - 10, player.image.get_height())))


                player.score += len(di)*20


class Ball(Wall):
    def __init__(self, x, y, width, height, color = '#FF0000'):
        super(Wall, self).__init__(x, y, width, height, color)
        self.speed = 7
        self.angle =  float (2*math.pi)

    def update(self, ballG, heigth):
        if self.rect.y + 10 > height:
            self.remove(ballG)
        else:
            self.rect.x += math.sin(self.angle) * self.speed
            self.rect.y -= math.cos(self.angle) * self.speed

    def draw(self, surface):
        surface.blit(self.image, [self.rect.x, self.rect.y])


class Player (BrickTop):

    def __init__(self, x, y, width, height, color='#0000FF'):
        super(Player, self).__init__(x, y, width, height, color)
        # скорость ракетки
        self.speedX = 8
        #Список активных бонусов
        self.getted_bonus = []
        self.lives = 3
        self.score = 0

    def __move_single_axis(self, dx, wallsG):
        self.rect.x += dx
        for wall in wallsG:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right

    #Движение ракетки до снеток (имеется баг)
    def update(self, keys, wallsG):

            if keys[pygame.K_RIGHT]:
                self.__move_single_axis(self.speedX, wallsG)
            if keys[pygame.K_LEFT]:
                self.__move_single_axis((-1)*(self.speedX), wallsG)

    def collision(self, ball):

        col = self.direction_to_rect(ball.rect)
        if col == 1:
            ball.rect.y -= ball.speed # убираем коллизии с 1 итерации
            ball.angle = self.__segmentation(5, ball)

    def __segmentation(self, segments, ball):
        halfwidth = self.rect.width / 2
        line = []
        angles = [1.1]
        offset = angles[0] / segments
        for k in range(0, halfwidth, halfwidth / segments):
            line.append([self.rect.x+k, self.rect.x+k + halfwidth / segments])
            angles.append(round((1.1 - len(line) * offset), 2))
        line.append([self.rect.x+ halfwidth,self.rect.x+halfwidth])

        for z, k in enumerate(range(halfwidth, self.rect.width, halfwidth / segments)):
            line.append([self.rect.x+k, self.rect.x+k + halfwidth / segments])
            angles.append(round((2 * math.pi - ((z + 1) * offset)), 2))
        anglepos = 0
        angles.reverse()

        for enum, segment in enumerate(line):
            if segment[0] < ball.rect.centerx <= segment[1]:
                return angles[enum]
            
        if anglepos == 0:
            if ball.rect.centerx < self.rect.centerx:
                return angles[0]
            else:
                return angles[len(angles)-1]


class Encounters (Ball):
    def __init__(self,x, y, heigth, width, color = '#FF00FF'):
        super(Encounters, self).__init__(x,y, heigth, width)
        self.speed = 2
        self.angle = 0.01
        self.y = self.rect.y
        self.animateleng = 0

    def collision(self,player, Gball, encodGroup):

        if pygame.sprite.spritecollideany(self, Gball):
            TakeEncounter.play(0)
            self.remove(encodGroup)
            player.score += 100


    def update (self, player, gball, amplitude, encGroup, screenwidth):
        self.collision (player,gball,encGroup)
        if self.rect.y > screenwidth:
            self.remove(encGroup)

        self.rect.x += self.speed
        self.rect.y = self.y + math.sin(self.angle)*amplitude
        self.angle += 0.1



    def draw (self, surface):
        surface.blit (self.image, [self.rect.x, self.rect.y])

def Collisions (wallG, ballG, exist1, exist2):
    remeaning = pygame.sprite.groupcollide(ballG, wallG, exist1, exist2)
    if remeaning:
        effect.play(0)
        for ballobj in remeaning.keys():
            for wallobj in remeaning[ballobj]:
                    if  hasattr(wallobj, 'lives'):
                        wallobj.collision(ballobj)
                    elif hasattr(wallobj, 'bonus'):
                        wallobj.collision (ballobj, flyingBonuses, brickWall)
                        board.score += 10
                    else:
                        wallobj.collision(ballobj)


def build_lvl(name):
    def setbonussurf(merg, cut):
        merg.paste(cut, (0, 0))
        return merg
    # кирпичи в атласе
    brick_top_sprite = [
        ImgPil(img, (82, 0, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (0, 21, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (41, 21, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (0, 42, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (82, 42, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (0, 63, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (41, 63, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (0, 84, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (41, 84, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
        ImgPil(img, (0, 105, 40, 20), (40, 20), setbonussurf).convert_to_pygame_surface((40, 20)),
    ]

    lvl = open(conf.get("lvl_folder", "lvl") + name)
    brickW = int(conf.get("bricks", "width"))
    brickH = int(conf.get("bricks", "heigth"))
    offsetBrickH = brickH
    for line in lvl:
        offsetBrickW = brickW
        line = line.replace("\n", "")
        line = line.replace("\t", "")
        for item in line:
            if item != '0':
                onceBrick = BrickTop(
                    offsetBrickW, offsetBrickH, brickW, brickH
                    )
                onceBrick.setSurface(random.choice(brick_top_sprite))
                #onceBrick.hits = int(item)
                brickWall.add(onceBrick)
            offsetBrickW += brickW
        offsetBrickH += brickH


pygame.font.init()

'''
Effect
'''
pygame.mixer.init()
effect = pygame.mixer.Sound('res\wav\HitBall.wav')
effect.set_volume (0.5)
loselive = pygame.mixer.Sound('res\wav\looselive.wav')
effect.set_volume (0.75)
loseGame = pygame.mixer.Sound('res\wav\Gameover.wav')
TakeBonus = pygame.mixer.Sound('res\wav\TakeBonus.wav')
TakeBonus.set_volume (0.75)
TakeEncounter = pygame.mixer.Sound('res\wav\TakeEncounter.wav')

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Brick out')

img = Image.open('res/sheet/SpriteBuild.png') # загрузка изображения через PIL

encounterfront = pygame.image.load('res/sheet/Disk1.png')
encounterdorder = pygame.image.load('res/sheet/Disk2.png')

def ballcut (imgmerg, imgcut):
    imgmerg.paste(imgcut, (0, 0))
    return imgmerg

# мячик начало игры
ball_surf = ImgPil(img, (81,105, 14,14),(14,14),ballcut).convert_to_pygame_surface((14,14))
oneball = Ball (width/2,height/2,14,14)
oneball.setSurface(ball_surf)
balls = SpriteGroup(oneball)

# Ракетка начало игры
board_surface = ImgPil(img, (0, 126, 80, 20),(80,20), ballcut).convert_to_pygame_surface((80,20))
board = Player (width/2-20, height-40, 80, 20, '#FF00FF')
board.setSurface(board_surface)
player = SpriteGroup (board)

bg = pygame.image.load("res/sheet/starfield.png")
bg = pygame.transform.scale (bg, (640,600))

brickWall = SpriteGroup()

def leftrigthwall (merged, cutted):
    for setup in range(0, merged.size[1], cutted.size[1]):
        merged.paste(cutted, (0, setup))
    return merged

wallsurf = ImgPil (img, (62, 105, 10, 20), (10, height), leftrigthwall).convert_to_pygame_surface((10,height))
leftWall = Wall(0, 0, 10, height)
leftWall.setSurface(wallsurf)
rightWall = Wall(width - 10, 0, 10, height)
rightWall.setSurface(wallsurf)

def topwallsurf (merged, cutted):
    for setup in range(0, merged.size[0], cutted.size[0]):
        merged.paste(cutted, (setup, 0))
    return merged

wallsurf = ImgPil (img, (96, 105, 20, 10), (width, 10), topwallsurf).convert_to_pygame_surface((width,10))

topWall = Wall(0, 0, width, 10)
topWall.setSurface(wallsurf)

bottomWall = Wall(0, height - 10, width, height)
bottomWall.setSurface(wallsurf)
walls = SpriteGroup(topWall, leftWall, rightWall)#, bottomWall)

lvl_count = 0
lst = lvl_open ('lvl').get_sorted()
build_lvl (lst[lvl_count])

flyingBonuses = SpriteGroup()

fpswrite = Text(14, color='#00FF00')

Win = Text (32, color='#00FF00')

FPS = pygame.time.Clock()
running = True

#Event

eventz = pygame.USEREVENT+0
pygame.time.set_timer(eventz, random.randint(1000, 20000))

animateEvent = pygame.USEREVENT+1
pygame.time.set_timer(animateEvent, 160) # анимация

fly_events  = SpriteGroup()
mustbeplayed = True
ESC_pause = True

while running:
    FPS.tick(60)
    # pressed bth
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == eventz:
            shit_fly = Encounters(-50, random.randint (70, 300), 20,40)
            fly_events.add(shit_fly)

        if event.type == animateEvent:
            for encounter in fly_events:

                if encounter.animateleng == 0:
                    encounter.setSurface (encounterfront)
                    encounter.animateleng = 1

                elif encounter.animateleng == 1:
                    encounter.setSurface (encounterdorder)
                    encounter.animateleng = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ESC_pause = not ESC_pause
            if event.key == pygame.K_r:
                if board.lives == 0:
                    balls.empty()
                    brickWall.empty()
                    board.lives = 3
                    lvl_count = 0
                    lst = lvl_open('lvl').get_sorted()
                    build_lvl(lst[lvl_count])
                    board.score = 0
                    balls.add(oneball)


    screen.blit(bg, (0,0))

    '''
    Коллизии
    '''
    # Стены
    Collisions(walls, balls, False, False)
    # Кирпичи
    Collisions(brickWall, balls, False, False)
    # Игрок
    Collisions(player, balls, False, False)
    if ESC_pause == False:
        'Update section'
        fly_events.update(board, balls, 80, fly_events, width)
        player.update(keys, walls)
        balls.update(balls, height)
        flyingBonuses.update(height, flyingBonuses, player, balls)
    else:
        if board.lives != 0:
            Win.text = 'Paused!'
            Win.writeOn(screen, (width / 3, height / 2))

    'Draw section'
    fly_events.draw(screen)
    player.draw(screen)
    walls.draw(screen)
    balls.draw(screen)
    brickWall.draw(screen)
    flyingBonuses.draw(screen)

    if len(balls) == 0 and board.lives > 0:
        if board.lives > 1:
            loselive.play(0)
        board.lives -= 1
        balls.add(oneball)

        for ball in balls:
            ball.rect.x = width / 2
            ball.rect.y = height / 2
            ball.angle = float(2*math.pi)
        board.rect.x = width / 2 - 20

    if board.lives == 0:
        Win.text = '\t\tGAME OVER!'
        if mustbeplayed is True:
            loseGame.play(0)
            mustbeplayed = False
        balls.empty()
        Win.writeOn(screen, (width / 6, height / 2))


    if len (brickWall) == 0 and board.lives > 0:

        if len (lst)== lvl_count+1:
            Win.text = 'Win!'
            Win.writeOn(screen, (width / 10, height / 2))
            board.score += 1000

        else:
            lvl_count+=1
            board.score += 500
            build_lvl(lst[lvl_count])
            balls.empty()
            balls.add(oneball)

            for ball in balls:
                ball.rect.x = width/2
                ball.rect.y = height/2
                ball.angle = float (math.pi)

            board.rect.x = width/2-20
    else:
        if board.lives == 0:
            fpswrite.text = u' You Score: ' + str(board.score)
        else:
            fpswrite.text = u' Lives:  '+str(board.lives)+u' Score: '+ str(board.score)
        fpswrite.writeOn(screen, (10,10))


    pygame.display.flip()