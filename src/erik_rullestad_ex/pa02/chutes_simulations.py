# -*- coding: utf-8 -*-

__author__ = 'Erik Rullestad, Håvard Molversmyr'
__email__ = 'erikrull@nmbu.no, havardmo@nmbu.no'


import random
from collections import Counter, defaultdict


class Board:
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
        elif position in self.chutes:
            return position - self.chutes[position]
        else:
            return 0


class Player:
    def __init__(self, board):
        self.board = board
        self.position = 0
        self.n_steps = 0

    def move(self):
        die_roll = random.randint(1, 6)
        self.position = self.get_position() + die_roll

        self.position += self.board.position_adjustment(self.position)

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
        if self.get_position() in self.board.chutes.values():
            die_roll = random.randint(1, 6)
            self.position = self.get_position() + die_roll + self.extra_steps

            self.position += self.board.position_adjustment(self.position)

            self.n_steps += 1
        else:
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
        if self.get_position() in self.board.ladders.values():
            die_roll = random.randint(1, 6)
            if die_roll >= self.dropped_steps:
                self.position = (
                    self.get_position() + die_roll - self.dropped_steps
                )

                self.position += self.board.position_adjustment(self.position)

                self.n_steps += 1
            else:
                pass
        else:
            super().move()

    def get_position(self):
        return self.position

    def get_steps(self):
        return self.n_steps


class Simulation:
    def __init__(self, player_field=None, board=None,
                 seed=None, randomize_players=True):
        self.player_field = player_field
        self.board = board
        if self.board is None:
            self.board = Board()
        self.seed = seed
        self.randomize_players = randomize_players
        if self.randomize_players is True:
            random.shuffle(self.player_field)
        else:
            pass
        self.sim_res = []

    def single_game(self):
        player_list = []
        for player_class in self.player_field:
            player_list.append(player_class(self.board))

        while True:
            for player in player_list:
                player.move()

                if player.board.goal_reached(player.get_position()):
                    nos = player.get_steps()
                    wc = type(player).__name__
                    return nos, wc

    def run_simulation(self, sim_num):
        for _ in range(sim_num):
            self.sim_res.append(self.single_game())

    def get_results(self):
        return self.sim_res

    def winners_per_type(self):
        return dict(Counter(elem[1] for elem in self.get_results()))

    def durations_per_type(self):
        durations = defaultdict(list)
        for value, key in self.get_results():
            durations[key].append(value)
        return dict(durations)

    def players_per_type(self):
        class_list = [cls.__name__ for cls in self.player_field]
        return dict(Counter(class_list))
