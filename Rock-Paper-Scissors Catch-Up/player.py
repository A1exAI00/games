import numpy as np
import random
import pygame as pg
from typing import Type

import global_vars as g

#########################################################################################

class Player():
    def __init__(self, team:str=None) -> None: 
        self.pos = np.array([random.random() * g.WIDTH, random.random() * g.HEIGHT])
        self.vel = np.zeros(2)
        self.team = random.choice(['R', 'P', 'S']) if team == None else team
        self.max_speed = {'R':g.R_SPEED, 'P':g.P_SPEED, 'S':g.S_SPEED}[self.team]

        # PyGame variables
        texture_w = {'R':g.R_TEXTURE_WIDTH, 
                     'P':g.P_TEXTURE_WIDTH, 
                     'S':g.S_TEXTURE_WIDTH}[self.team]
        texture_h = {'R':g.R_TEXTURE_HEIGHT, 
                     'P':g.P_TEXTURE_HEIGHT, 
                     'S':g.S_TEXTURE_HEIGHT}[self.team]
        self.rect = pg.Rect(self.pos[0], self.pos[1], texture_w, texture_h)
        texture_path = {'R':f'{g.TEXTURE_PATH}\\R.png', 
                        'P':f'{g.TEXTURE_PATH}\\P.png', 
                        'S':f'{g.TEXTURE_PATH}\\S.png'}[self.team]
        self.surf = pg.image.load(texture_path) 
        self.surf = pg.transform.scale(self.surf, (texture_w, texture_h))
        
    def calculate_velocity(self, players_list: list[Type['Player']]) -> None: 
        ''' Calculate player velocity '''
        foe_player, food_player = self.get_nearest_players(players_list)
        foe_vec, food_vec = self.pos - foe_player.get_pos(), self.pos - food_player.get_pos()
        foe_dist, food_dist = self.dist(foe_player), self.dist(food_player)

        v_1 = - foe_vec/foe_dist /(foe_dist*g.SPEED_MULT) if foe_dist != 0 else 0
        v_2 = + food_vec/food_dist /(food_dist) if food_dist != 0 else 0
        
        v_sum = v_1 + v_2
        self.vel = v_sum/np.sqrt(v_sum.dot(v_sum)) * self.max_speed
    
    def get_nearest_players(self, players_list: list[Type['Player']]) -> tuple[Type['Player']]:
        ''' Get nearest foe and food players '''
        foe_i, foe_dist = 0, 1e10 
        food_i, food_dist = 0, 1e10

        # Get nearest foe and food indecies
        for i, pl in enumerate(players_list): 
            if self.relation(pl) == 'same':
                continue
            if self.relation(pl) == 'foe': 
                curr_dist = self.dist(pl)
                if curr_dist < foe_dist:
                    foe_dist,foe_i = curr_dist, i
            elif self.relation(pl) == 'food': 
                curr_dist = self.dist(pl)
                if curr_dist < food_dist:
                    food_dist, food_i = curr_dist, i
        return players_list[foe_i], players_list[food_i]

    def dist(self, other: Type['Player']) -> float:
        ''' Calculate distance between players '''
        vec = (self.pos - other.get_pos())
        return np.sqrt(vec.dot(vec))

    def relation(self, other: Type['Player']) -> str:
        m_team = self.get_team()
        o_team = other.get_team()
        if m_team == 'R':
            return {'R':'same', 'P':'food', 'S':'foe'}[o_team]
        if m_team == 'P':
            return {'R':'foe', 'P':'same', 'S':'food'}[o_team]
        if m_team == 'S':
            return {'R':'food', 'P':'foe', 'S':'same'}[o_team]

    def get_pos(self) -> np.ndarray: return self.pos

    def set_pos(self, pos:np.ndarray) -> None: self.pos = pos

    def get_team(self) -> str: return self.team

    def set_vel(self, vel: np.ndarray) -> None: self.vel = vel

    def show(self, dspsurf: pg.Surface) -> None: dspsurf.blit(self.surf, self.rect)

    def update(self) -> None: 
        ''' Update position '''
        self.pos += self.vel
        self.rect.center = self.pos
        self.vel *= 0
    
    def check_walls(self) -> None:
        ''' Check if player is out of screen '''
        if self.pos[0] < 0:
            self.pos[0] = g.FRAME_WIDTH
        elif self.pos[0] > g.WIDTH:
            self.pos[0] = g.WIDTH - g.FRAME_WIDTH
        if self.pos[1] < 0:
            self.pos[1] = g.FRAME_WIDTH
        elif self.pos[1] > g.HEIGHT:
            self.pos[1] = g.HEIGHT - g.FRAME_WIDTH
    
    def frame(self, dspsurf: pg.Surface) -> None: 
        pg.draw.rect(dspsurf, pg.Color((255,200,200)), self.rect, border_radius=5)

#########################################################################################

def test(): 
    p = Player()

#########################################################################################

if __name__ == '__main__':
    test()