import sys
import pygame
from pygame.locals import K_SPACE, QUIT
from entities.game import Game
from sprites.sprites import load_image, draw_text, CardSprite, EscobaSprite

WIDTH = 1024
HEIGHT = 720


class Application(object):

    def __init__(self):
        self.game = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background_image = load_image('images/background.jpg')
        self.cards_sprites = pygame.sprite.Group()
        self.hand_sprites = pygame.sprite.Group()
        self.table_sprites = pygame.sprite.Group()

    def __draw_card(self, sprite, allow_click=True):
        """
        generate a specific card with his properties and position
        :rtype: CardSprite
        """
        self.screen.blit(sprite.image, sprite.rect)
        if allow_click:
            self.cards_sprites.add(sprite)
        return sprite

    def draw_table_card(self, card, posx, posy, index):
        """
        :param card: card Object
        :param posx: position X
        :param posy: position Y
        :param index: card index
        :return:
        """
        sprite = CardSprite(card, posx, posy, index, True)
        sprite = self.__draw_card(sprite)
        self.table_sprites.add(sprite)

    def draw_player_card(self, card, posx, posy, index, show_card):
        """
        :param card: card Object
        :param posx: position X
        :param posy: position Y
        :param index: card index
        :param show_card: show value of card
        :rtype: CardSprite
        """
        sprite = CardSprite(card, posx, posy, index, show_card)
        sprite = self.__draw_card(sprite, show_card)
        self.hand_sprites.add(sprite)
        return sprite

    def draw_escoba_card(self, card, posx, posy, index):
        """
        :param card: card Object
        :param posx: position X
        :param posy: position Y
        :param index: card index
        :return:
        """
        sprite = EscobaSprite(card, posx, posy, index)
        self.__draw_card(sprite, False)

    def update_screen(self):
        """
        render cards and points for each player in the screen
        """
        self.screen.blit(self.background_image, (0, 0))

        self.cards_sprites.empty()
        self.hand_sprites.empty()
        self.table_sprites.empty()

        # Players Cards
        number_player = 0
        for player in self.game.players:
            number_player += 1
            if number_player == 1:
                height_card = HEIGHT - 170
                show_card = True
            else:
                height_card = 25
                show_card = False
            index = 0
            # HAND CARDS
            for card in player.hand:
                self.draw_player_card(card, 350 + (index * 100), height_card, index, show_card)
                index += 1
            # PICKED CARDS
            if player.escobas:
                self.draw_escoba_card(player.escobas[-1], 150, height_card, index)
            if player.cards:
                self.draw_player_card(player.cards[0], 50, height_card, index, False)

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

            self.draw_table_card(card, posx, posy, index)
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

    def __show_end_round(self):
        """
        show points for each player
        """
        self.screen.blit(self.background_image, (0, 0))
        text, position = draw_text("Finished Round", (WIDTH / 2), (HEIGHT / 2))
        self.screen.blit(text, position)
        pygame.display.flip()
        pygame.time.wait(2000)

        for player in self.game.players:
            self.screen.blit(self.background_image, (0, 0))
            text, position = draw_text("%s scored %s points" % (player.name, player.round_points),
                                       (WIDTH / 2), (HEIGHT / 2))
            self.screen.blit(text, position)
            pygame.display.flip()
            pygame.time.wait(2000)

    def __show_winner(self):
        """
        shows winner and his points on the screen
        """
        self.screen.blit(self.background_image, (0, 0))
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
        """
        start the game
        """
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
            self.__show_end_round()
            self.game.clear_players()
        self.__show_winner()


if __name__ == '__main__':
    pygame.init()
    APP = Application()
    APP.start()
