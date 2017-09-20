# coding=utf-8
import pygame

from cpu_player import CpuPlayer
from sprites.sprites import draw_text


class CpuPygamePlayer(CpuPlayer):

    def __init__(self, name, game, app_pygame):
        super(CpuPygamePlayer, self).__init__(name, game)
        self.app_pygame = app_pygame
        self.time_between_moves = 1000

    def play(self):
        """
        Cpu game implementation
        """
        moves = self._get_possible_moves()
        if not moves:
            throw_index_card = self._search_a_card_to_throw()
            for card_sprite in self.app_pygame.hand_sprites:
                if card_sprite.card == self.hand[throw_index_card]:
                    sprite = self.app_pygame.draw_player_card(card_sprite.card, card_sprite.rect.x, card_sprite.rect.y,
                                                              throw_index_card, True)
                    self.__display_selected_card(sprite, "THROW")
                    self.throw_card(throw_index_card)
                    break
        else:
            player_card, table_cards = self._get_best_move(moves)
            # SHOW HAND CARD TO USE
            for card_sprite in self.app_pygame.hand_sprites:
                if card_sprite.card == self.hand[player_card]:
                    sprite = self.app_pygame.draw_player_card(card_sprite.card, card_sprite.rect.x, card_sprite.rect.y,
                                                              player_card, True)
                    self.__display_selected_card(sprite, "USE")
                    break
            # SHOW TABLE CARDS TO PICK
            cards_to_pick = []
            for index in table_cards:
                cards_to_pick.append(self.game.table[index])

            for card_sprite in self.app_pygame.table_sprites:
                if card_sprite.card in cards_to_pick:
                    self.__display_selected_card(card_sprite, "SELECTED")

            self.make_a_move(player_card, table_cards)

    def __display_selected_card(self, sprite, text):
        text, position = draw_text(text, sprite.rect.centerx, sprite.rect.y - 10)
        self.app_pygame.screen.blit(text, position)
        pygame.display.update()
        pygame.time.wait(self.time_between_moves)
