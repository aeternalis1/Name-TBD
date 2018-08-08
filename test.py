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
    if dist(y,x,center[1],center[0])<50 and move[1]:
        return [600-y,x]
    elif dist(y,x,center[1],center[0])>280 and move[0]:
        return [600-y,x]
    ny = 600-ny
    return [ny,nx]


def updateBulletPos(b1,spd):
    dy = math.sin(b1.angle*3.14/180)
    dx = math.cos(b1.angle*3.14/180)
    return (b1.rect.centery + spd*dy, b1.rect.centerx + spd*dx)


def updateCoinPos(c1,spd):
    dy = math.sin(c1.angle*3.14/180)
    dx = math.cos(c1.angle*3.14/180)
    return (c1.rect.centery + spd*dy, c1.rect.centerx + spd*dx)


def collided(cur,y,x,radius):
    if dist(cur.rect.centery,cur.rect.centerx,y,x) <= radius+cur.radius:
        return 1
    return 0


def runGame(screen):
    screen.fill((0,0,0))
    clock = pygame.time.Clock()
    myFont = pygame.font.SysFont("monospace",16)
    myFont2 = pygame.font.SysFont("monospace",30)

    #misc. variables
    center = [400,300]
    score = 0
    allSprites = pygame.sprite.Group()

    #variables concerning player
    p1 = player()
    p1.rect.centery = 100
    p1.rect.centerx = 400
    y = 100
    x = 400
    allSprites.add(p1)
    lives = 3
    life = pygame.image.load("life.png")

    #variables concerning bullets and coins
    bullets = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    interval = 60
    cnt = 0
    cnt2 = 0
    spd = 3 #speed of projectiles
    freq = 1 #number of projectiles spawned per interval

    #access high score
    try:
        f = open("highscore.txt", "r")
        print ("ok")
    except:
        f = open("highscore.txt", "w+")
        f.write("0")
        f.close()
        f = open("highscore.txt", "r")
    try:
        if f.mode=='r':
            high = int(f.read())
        f.close()
        f = open("highscore.txt","w")
    except:
        f.close()
        f = open("highscore.txt","w")
        high = 0
        f.write("0")

    while lives>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0,0,0))
        high = max(high,score)
        scoreText = myFont.render("Score: {0}".format(int(score)),1,(255,255,255))
        highText = myFont.render("High: {0}".format(int(high)),1,(255,255,255))
        screen.blit(scoreText,(0,0))
        screen.blit(highText,(0,30))
        for i in range(1,lives+1):
            screen.blit(life,(800-50*i,10))
        allSprites.draw(screen)
        pygame.display.flip()

        toRemove = []

        for i in bullets:
            i.rect.centery, i.rect.centerx = updateBulletPos(i, spd)
            if i.rect.centery >= 600 or i.rect.centery <= 0 or i.rect.centerx >= 800 or i.rect.centerx <= 0:
                toRemove.append(i)
            elif collided(i, p1.rect.centery, p1.rect.centerx, p1.radius):
                toRemove.append(i)
                lives -= 1

        for i in toRemove:
            bullets.remove(i)
            allSprites.remove(i)

        toRemove = []

        for i in coins:
            i.rect.centery, i.rect.centerx = updateBulletPos(i, spd)
            if i.rect.centery >= 600 or i.rect.centery <= 0 or i.rect.centerx >= 800 or i.rect.centerx <= 0:
                toRemove.append(i)
            elif collided(i, p1.rect.centery, p1.rect.centerx, p1.radius):
                toRemove.append(i)
                score += 100*(spd+pow(cnt2,0.5))

        for i in toRemove:
            coins.remove(i)
            allSprites.remove(i)

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
        cnt2 += 1
        score += spd+pow(cnt2,0.5)

        if cnt==interval: #spawn new entity
            angles = []
            cur = int(math.atan2(p1.rect.centery-center[1],p1.rect.centerx-center[0])*180/3.1415)
            for i in range(randint(1,freq)):
                if randint(1,10)==1: #new coin
                    c1 = coin(randint(5,15),randint(cur-90,cur+90))
                    c1.rect.centerx,c1.rect.centery = 400,300
                    while c1.angle in angles:
                        c1.angle = randint(cur-90,cur+90)
                    angles.append(c1.angle)
                    coins.add(c1)
                    allSprites.add(c1)
                else:
                    b1 = bullet(randint(5,15),randint(cur-90,cur+90))
                    b1.rect.centerx,b1.rect.centery = 400,300
                    while b1.angle in angles:
                        b1.angle = randint(cur-90,cur+90)
                    angles.append(b1.angle)
                    bullets.add(b1)
                    allSprites.add(b1)
            cnt = 0

        if cnt2%100==0:
            if spd <= 5:
                spd += 0.05
        if cnt2%1000==0:
            if interval >= 10:
                interval //= 2
            cnt = min(cnt,interval-1)
        if cnt2%2000==0:
            freq += 1

        clock.tick(60)
    high = max(high,int(score))
    f.write(str(int(high)))
    f.close()

    gameover = pygame.image.load("gameover.png")
    playAgain = pygame.image.load("gameover-play.png")
    mainMenu = pygame.image.load("gameover-menu.png")
    curScore = myFont2.render("Your Score: {0}".format(int(score)),1,(255,255,255))
    highScore = myFont2.render("High Score: {0}".format(int(high)),1,(255,255,255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0,0,0))
        bx,by = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if bx >= 117 and bx <= 322 and by >= 500 and by <= 555:
            if 1 in click:
                runGame(screen)
                return
            else:
                screen.blit(playAgain,(0,0))
        elif bx >= 467 and bx <= 672 and by >= 500 and by <= 555:
            if 1 in click:
                return
            else:
                screen.blit(mainMenu,(0,0))
        else:
            screen.blit(gameover,(0,0))
        screen.blit(curScore,(400-curScore.get_rect().width/2,200))
        screen.blit(highScore,(400-highScore.get_rect().width/2,250))
        pygame.display.flip()


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