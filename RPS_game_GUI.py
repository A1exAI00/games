'''
Игра "Камень-ножницы-бумага" с графическим интерфейсом
Первый опыт создания GUI

Date: 03.01.2022
Author: Alex Akinin
'''


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


from PySimpleGUI.PySimpleGUI import theme_background_color
import numpy.random as random
import PySimpleGUI as sg
from time import sleep


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Создание переменных
get_random_move = lambda: random.choice(['r', 'p', 's'])
game_results = [0, 0, 0]

# Создание лэйаута окна и самого окна
sg.theme("DarkBlue3")
layout = [[sg.T('Выбери ход')], 
          [sg.T('Ваш ход:', size=(15,1)), sg.T('Ход компьютера:')],
          [sg.T('', key='-YOURMOVE-', size=(15,1)), sg.T('', key='-PCMOVE-', size=(12,1))],
          [sg.T('', key='-RESULT-', size=(9,1), )],
          [sg.B('Камень'), sg.B('Ножницы'), sg.B('Бумага'), sg.B('Выход', button_color='red',)]]
window = sg.Window('Камень-ножницы-бумага', layout, resizable=True, finalize=True)

# Цикл работы окна
while True:

    # Чтение эвентов
    event, values = window.read()
    if event in (None,'Выход'):
        break
    
    # Проверка, был ли сделан ход 
    move = ''
    pcmove = ''
    if event == 'Камень':
        window['-YOURMOVE-'].update('Камень')
        move = 'r'
    elif event == 'Ножницы':
        window['-YOURMOVE-'].update('Ножницы')
        move = 's'
    elif event == 'Бумага':
        window['-YOURMOVE-'].update('Бумага')
        move = 'p'
    
    # Если не сделан, то возвращаемся в начало цикла
    if not move:
        continue

    # Типа ожидание и получение хода компьютера
    sleep(1)
    pcmove = get_random_move()

    # Вывод хода компьютера
    if pcmove == 'r':
        window['-PCMOVE-'].update('Камень')
    if pcmove == 'p':
        window['-PCMOVE-'].update('Бумага')
    if pcmove == 's':
        window['-PCMOVE-'].update('Ножницы')

    # Сравнивание нашего и компьютерного хода
    if move == pcmove:
        window['-RESULT-'].update('Ничья', background_color=theme_background_color())
        game_results[0] += 1
    elif (move == 'r' and pcmove == 's') or (move == 's' and pcmove == 'p') or (move == 'p' and pcmove == 'r'):
        window['-RESULT-'].update('Выиграл! :)', background_color='green')
        game_results[1] += 1
    else:
        window['-RESULT-'].update('Проиграл :(', background_color='red')
        game_results[2] += 1


# Вывод результатов игры
sg.Popup(f'Ничьи: {game_results[0]}', f'Выигрыши: {game_results[1]}', f'Проигрыши: {game_results[2]}')

# Закрытие окна
window.close()