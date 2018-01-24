# coding=utf-8
"""
This class manage all the game and its players using the pygame framework
"""

from entities.game_controller import GameController
from pygame_entities.pygame_human_player import PygameHumanPlayer
from pygame_entities.pygame_cpu_player import PygameCpuPlayer


class PyGameController(GameController):

    def __init__(self, app_pygame):
        super(PyGameController, self).__init__()
        self.app_pygame = app_pygame

    def add_human_player(self, name):
        player = PygameHumanPlayer(name, self)
        self._add_player(player)

    def add_cpu_player(self, name):
        player = PygameCpuPlayer(name, self)
        self._add_player(player)
