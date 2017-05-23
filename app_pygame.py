import pygame
import sys

from pygame.locals import *
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
        self.cards_sprites = pygame.sprite.Group()
        self.hand_sprites = pygame.sprite.Group()
        self.selected_hand_card = None
        self.selected_table_cards = []

    def __generate_sprite(self, card, posx, posy, index, allow_click=True):
        sprite = CardSprite(card, posx, posy, index)
        self.screen.blit(sprite.image, sprite.rect)
        if allow_click:
            self.cards_sprites.add(sprite)
        return sprite

    def __update_board(self):
        background_image = load_image('images/background.jpg')
        self.screen.blit(background_image, (0, 0))
        self.cards_sprites.empty()
        self.hand_sprites.empty()
        # Player 1 Cards
        index = 0
        for card in self.game.players[0].hand:
            sprite = self.__generate_sprite(card, 300+(index*100), HEIGHT-175, index)
            self.hand_sprites.add(sprite)
            index += 1

        # Player 2 Cards
        index = 0
        for card in self.game.players[1].hand:
            self.__generate_sprite(card, 300+(index*100), 25, index, False)
            index += 1

        # Table Cards
        index = 0
        for card in self.game.table:
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

            self.__generate_sprite(card, posx, posy, index)
            index += 1

        # MESSAGES
        text, position = draw_text("ROUND %d" % self.game.round, WIDTH-100, HEIGHT/2)
        self.screen.blit(text, position)
        text, position = draw_text("Points: %d" % self.game.players[1].points, WIDTH-100, 50)
        self.screen.blit(text, position)
        text, position = draw_text("Escobas: %d" % self.game.players[1].escoba, WIDTH-100, 100)
        self.screen.blit(text, position)
        text, position = draw_text("Points: %d" % self.game.players[0].points, WIDTH-100, HEIGHT-100)
        self.screen.blit(text, position)
        text, position = draw_text("Escobas: %d" % self.game.players[0].escoba, WIDTH-100, HEIGHT-50)
        self.screen.blit(text, position)

        if self.game.winner:
            text, position = draw_text("THE WINNER IS %s" % self.game.winner.name, (WIDTH/2) - 100, HEIGHT / 2)
            self.screen.blit(text, position)

        pygame.display.flip()

    def start(self):
        pygame.display.set_caption("PYEscoba")
        clock = pygame.time.Clock()

        player1 = HumanPlayer("Player1", self.game)
        self.game.add_player(player1)
        player2 = CpuPlayer("CPU", self.game)
        self.game.add_player(player2)

        while not self.game.someone_win():
            time = clock.tick(30)  # framerate
            self.game.round += 1
            self.game.generate_deck()
            self.game.mix_deck()
            self.game.give_cards_to_table()
            while 1:
                self.game.give_cards_to_players()
                self.__update_board()
                for x in range(0, 3):
                    for player in self.game.players:
                        if isinstance(player, HumanPlayer):
                            self.play_human(player1)
                            self.__update_board()
                        else:
                            player.play()
                            self.__update_board()
                if not self.game.deck:
                    break
            self.game.update_points()
            self.game.clear_players()
        self.__update_board()
        pygame.time.wait(5000)

    def play_human(self, player1):
        need_reload = False
        while True:
            if need_reload:
                self.__update_board()
                need_reload = False

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left Click
                    for sprite in self.cards_sprites:
                        if sprite.rect.collidepoint(event.pos):
                            if sprite == self.selected_hand_card or sprite.index in self.selected_table_cards \
                                    or (self.selected_hand_card is not None and sprite in self.hand_sprites):
                                need_reload = True
                                self.selected_table_cards = []
                                self.selected_hand_card = None
                            else:
                                if sprite in self.hand_sprites:
                                    self.selected_hand_card = sprite.index
                                else:
                                    self.selected_table_cards.append(sprite.index)
                                text, position = draw_text("SELECTED", sprite.rect.centerx, sprite.rect.y - 10)
                                self.screen.blit(text, position)
                                pygame.display.update()
                                if self.selected_hand_card is not None and self.selected_table_cards != []:
                                    result = player1.make_a_move(self.selected_hand_card, self.selected_table_cards)
                                    if result:
                                        return
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:  # Right Click
                    for sprite in self.cards_sprites:
                        if sprite.rect.collidepoint(event.pos) and sprite in self.hand_sprites:
                            player1.throw_card(sprite.index)
                            return


if __name__ == '__main__':
    pygame.init()
    app = Application()
    app.start()
