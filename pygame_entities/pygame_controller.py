# coding=utf-8
"""
This class manage all the game and its players using the pygame framework
"""

from entities.game_controller import GameController
from pygame_entities.pygame_human_player import PygameHumanPlayer
from pygame_entities.pygame_cpu_player import PygameCpuPlayer


class PyGameController(GameController):

    def __init__(self):
        super(PyGameController, self).__init__()

    def add_human_pygame_player(self, name, app_pygame):
        player = PygameHumanPlayer(name, self, app_pygame)
        self._add_player(player)

    def add_cpu_pygame_player(self, name, app_pygame):
        player = PygameCpuPlayer(name, self, app_pygame)
        self._add_player(player)
