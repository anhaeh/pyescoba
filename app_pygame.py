import pygame
from entities.game import Game
from sprites.sprites import load_image, draw_text, CardSprite

WIDTH = 1024
HEIGHT = 720


class Application(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        self.cards_sprites = pygame.sprite.Group()
        self.hand_sprites = pygame.sprite.Group()

    def __generate_sprite(self, card, posx, posy, index, allow_click=True):
        sprite = CardSprite(card, posx, posy, index)
        self.screen.blit(sprite.image, sprite.rect)
        if allow_click:
            self.cards_sprites.add(sprite)
        return sprite

    def update_screen(self):
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
                posy = (HEIGHT/2) - 75
            else:
                if index < 5:
                    posx = 250 + (index * 100)
                    posy = (HEIGHT / 2) - 150
                else:
                    posx = 250 + ((index-5) * 100)
                    posy = (HEIGHT / 2) + 15

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

        self.game.add_human_pygame_player("Player1", self)
        # self.game.add_cpu_player("CPU2")
        self.game.add_cpu_player("CPU1")

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
            pygame.time.wait(1000)
            self.game.clear_players()
        self.update_screen()
        pygame.time.wait(5000)


if __name__ == '__main__':
    pygame.init()
    app = Application()
    app.start()
