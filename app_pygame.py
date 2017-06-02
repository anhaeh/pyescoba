import pygame
from pygame.locals import *
import sys

from entities.game import Game
from sprites.sprites import load_image, draw_text, CardSprite

WIDTH = 1024
HEIGHT = 720


class Application(object):

    def __init__(self):
        self.game = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.cards_sprites = pygame.sprite.Group()
        self.hand_sprites = pygame.sprite.Group()
        self.table_sprites = pygame.sprite.Group()

    def generate_sprite(self, card, posx, posy, index, allow_click=True, show=True):
        sprite = CardSprite(card, posx, posy, index, show)
        self.screen.blit(sprite.image, sprite.rect)
        if allow_click:
            self.cards_sprites.add(sprite)
        return sprite

    def update_screen(self):
        background_image = load_image('images/background.jpg')
        self.screen.blit(background_image, (0, 0))

        self.cards_sprites.empty()
        self.hand_sprites.empty()
        self.table_sprites.empty()

        # Player 1 Cards
        index = 0
        for card in self.game.players[0].hand:
            sprite = self.generate_sprite(card, 350 + (index * 100), HEIGHT - 170, index)
            self.hand_sprites.add(sprite)
            index += 1

        if self.game.players[0].cards:
            self.generate_sprite(self.game.players[0].cards[0], 50, HEIGHT - 170, index, False, False)
        if self.game.players[0].escobas:
            self.generate_sprite(self.game.players[0].escobas[-1], 150, HEIGHT - 170, index, False)

        # Player 2 Cards
        index = 0
        for card in self.game.players[1].hand:
            sprite = self.generate_sprite(card, 350 + (index * 100), 25, index, False, False)
            self.hand_sprites.add(sprite)
            index += 1

        if self.game.players[1].cards:
            self.generate_sprite(self.game.players[1].cards[0], 50, 25, index, False, False)
        if self.game.players[1].escobas:
            self.generate_sprite(self.game.players[1].escobas[-1], 150, 25, index, False)

        # Table Cards
        index = 0
        for card in self.game.table:
            if self.game.table.__len__() <= 5:
                posx = 250 + (index * 100)
                posy = (HEIGHT/2) - 75
            else:
                if index < 5:
                    posx = 250 + (index * 100)
                    posy = (HEIGHT / 2) - 150
                else:
                    posx = 250 + ((index-5) * 100)
                    posy = (HEIGHT / 2) + 15

            sprite = self.generate_sprite(card, posx, posy, index)
            self.table_sprites.add(sprite)
            index += 1

        # MESSAGES
        text, position = draw_text("ROUND %d" % self.game.round, WIDTH-100, HEIGHT/2)
        self.screen.blit(text, position)
        text, position = draw_text("%s" % self.game.players[1].name.upper(), WIDTH-100, 50)
        self.screen.blit(text, position)
        text, position = draw_text("Points: %d" % self.game.players[1].points, WIDTH-100, 80)
        self.screen.blit(text, position)
        text, position = draw_text("%s" % self.game.players[0].name.upper(), WIDTH-100, HEIGHT-100)
        self.screen.blit(text, position)
        text, position = draw_text("Points: %d" % self.game.players[0].points, WIDTH-100, HEIGHT-70)
        self.screen.blit(text, position)

        pygame.display.flip()

    def show_end_round(self):
        background_image = load_image('images/background.jpg')
        self.screen.blit(background_image, (0, 0))
        text, position = draw_text("Finished Round", (WIDTH / 2), (HEIGHT / 2))
        self.screen.blit(text, position)
        pygame.display.flip()
        pygame.time.wait(2000)

        for player in self.game.players:
            self.screen.blit(background_image, (0, 0))
            text, position = draw_text("%s scored %s points in this round" % (player.name, player.round_points),
                                       (WIDTH / 2), (HEIGHT / 2))
            self.screen.blit(text, position)
            pygame.display.flip()
            pygame.time.wait(2000)

    def __show_winner(self):
        background_image = load_image('images/background.jpg')
        self.screen.blit(background_image, (0, 0))
        text, position = draw_text("THE WINNER IS %s WITH %s POINTS" %
                                   (self.game.winner.name, self.game.winner.points), (WIDTH/2), HEIGHT / 2)
        self.screen.blit(text, position)
        text, position = draw_text("Press SPACE to restart game", (WIDTH/2), HEIGHT / 2 + 30)
        self.screen.blit(text, position)
        pygame.display.flip()
        while True:
            clock = pygame.time.Clock()
            clock.tick(30)
            keys = pygame.key.get_pressed()

            if keys[K_SPACE]:
                self.start()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

    def start(self):
        pygame.display.set_caption("PYEscoba")
        self.game = Game()
        self.game.add_human_pygame_player("Player1", self)
        self.game.add_cpu_pygame_player("CPU1", self)
        # self.game.add_cpu_pygame_player("CPU2", self)

        while not self.game.someone_win():
            self.game.round += 1
            self.game.generate_deck()
            self.game.mix_deck()
            self.game.give_cards_to_table()
            while 1:
                self.game.give_cards_to_players()
                for x in range(0, 3):
                    for player in self.game.players:
                        self.update_screen()
                        player.play()
                        self.update_screen()
                if not self.game.deck:
                    break
            self.game.update_points()
            self.show_end_round()
            self.game.clear_players()
        self.__show_winner()

if __name__ == '__main__':
    pygame.init()
    app = Application()
    app.start()
