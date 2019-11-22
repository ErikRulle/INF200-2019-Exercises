# -*- coding: utf-8 -*-

__author__ = 'Erik Rullestad, Håvard Molversmyr'
__email__ = 'erikrull@nmbu.no, havardmo@nmbu.no'


import src.erik_rullestad_ex.pa02.chutes_simulations as cs


class TestBoard:
    def test_goal_reach_success(self):
        board = cs.Board()
        assert board.goal_reached(90)

    def test_goal_reach_fail(self):
        board = cs.Board()
        assert not board.goal_reached(70)

    def test_goal_reach_custom_goal(self):
        board = cs.Board(goal=100)
        assert not board.goal_reached(90)
        assert board.goal_reached(100)

    def test_position_adjustment(self):
        b = cs.Board()
        assert b.position_adjustment(1) is 39


class TestPlayer:
    def test_move(self):
        b = cs.Board(ladders={1: 30, 2: 31, 3: 32, 4: 33, 5: 34, 6: 35},
                     chutes={40: 12, 41: 11, 42: 10, 43: 9})
        p = cs.Player(b)
        pos1 = p.position
        p.move()
        pos2 = p.position
        assert pos1 is not pos2
        assert pos2 - pos1 >= 30
        assert pos2 >= 1
        assert not p.get_position() in b.ladders.keys()
        assert not p.get_position() in b.chutes.keys()

    def test_get_position(self):
        b = cs.Board()
        p = cs.Player(b)
        p.move()
        assert p.get_position() is p.position

    def test_get_steps(self):
        b = cs.Board()
        p = cs.Player(b)
        p.move()
        p.move()
        assert p.get_steps() is 2


class TestSimulation:
    def test_winners_per_type(self):
        player_list = [cs.Player, cs.Player, cs.Player,
                       cs.LazyPlayer, cs.LazyPlayer, cs.ResilientPlayer]
        b = cs.Board()
        pl = cs.Simulation(board=b, player_field=player_list)
        pl.run_simulation(10)
        pl.get_results()
        res = pl.winners_per_type()
        for i in range(3):
            assert list(res.keys())[i] in [
                'Player', 'ResilientPlayer', 'LazyPlayer'
            ]
        for value in res.values():
            assert isinstance(value, int)

    def test_durations_per_type(self):
        player_list = [cs.Player, cs.Player, cs.Player,
                       cs.LazyPlayer, cs.LazyPlayer, cs.ResilientPlayer]
        b = cs.Board()
        pl = cs.Simulation(board=b, player_field=player_list)
        pl.run_simulation(10)
        pl.get_results()
        res = pl.durations_per_type()
        for i in range(3):
            assert list(res.keys())[i] in [
                'Player', 'ResilientPlayer', 'LazyPlayer'
            ]
        for value in res.values():
            assert isinstance(value, list)

    def test_players_per_type(self):
        player_list = [cs.Player, cs.Player, cs.Player,
                       cs.LazyPlayer, cs.LazyPlayer, cs.ResilientPlayer]
        b = cs.Board()
        pl = cs.Simulation(board=b, player_field=player_list,
                           randomize_players=False)
        pl.run_simulation(10)
        pl.get_results()
        res = pl.players_per_type()
        for i in range(3):
            assert list(res.keys())[i] in [
                'Player', 'ResilientPlayer', 'LazyPlayer'
            ]
        assert list(res.values())[0] == 3
        assert list(res.values())[1] == 2
        assert list(res.values())[2] == 1



