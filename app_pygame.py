import threading

import pygame
import sys

from pygame.locals import *

from entities.card import Card
from entities.cpu_player import CpuPlayer
from entities.game import Game
from entities.human_player import HumanPlayer
from sprites.sprites import load_image, draw_text, CardSprite

WIDTH = 1024
HEIGHT = 800


class Application(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        self.cards_sprites = {}
        self.__generate_sprites()

    def __generate_sprites(self):
        for card_type in Card.CARD_TYPES:
            for i in range(1, 11):
                sprite = CardSprite(i, card_type)
                self.cards_sprites.update({"%d%s" % (i, card_type): sprite})

    def __update_board(self):
        background_image = load_image('images/background.jpg')
        self.screen.blit(background_image, (0, 0))

        # Player 1 Cards
        index = 0
        for card in self.game.players[0].hand:
            sprite = self.cards_sprites["%d%s" % (card.number, card.card_type)]
            self.screen.blit(sprite.image, (300+(index*100), HEIGHT-175))
            index += 1

        # Player 2 Cards
        index = 0
        for card in self.game.players[1].hand:
            sprite = self.cards_sprites["%d%s" % (card.number, card.card_type)]
            self.screen.blit(sprite.image, (300+(index*100), 25))
            index += 1

        # Table Cards
        for index in range(0, self.game.table.__len__()):
            sprite = self.cards_sprites["%d%s" % (self.game.table[index].number, self.game.table[index].card_type)]
            if self.game.table.__len__() <= 5:
                posx = 250+(index*100)
                posy = (HEIGHT/2)-75
            else:
                if index < 5:
                    posx = 250 + (index * 100)
                    posy = (HEIGHT / 2) - 150
                else:
                    posx = 250 + ((index-5) * 100)
                    posy = (HEIGHT / 2)
            self.screen.blit(sprite.image, (posx, posy))

        # MESSAGES
        text, position = draw_text("ROUND %d" % self.game.round, WIDTH-100, HEIGHT/2)
        self.screen.blit(text, position)
        text, position = draw_text("Points: %d" % self.game.players[0].points, WIDTH-100, 50)
        self.screen.blit(text, position)
        text, position = draw_text("Escobas: %d" % self.game.players[0].escoba, WIDTH-100, 100)
        self.screen.blit(text, position)

        text, position = draw_text("Points: %d" % self.game.players[1].points, WIDTH-100, HEIGHT-100)
        self.screen.blit(text, position)
        text, position = draw_text("Escobas: %d" % self.game.players[1].escoba, WIDTH-100, HEIGHT-50)
        self.screen.blit(text, position)

        if self.game.winner:
            text, position = draw_text("THE WINNER IS %s" % self.game.winner.name, (WIDTH/2) - 100, HEIGHT / 2)
            self.screen.blit(text, position)

    def start(self):
        pygame.display.set_caption("PYEscoba")
        clock = pygame.time.Clock()

        player1 = HumanPlayer("P1", self.game)
        # player1 = CpuPlayer("CPU1", self.game)
        self.game.add_player(player1)
        player2 = CpuPlayer("CPU2", self.game)
        self.game.add_player(player2)

        t = threading.Thread(target=self.worker, args=())
        t.daemon = True
        t.start()

        while True:
            time = clock.tick(30)  # framerate
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            self.__update_board()
            pygame.display.flip()

        return 0

    def worker(self):
        self.game.begin_game()


if __name__ == '__main__':
    pygame.init()
    app = Application()
    app.start()
