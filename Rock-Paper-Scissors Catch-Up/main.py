"""
DONE: basic Player functionality
DONE: global vars modile
DONE: PyGame initialization
DONE: Players initialization
DONE: write show() method for players
DONE: create Players icons
DONE: ability to resize icons
DONE: replace if statements with dicts in Player class
TODO: replace teams in Player class with special class variable
DONE: death
DONE: type hinting
TODO: add controlled player
"""


#########################################################################################


import numpy as np
import pygame as pg

import global_vars as g
from player import Player


#########################################################################################


def init_players(mode: str) -> list[Player]:
    ''' Initialization of players '''
    if mode == 'random':
        player_total = g.R_NUM + g.P_NUM + g.S_NUM
        players = [Player() for i in range(player_total)]
    else:
        players = []
        for _ in range(g.R_NUM):
            players.append(Player(team='R'))
        for _ in range(g.P_NUM):
            players.append(Player(team='P'))
        for _ in range(g.S_NUM):
            players.append(Player(team='S'))
    return players


def check_dead_players(main_player: Player, players: list[Player]) -> list[Player]: 
    ''' Check if players are dead '''
    if check_main_player_dead(main_player, players):
        return []

    dead_indecies = []
    for i, pl_1 in enumerate(players):
        for j, pl_2 in enumerate(players):
            if i == j:
                continue
            if pl_1.relation(pl_2) == 'food':
                if pl_1.dist(pl_2) < g.DEATH_RADIUS:
                    dead_indecies.append(i)
    
    survived_list = []
    for i, pl in enumerate(players):
        if not (i in dead_indecies):
            survived_list.append(pl)
    return survived_list


def check_main_player_dead(main_player: Player, players: list[Player]) -> bool: 
    for player in players:
        if main_player.relation(player) == 'food':
            if main_player.dist(player) < g.DEATH_RADIUS:
                return True
    return False


def check_winners(players: list[Player]) -> bool:
    ''' Check teams counts '''
    r_count, p_count, s_count = teams_count(players)

    if r_count == 0 and p_count == 0 and s_count == 0:
        # print('tie')
        return False
    if r_count != 0 and p_count == 0 and s_count == 0:
        # print('ROCK winner')
        return False 
    if r_count == 0 and p_count != 0 and s_count == 0:
        # print('PAPER winner')
        return False 
    if r_count == 0 and p_count == 0 and s_count != 0:
        # print('SCISSORS winner')
        return False
    return True


def teams_count(players: list[Player]) -> tuple[int]:
    ''' Count team players '''
    r_count, p_count, s_count = 0, 0, 0
    for player in players:
        curr_team = player.get_team()
        if curr_team == 'R':
            r_count += 1
        elif curr_team == 'P':
            p_count += 1
        elif curr_team == 'S':
            s_count += 1
    return r_count, p_count, s_count


def output_teams_count(dspsurf: pg.Surface, players: list[Player], font: pg.font) -> None:
    ''' Output team counts on to a screen '''
    r_c, p_c, s_c = teams_count(players)
    msg1 = f'Rock count: {r_c}'
    msg2 = f'Paper count: {p_c}'
    msg3 = f'Scissors count: {s_c}'
    text_surf1 = font.render(msg1, False, (0, 0, 0))
    text_surf2 = font.render(msg2, False, (0, 0, 0))
    text_surf3 = font.render(msg3, False, (0, 0, 0))
    dspsurf.blit(text_surf1, (5,5))
    dspsurf.blit(text_surf2, (5,25))
    dspsurf.blit(text_surf3, (5,45))


def vec_to_cursor(main_player: Player):
    vec = np.array(pg.mouse.get_pos()) - main_player.get_pos()
    return vec/np.sqrt(vec.dot(vec)) * main_player.max_speed


#########################################################################################


def main(): 
    # Initialize players
    players = init_players(g.SPAWN_MODE)
    main_player = Player()
    main_player.set_pos(np.array([g.WIDTH/2, g.HEIGHT/2]))

    # PyGame init business
    pg.init()
    pg.font.init() 
    DISPLAYSURF = pg.display.set_mode((g.WIDTH, g.HEIGHT))
    pg.display.set_caption(g.WINDOW_NAME)
    clock = pg.time.Clock()
    FONT = pg.font.SysFont('Bahnschrift', 20)

    # Main gameloop
    gameLoop = True
    while gameLoop:

        # PyGame loop business
        DISPLAYSURF.fill(g.BG_COLOR)
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gameLoop = False

        # Player loop business
        players = check_dead_players(main_player, players)
        if len(players) == 0:
            players = init_players(g.SPAWN_MODE)
            continue
        if not check_winners(players):
            players = init_players(g.SPAWN_MODE)
            continue
        
        main_player.set_vel(vec_to_cursor(main_player))
        for player in players:
            player.calculate_velocity(players+[main_player,])
        
        main_player.update()
        main_player.frame(DISPLAYSURF)
        main_player.check_walls()
        main_player.show(DISPLAYSURF)
        for player in players:
            player.update()
            player.check_walls()
            player.show(DISPLAYSURF)

        output_teams_count(DISPLAYSURF, players+[main_player,], FONT)
        
        # Update display
        pg.display.update()
        clock.tick(g.FPS)
    
    # Close window
    pg.quit()

#########################################################################################

if __name__ == '__main__':
    main()