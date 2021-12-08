# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 13:12:53 2021

@author: Alex Akinin

Игра в виселицу на русском
"""

from russ_words import russ_words_var as my_dict
from random import choice as choice


alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


class Hangman_game:
    def __init__(self):
        self.choice = choice(my_dict)
        self.word, self.frec, self.word_score = self.choice
        self.guessed_sec = [False for _ in range(len(self.word))]
        self.guessed_print = ['_' for _ in range(len(self.word))]
        self.lives = len(self.word) + 7
        self.guess_list = []
        self.runGame()

    def getGuess(self):
        valid_input = False

        while not valid_input:
            inp = input('Выбери букву: ')
            if inp in alph and self.guessInList(inp):
                valid_input = True

        self.guess = inp.lower()
        self.guess_list.append(self.guess)

    def guessInWord(self):
        Guessed = False
        tmp_word = self.word
        for i in range(len(tmp_word)):
            if tmp_word[i] == self.guess:
                self.guessed_sec[i] = True
                self.guessed_print[i] = self.guess
                Guessed = True

        if Guessed:
            return True
        self.lives -= 1
        return False

    def printCurState(self):
        for i in self.guessed_print:
            print(i, end=' ')
        print()
        print(f'У тебя {self.lives} жизней')

    def printTF(self, TF):
        if TF:
            print(f'YES YES YES!! Буква "{self.guess}" есть в слове')
        else:
            print(f'NO NO NO!! Буквы "{self.guess}" НЕТ в слове')

    def guessInList(self, guess):
        if guess in self.guess_list:
            print(f'Буква "{guess}" уже была')
            return False
        else:
            return True

    def checkWin(self):
        if False in self.guessed_sec:
            return False
        else:
            return True

    def runGame(self):
        while self.lives > 0:
            self.printCurState()
            self.getGuess()
            self.printTF(self.guessInWord())
            print()

            if self.checkWin():
                break

        if self.lives != 0:
            print(
                f'Ты выиграл и заработал {self.word_score} очков! \nСлово {self.word}')
        else:
            print(f'Ты проиграл. Слово {self.word}')


# ----------------------------------------------------------------------


Hangman_game()

end = False
while not end:
    again = input('Хочешь поиграть ещё? д/н : ')
    if again == 'д':
        Hangman_game()
    else:
        end = True
