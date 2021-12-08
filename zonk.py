# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 19:36:01 2021

@author: Alex
"""
from random import choice as choice1
from time import sleep

NUMS_ON_DICE = 6
dices_left = 6
options = []
ROUNDS = 3
tot_score = 0

DICE = list([i for i in range(1, NUMS_ON_DICE+1)])

d_up = ['' ,'|     |', '|     |', '|0    |', '|0   0|', '|0   0|', '|0 0 0|']
d_md = ['' ,'|  0  |', '|0   0|', '|  0  |', '|     |', '|  0  |', '|     |']
d_dw = ['' ,'|     |', '|     |', '|    0|', '|0   0|', '|0   0|', '|0 0 0|']
 

def gen_n_dice(): return [choice1(DICE) for _ in range(6)]


# ----------------------------------------------------------------------


def eq_vals(vals):
    tmp_v = vals.copy()
    s = [0 for i in range(6)]
    for i in range(6):
        for _ in range(6):
            if i+1 in tmp_v:
                s[i] += 1
                tmp_v.remove(i+1)
            else:
                break
    return s


# ----------------------------------------------------------------------


def x_n_oprions(info):
    global options
    s = [[False for i in range(6)] for _ in range(4)]
    
    # h - количество кубиков в комбинации
    for h in range(2,7):
        
        # i - значение кубика, для которого проверяем комбинацию
        for i in range(6):
            if (info[i] > h):
                if i == 0:
                    # [dice_val, number of dices in combination, points]
                    options.append([i+1, h+1, 1000*(h-1)])
                else:
                    options.append([i+1, h+1, (h-1)*(i+1)*100])
    return s


# ----------------------------------------------------------------------


def one_five_option(info):
    global options
    
    # проверить единички в стэке
    if info[0] > 0:
        # [dice_val, number of dices in combination, points]
        options.append([1, 1, 100])
    
    # проверить пятёрочки в стэке
    if info[4] > 0:
        # [dice_val, number of dices in combination, points]
        options.append([5, 1, 50])


# ----------------------------------------------------------------------


def three_pairs_option(info):
    global options
    tmp_info = info.copy()
    pairs = 0
    for _ in range(3):
        if 2 in tmp_info:
            pairs += 1
            tmp_info.remove(2)
    if pairs == 3:
        options.append([7, 6, 750])


# ----------------------------------------------------------------------


def all_diff_option(stack):
    global options
    tmp_stack = stack.copy()
    
    if len(set(tmp_stack)) == 6:
        options.append([0, 6, 1500])


# ----------------------------------------------------------------------


def print_options():
    tmp_opt = options.copy()
    n = 1
    for i in tmp_opt:
        if i[0] == 0:
            print(n,': all diff :', i[1], 'dices :', i[2], 'points')
        elif i[0] == 7:
            print(n,': 3 pairs :', i[1], 'dices :', i[2], 'points')
        else:
            if i[1] == 1:
                print(n,': one option with', i[0], ':',
                  i[1], 'dice :', i[2], 'points')
            else:
                print(n,': x option with', i[0], ':',
                  i[1], 'dices :', i[2], 'points')
        n += 1


# ----------------------------------------------------------------------


def get_answer():
    valid_input = False
    while not valid_input:
        inp = int(input('CHOOCE OPTION! TYPE 0 TO LEAVE : '))
        if inp >= 0 and inp < len(options)+1:
            valid_input = True
    if inp == 0:
        return []
    else:
        return options[inp-1]


# ----------------------------------------------------------------------


def dices_image(st):
    tmp_st = st.copy()
    im_up, im_md, im_dw = '', '', ''
    for i in range(len(tmp_st)):
        im_up += (d_up[tmp_st[i]] + '  ')
        im_md += (d_md[tmp_st[i]] + '  ')
        im_dw += (d_dw[tmp_st[i]] + '  ')
    print(im_up)
    print(im_md)
    print(im_dw)


# ----------------------------------------------------------------------


def game():
    global options
    game_run = True
    dices_left = 6
    score = 0
    while game_run:
        
        # генерация 6 случайных кубиков
        stack = gen_n_dice()
        # stack = [1 for i in range(1,7)]
        # stack = [1, 1, 2, 2, 3, 3]
        
        
        # создание нынешнего стэка и информации о нём
        stack_c = stack.copy()[:dices_left]
        info = eq_vals(stack_c)
        # print(stack_c)
        dices_image(stack_c)
        
        # следующие команды дополняют переменную options
        options = []
        one_five_option(info)
        x_n_oprions(info)
        three_pairs_option(info)
        all_diff_option(stack_c)
        print_options()
        
        if len(options) == 0:
            print('YOU LOST!')
            score = 0
            game_run = False
        else:
            choice = get_answer().copy() # получить ответ и обработать
            if choice == []:
                game_run = False
                print('YOU ENDED THE GAME!')
            else:
                dices_left -= choice[1]
                if dices_left == 0:
                    print('BONUS ROUND!')
                    dices_left = 6
                score += choice[2]

        print('SCORE :', score, '\n')
    return score

# ----------------------------------------------------------------------


# ROUNDS = int(input('HOW MANY ROUNDS TO PLAY : '))
print('YOU WILL PLAY {} ROUNDS'.format(ROUNDS), '\n')

for _ in range(ROUNDS):
# while True:
    cur_score = game()
    tot_score += cur_score
    sleep(1)

print('TOTAL SCORE :', tot_score)
sleep(7)
