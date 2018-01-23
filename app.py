#!/usr/bin/env python

from entities.game_controller import GameController


if __name__ == "__main__":
    GAME = GameController()
    GAME.add_human_player("Player1")
    # game.add_cpu_player("CPU2")
    GAME.add_cpu_player("CPU1")
    GAME.begin_game()
