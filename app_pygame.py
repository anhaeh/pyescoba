import pygame
import sys
from pygame.locals import *

from entities.card import Card
from entities.cpu_player import CpuPlayer
from entities.game import Game
from entities.human_player import HumanPlayer
from sprites.sprites import load_image, CardSprite

WIDTH = 800
HEIGHT = 600


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

        index = 0
        for card in self.game.players[0].hand:
            sprite = self.cards_sprites["%d%s" % (card.number, card.card_type)]
            self.screen.blit(sprite.image, (100+(index*100), 450))
            index += 1
        index = 0
        for card in self.game.players[1].hand:
            sprite = self.cards_sprites["%d%s" % (card.number, card.card_type)]
            self.screen.blit(sprite.image, (100+(index*100), 25))
            index += 1
        index = 0
        for card in self.game.table:
            sprite = self.cards_sprites["%d%s" % (card.number, card.card_type)]
            self.screen.blit(sprite.image, (100+(index*100), 250))
            index += 1

    def start(self):
        pygame.display.set_caption("PY Escoba de 15")
        clock = pygame.time.Clock()

        player1 = HumanPlayer("P1", self.game)
        # player1 = CpuPlayer("CPU1", self.game)
        self.game.add_player(player1)
        player2 = CpuPlayer("CPU2", self.game)
        self.game.add_player(player2)

        while not self.game.someone_win():
            time = clock.tick(60)  # El parametro es el framerate
            keys = pygame.key.get_pressed()  # nos devuelve las teclas pulsadas en una lista

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            self.game.start_round_for_pygame()

            while True:
                for x in range(0, 3):
                    for player in self.game.players:
                        self.__update_board()
                        pygame.display.flip()
                        # END DRAW
                        player.play()
                if not self.game.deck:
                    break
                self.game.give_cards_to_players()
            self.game.update_points()
            self.game.clear_players()

        print "FINISH in %d ROUNDS" % self.game.round
        print "The winner is %s" % self.game.winner.name
        return 0

if __name__ == '__main__':
    pygame.init()
    app = Application()
    app.start()
