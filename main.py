import pygame
import math
from random import randint

CIRCLE = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.gfxdraw.aacircle(CIRCLE, 15, 15, 14, (0, 255, 0))
pygame.gfxdraw.filled_circle(CIRCLE, 15, 15, 14, (0, 255, 0))


class bullet(pygame.sprite.Sprite):
    def __init__(self,radius,angle):
        super().__init__()
        self.rect = self.image.get_rect
        self.radius = radius
        self.angle = angle
        self.image = CIRCLE


class coin(pygame.sprite.Sprite):
    def __init__(self,radius,angle):
        super().__init__()
        self.rect = self.image.get_rect
        self.radius = radius
        self.angle = angle
        self.image = CIRCLE


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


def runGame(screen):
    screen.fill((0,0,0))
    clock = pygame.time.Clock()
    center = [400,300]
    lives = 3
    score = 0
    interval = 60
    start = pygame.time.get_ticks()
    bullets = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()
    p1 = player()
    p1.rect.centery = 100
    p1.rect.centerx = 400
    y = 100
    x = 400
    allSprites.add(p1)
    cnt = 0
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



        cnt += 1
        if cnt==interval: #spawn new entity
            if randint(1,10)==1: #new coin
                c1 = coin(randint(15,20),randint(0,359))
                c1.rect.centerx,c1.rect.centery = 400,300
                coins.add(c1)
                allSprites.add(c1)
            else:
                b1 = bullet(randint(15,20),randint(0,359))
                c1.rect.centerx,c1.rect.centery = 400,300
                bullets.add(b1)
                allSprites.add(b1)
            cnt = 0
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