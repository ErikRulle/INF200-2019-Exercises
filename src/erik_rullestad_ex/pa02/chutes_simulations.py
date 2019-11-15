# -*- coding: utf-8 -*-

__author__ = 'Erik Rullestad, Eirik Høyheim'
__email__ = 'erikrull@nmbu.no, eirihoyh@nmbu.no'


import random


class Board():
    default_ladders = {1: 40, 8: 10, 36: 52, 43: 62, 49: 79, 65: 82, 68: 85}
    default_chutes = {24: 5, 33: 3, 42: 30, 56: 37, 64: 27, 74: 12, 87: 70}

    def __init__(self, ladders=None, chutes=None, goal=90):
        self.ladders = ladders
        if self.ladders is None:
            self.ladders = self.default_ladders
        self.chutes = chutes
        if self.chutes is None:
            self.chutes = self.default_chutes
        self.goal = goal

    def goal_reached(self, position):
        return position >= self.goal

    def position_adjustment(self, position):
        if position in self.ladders:
            return self.ladders[position] - position
        if position in self.chutes:
            return position - self.chutes[position]


class Player():

    def __init__(self, board):
        self.board = board
        self.position = 0
        self.n_steps = 0

    def move(self):
        die_roll = random.randint(1, 6)
        self.position = self.get_position() + die_roll

        self.board.position_adjustment(self.position)

        self.n_steps += 1

    def get_position(self):
        return self.position

    def get_steps(self):
        return self.n_steps


class ResilientPlayer(Player):
    default_extra_steps = 1

    def __init__(self, board, extra_steps=None):
        super().__init__(board)
        self.extra_steps = extra_steps
        if self.extra_steps is None:
            self.extra_steps = self.default_extra_steps

    def move(self):
        super().move()

    def get_position(self):
        return self.position

    def get_steps(self):
        return self.n_steps


class LazyPlayer(Player):
    default_dropped_steps = 1

    def __init__(self, board, dropped_steps=None):
        super().__init__(board)
        self.dropped_steps = dropped_steps
        if self.dropped_steps is None:
            self.dropped_steps = self.default_dropped_steps

    def move(self):
        super().move()

    def get_position(self):
        return self.position

    def get_steps(self):
        return self.n_steps


class Simulation():
    pass