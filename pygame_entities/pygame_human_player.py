# coding=utf-8
"""
Implementation for a human player using the pygame framework
"""

import sys
import pygame
from pygame.locals import *
from pygame_entities.sprites import draw_text
from entities.player import Player


class PygameHumanPlayer(Player):

    def __init__(self, name, game):
        super(PygameHumanPlayer, self).__init__(name, game)
        self.app_pygame = game.app_pygame

    def play(self):
        """
        Human player implementation for pygame engine
        """
        selected_hand_card = None
        selected_table_cards = []
        need_reload = False
        while True:
            clock = pygame.time.Clock()
            clock.tick(30)
            pygame.key.get_pressed()

            if need_reload:
                self.app_pygame.update_screen()
                need_reload = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left Click
                    for sprite in self.app_pygame.cards_sprites:
                        if sprite.rect.collidepoint(event.pos):
                            if sprite == selected_hand_card or \
                                    (selected_hand_card is not None and sprite.index in selected_table_cards) \
                                    or (selected_hand_card is not None and sprite in self.app_pygame.hand_sprites):
                                need_reload = True
                                selected_table_cards = []
                                selected_hand_card = None
                            else:
                                if sprite in self.app_pygame.hand_sprites:
                                    selected_hand_card = sprite.index
                                else:
                                    selected_table_cards.append(sprite.index)
                                text, position = draw_text("SELECTED", sprite.rect.centerx, sprite.rect.y - 10)
                                self.app_pygame.screen.blit(text, position)

                                if selected_hand_card is not None and selected_table_cards != []:
                                    result = self.make_a_move(selected_hand_card, selected_table_cards)
                                    if result:
                                        return
                                pygame.display.update()
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:  # Right Click
                    for sprite in self.app_pygame.cards_sprites:
                        if sprite.rect.collidepoint(event.pos) and sprite in self.app_pygame.hand_sprites:
                            self.throw_card(sprite.index)
                            return
