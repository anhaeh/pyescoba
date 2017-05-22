#!/usr/bin/env python

from entities.game import Game
from entities.human_player import HumanPlayer
from entities.cpu_player import CpuPlayer


if __name__ == "__main__":
    game = Game()
    player1 = HumanPlayer("Player1", game)
    # player1 = CpuPlayer("CPU1", game)
    game.add_player(player1)
    player2 = CpuPlayer("CPU2", game)
    game.add_player(player2)
    game.begin_game()
