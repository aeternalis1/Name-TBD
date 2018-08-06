import pygame
import pygame.gfxdraw
import math
from random import randint



class bullet(pygame.sprite.Sprite):
    def __init__(self,radius,angle):
        super().__init__()
        self.radius = radius
        CIRCLE = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(CIRCLE, 15, 15, radius, (255, 255, 255))
        pygame.gfxdraw.filled_circle(CIRCLE, 15, 15, radius, (255, 255, 255))
        self.angle = angle
        self.image = CIRCLE
        self.rect = self.image.get_rect()


class coin(pygame.sprite.Sprite):
    def __init__(self,radius,angle):
        super().__init__()
        self.radius = radius
        CIRCLE = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(CIRCLE, 15, 15, radius, (255, 255, 0))
        pygame.gfxdraw.filled_circle(CIRCLE, 15, 15, radius, (255, 255, 0))
        self.angle = angle
        self.image = CIRCLE
        self.rect = self.image.get_rect()


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey((1,1,1))
        self.rect = self.image.get_rect()
        self.radius = 12


def dist(y,x,y2,x2):
    return pow(pow(y-y2,2)+pow(x-x2,2),0.5)


def updatePlayerPos(y,x,rev,move,center):
    y = 600-y
    if rev[0] and not rev[1]:
        s = math.sin(0.0349)
        c = math.cos(0.0349)
        y -= center[1]
        x -= center[0]
        ny = x*s+y*c+center[1]
        nx = x*c-y*s+center[0]
    elif rev[1] and not rev[0]:
        s = math.sin(-0.0349)
        c = math.cos(-0.0349)
        y -= center[1]
        x -= center[0]
        ny = x*s+y*c+center[1]
        nx = x*c-y*s+center[0]
    else:
        ny,nx = y,x
    y,x = ny,nx
    if move[0] and not move[1]:
        length = dist(y,x,center[1],center[0])
        ny,nx = center[1]+(y-center[1])/length*(length+5),center[0]+(x-center[0])/length*(length+5)
    elif move[1] and not move[0]:
        length = dist(y,x,center[1],center[0])
        ny,nx = center[1]+(y-center[1])/length*(length-5),center[0]+(x-center[0])/length*(length-5)
    if dist(y,x,center[1],center[0])<50:
        y,x = ny,nx
        length = dist(y,x,center[1],center[0])
        ny,nx = center[1]+(y-center[1])/length*(50),center[0]+(x-center[0])/length*(50)
    elif dist(y,x,center[1],center[0])>280:
        y,x = ny,nx
        length = dist(y,x,center[1],center[0])
        ny,nx = center[1]+(y-center[1])/length*(280),center[0]+(x-center[0])/length*(280)
    ny = 600-ny
    return [ny,nx]


def updateBulletPos(b1,y,x,spd):
    dy = math.sin(b1.angle*3.14/180)
    dx = math.cos(b1.angle*3.14/180)
    return (b1.rect.centery + spd*dy, b1.rect.centerx + spd*dx)


def updateCoinPos(c1,y,x,spd):
    dy = math.sin(c1.angle*3.14/180)
    dx = math.cos(c1.angle*3.14/180)
    return (c1.rect.centery + spd*dy, c1.rect.centerx + spd*dx)


def runGame(screen):
    screen.fill((0,0,0))
    clock = pygame.time.Clock()

    #misc. variables
    center = [400,300]
    score = 0
    start = pygame.time.get_ticks()
    allSprites = pygame.sprite.Group()

    #variables concerning player
    p1 = player()
    p1.rect.centery = 100
    p1.rect.centerx = 400
    y = 100
    x = 400
    allSprites.add(p1)
    lives = 3

    #variables concerning bullets and coins
    bullets = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    interval = 60
    cnt = 0
    spd = 2

    while lives:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0,0,0))
        allSprites.draw(screen)
        pygame.display.flip()
        rev = [0,0] #direction of revolution
        move = [0,0] #direction of movement (toward or away)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rev[0] = 1
        if keys[pygame.K_RIGHT]:
            rev[1] = 1
        if keys[pygame.K_UP]:
            move[0] = 1
        if keys[pygame.K_DOWN]:
            move[1] = 1
        y,x = updatePlayerPos(y,x,rev,move,center)
        p1.rect.centery,p1.rect.centerx = y,x

        toRemove = []

        for i in bullets:
            i.rect.centery,i.rect.centerx = updateBulletPos(i,p1.rect.centery,p1.rect.centerx,spd)
            if i.rect.centery>=600 or i.rect.centery<=0 or i.rect.centerx>=800 or i.rect.centerx<=0:
                toRemove.append(i)

        for i in toRemove:
            bullets.remove(i)
            allSprites.remove(i)

        toRemove = []

        for i in coins:
            i.rect.centery,i.rect.centerx = updateBulletPos(i,p1.rect.centery,p1.rect.centerx,spd)
            if i.rect.centery>=600 or i.rect.centery<=0 or i.rect.centerx>=800 or i.rect.centerx<=0:
                toRemove.append(i)

        for i in toRemove:
            coins.remove(i)
            allSprites.remove(i)

        cnt += 1
        score += 1
        if cnt==interval: #spawn new entity
            if randint(1,10)==1: #new coin
                c1 = coin(randint(5,15),randint(0,359))
                c1.rect.centerx,c1.rect.centery = 400,300
                coins.add(c1)
                allSprites.add(c1)
            else:
                b1 = bullet(randint(5,15),randint(0,359))
                b1.rect.centerx,b1.rect.centery = 400,300
                bullets.add(b1)
                allSprites.add(b1)
            cnt = 0

        if score%1000==0:
            if interval >= 10:
                interval //= 2
            if spd <= 8:
                spd += 0.5
            cnt = min(cnt,interval-1)

        clock.tick(60)



def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Rotation Game")
    title = pygame.image.load("title.png")
    play = pygame.image.load("title-play.png")
    settings = pygame.image.load("title-settings.png")
    controls = pygame.image.load("title-controls.png")
    clock = pygame.time.Clock()
    screen.blit(title,(0,0))
    pygame.display.flip()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        bx,by = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if bx >= 304 and bx <= 509:
            if by >= 376 and by <= 431:
                screen.blit(play,(0,0))
                if 1 in click:
                    runGame(screen)
                    screen.blit(title,(0,0))
            elif by >= 446 and by <= 501:
                screen.blit(settings,(0,0))
            elif by >= 518 and by <= 573:
                screen.blit(controls,(0,0))
            else:
                screen.blit(title,(0,0))
        else:
            screen.blit(title,(0,0))
        pygame.display.flip()
        clock.tick(60)


if __name__=='__main__':
    main()