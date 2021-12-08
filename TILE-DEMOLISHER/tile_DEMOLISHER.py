# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 19:26:56 2021

@author: Alex
"""

import pygame as pg
import numpy as np
import time


# ----------------------------------------------------------------------


class Tiles:
    def __init__(self, row, col):
        TF = [True, False]
        self.row = row
        self.col = col
        self.da = round(WIDTH/(ROW))  # ШИРИНА
        self.db = round(HEIGHT/(COL)/2)  # ДЛИНА
        self.maxHP = 5
        
        self.tile_exist = [[np.random.choice(TF) for i in range(self.row)]
                           for j in range(self.col)]
        self.tRect = [[pg.Rect(i*self.da, j*self.db, self.da, self.db)
                       for i in range(self.row)] for j in range(self.col)]
        self.tSurf = [[pg.Surface((self.da, self.db)) for i in range(self.row)]
                      for j in range(self.col)]
        self.colors = [[tuple([round(155*np.random.rand()) for _ in range(3)])
                        for i in range(self.row)] for j in range(self.col)]
        self.hps = [[round(self.maxHP*np.random.rand())
                     for i in range(self.row)] for j in range(self.col)]


    def draw(self):
        for i in range(self.col):
            for j in range(self.row):
                if self.tile_exist[i][j]:
                    self.tSurf[i][j].fill(self.colors[i][j])
                    DISPLAYSURF.blit(self.tSurf[i][j], self.tRect[i][j])


    def getTile_ex(self):
        return self.tile_exist


    def check_hp(self):
        for i in range(self.col):
            for j in range(self.row):
                if self.tile_exist[i][j]:
                    if self.hps[i][j] < 0:
                        self.tile_exist[i][j] = False
                        gen_bonus((j*self.da,i*self.db))


    def checkBallColl(self, pos):
        x, y = pos
        res = [False for _ in range(8)]
        coll = False
        for i in range(self.col):
            for j in range(self.row):
                if self.tile_exist[i][j]:
                    lt, rt = self.tRect[i][j].left, self.tRect[i][j].right
                    up, dw = self.tRect[i][j].top, self.tRect[i][j].bottom
                    if x > lt-R and x < lt and (y > up and y < dw): 
                        res[0] = True #LEFT
                        coll = True
                    if x < rt+R and x > rt and (y > up and y < dw): 
                        res[1] = True #RIGHT
                        coll = True
                    if y > up-R and y < up and (x > lt and x < rt): 
                        res[2] = True #TOP
                        coll = True
                    if y < dw+R and y > dw and (x > lt and x < rt):
                        res[3] = True #BOTTOM
                        coll = True
                    
                    if x > lt-R and x < lt and (y > up-R and y < up): 
                        res[4] = True #TOPLEFT
                        coll = True
                    if x < rt+R and x > rt and (y > up-R and y < up): 
                        res[5] = True #TOPRIGHT
                        coll = True
                    if x < rt+R and x > rt and (y > dw and y < dw+R): 
                        res[6] = True #BOTRIGHT
                        coll = True
                    if x > lt-R and x < lt and (y > dw and y < dw+R): 
                        res[7] = True #BOTLEFT
                        coll = True
                    
                    if coll:
                        self.hps[i][j] -= 1
                        return res
        return False


    def noTiles(self):
        exist = False
        for i in range(self.col):
            for j in range(self.row):
                if self.tile_exist[i][j]:
                    exist = True
        if not exist:
            return True
    
    
    def countTiles(self):
        n = 0
        for i in range(self.col):
            for j in range(self.row):
                if self.tile_exist[i][j]:
                    n += 1
        return n


# ----------------------------------------------------------------------


class Ball:
    def __init__(self, x, y, n):
        self.x, self.y = x, y
        self.V = 500
        self.Vx, self.Vy = -self.V*n[0], -self.V*n[1]
        self.r = R
        self.setRandColor()

    def movement(self):
        self.x += self.Vx/FPS
        self.y += self.Vy/FPS

    def draw(self):
        pos = (self.x, self.y)
        pg.draw.circle(DISPLAYSURF, self.color, pos, self.r)

    def checkPos(self):
        if self.x > WIDTH - self.r:
            self.Vx = -abs(self.Vx)
            self.x = WIDTH - self.r
        if self.x < self.r:
            self.Vx = abs(self.Vx)
            self.x = self.r
        if self.y > HEIGHT - self.r:
            return True
        if self.y < self.r:
            self.Vy = abs(self.Vy)
        return False

    def getPos(self):
        return self.x, self.y

    def setRandColor(self):
        clr = [255, 127, 0]
        self.color = tuple([np.random.choice(clr) for _ in range(3)])
        while self.color == (255, 255, 255):
            self.color = tuple([np.random.choice(clr) for _ in range(3)])
    
    
    def deflect(self, n):
        if n != None:
            self.Vx = self.V *np.sin(np.pi*n/2)
            self.Vy = -self.V *np.cos(np.pi*n/2)
    
    
    def tile_colly(self):
        self.Vx = self.Vx
        self.Vy = -self.Vy
    
    
    def tile_collx(self):
        self.Vx = -self.Vx
        self.Vy = self.Vy
    
    def tile_collxy(self):
        self.Vx = -self.Vx
        self.Vy = -self.Vy


# ----------------------------------------------------------------------

            
class Bonus:
    def __init__(self, pos):
        self.x, self.y = pos
        self.Vx = 0
        self.Vy = 100
        self.width = 50
        self.height = 50
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.surf = pg.image.load('bonus.png')
    
    
    def draw(self):
        DISPLAYSURF.blit(self.surf, self.rect)
    
    
    def movement(self):
        self.x += self.Vx/FPS
        self.y += self.Vy/FPS
        self.rect.move_ip(self.Vx/FPS, self.Vy/FPS)
    
    
    def checkClick(self, pos):
        x, y = pos
        lt, rt = self.rect.left, self.rect.right
        up, dw = self.rect.top, self.rect.bottom
        if x > lt and x < rt:
            if y > up and y < dw:
                return True
        return False


# ----------------------------------------------------------------------


class Platform:
    def __init__(self):
        self.x, self.y = 0,0
        self.width = 100
        self.height = 10
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x , HEIGHT-30)
        self.surf = pg.Surface((self.width, self.height))
    
    
    def draw(self):
        DISPLAYSURF.blit(self.surf, self.rect)
    
    
    def movement(self):
        self.x = pg.mouse.get_pos()[0]
        self.rect.center = (self.x , HEIGHT-50)
    
    
    def platColl(self, pos):
        x,y = pos
        lt, rt = self.rect.left, self.rect.right
        up, dw = self.rect.top, self.rect.bottom
        if x > lt and x < rt:
            if y > up and y < dw:
                return (x - lt - (rt-lt)/2) / ((rt-lt)/2) # (-1, 1)
        return None
        

# ----------------------------------------------------------------------


def check_wall(ball):
    global balls_list
    x, y = ball.getPos()
    if y > HEIGHT or y < 0:
        balls_list.remove(ball)


def getN():
    x, y = pg.mouse.get_pos()
    dx, dy = ball_spawn[0]-x, ball_spawn[1]-y
    r = np.sqrt(dx**2 + dy**2)
    return dx/r, dy/r


def gen_bonus(pos):
    global bonus_list
    ran = 100*np.random.rand()
    if ran > 80:
        bonus_list.append(Bonus(pos))


# ----------------------------------------------------------------------


def main():
    global WIDTH, HEIGHT, FPS, ROW, COL, ball_spawn, DISPLAYSURF, R, bonus_list
    WIDTH = 700
    HEIGHT = 700
    FPS = 60
    ROW = 10
    COL = 15
    BGCOLOR = (255, 255, 255)
    dt = 0.5
    ball_spawn = (350, 590)
    R = 10

    pg.init()
    DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT))
    DISPLAYSURF.fill(BGCOLOR)
    pg.display.set_caption("TILE DEMOLISHER")
    pg.display.set_icon(pg.image.load('ball.bmp'))
    clock = pg.time.Clock()

    tiles_var = Tiles(ROW, COL)
    balls_list = [Ball(ball_spawn[0], ball_spawn[1], getN())]
    bonus_list = []
    plat_var = Platform()

    run = True
    st = time.time()
    while run:
        DISPLAYSURF.fill(BGCOLOR)

        # PYGAME EVENTS
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                run = False
        mp = pg.mouse.get_pressed()
        if mp[0]:
            for bon in bonus_list:
                if bon.checkClick(pg.mouse.get_pos()):
                    try:
                        bonus_list.remove(bon) #KILL BONUS
                        #ЗАПУСК БОНУСА
                        balls_list.append(Ball(ball_spawn[0], ball_spawn[1], getN()))
                    except: pass

        # BALL EVENTS
        for ball in balls_list:
            ball.draw()
            ball.movement()
            check_wall(ball)
            
            ball.deflect(plat_var.platColl(ball.getPos()))

            case1 = tiles_var.checkBallColl(ball.getPos())
            if case1 != False:
                if case1[0] or case1[1]:
                    # balls_list.remove(ball) # KILL BALL
                    ball.tile_collx()
                if case1[2] or case1[3]:
                    ball.tile_colly()
                if case1[4] or case1[5] or case1[6] or case1[7]:
                    ball.tile_collxy()
                

            ps = ball.checkPos()
            if ps:
                try:
                    balls_list.remove(ball)
                except:
                    pass
        # if time.time()-st > dt:
        #     balls_list.append(Ball(ball_spawn[0], ball_spawn[1], getN()))
        #     st = time.time()


        # TILE EVENTS
        tiles_var.draw()
        if tiles_var.noTiles():
            tiles_var = Tiles(ROW, COL)
        tiles_var.check_hp()
        # tiles_n = tiles_var.countTiles()
        # dt = 1/tiles_var.countTiles() if tiles_n !=0 else 1
        
        #PLATFORM EVENTS
        plat_var.movement()
        plat_var.draw()

        # UPDATES
        for bon in bonus_list:
            bon.movement()
            bon.draw()
            
        pg.display.update()
        clock.tick(FPS)

    pg.quit()


# ----------------------------------------------------------------------


if __name__ == '__main__':
    main()
