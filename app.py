#!/usr/bin/env python

from entities.game import Game


if __name__ == "__main__":
    game = Game()
    game.add_human_player("Player1")
    # game.add_cpu_player("CPU2")
    game.add_cpu_player("CPU1")
    game.begin_game()
