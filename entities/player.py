# coding=utf-8
from entities.exceptions import ImplementationError


class Player(object):

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.hand = []
        self.cards = []
        self.escobas = []
        self.points = 0
        self.round_points = 0

    def __repr__(self):
        return self.name

    def clear(self):
        """
        Clear all variables after the end of the round
        """
        self.hand = []
        self.cards = []
        self.escobas = []
        self.points += self.round_points
        self.round_points = 0

    def throw_card(self, id_card):
        """
        Throw a card from your hand to the table 
        """
        self.game.table.append(self.hand.pop(id_card))

    def add_card_to_hand(self, card):
        """
        Add a card to the player's hand
        """
        self.hand.append(card)

    def play(self):
        raise ImplementationError('play', self.__class__)

    def make_a_move(self, player_card, table_cards):
        """
        Makes a play using a selected card from a hand and others from the table
        """
        table_cards.sort()
        cards = [self.hand[player_card]]
        for index in table_cards:
            cards.append(self.game.table[int(index)])

        total = 0
        for card in cards:
            total += card.number

        if total == 15:
            id_adjust = 0
            for index in table_cards:
                self.cards.append(self.game.table.pop(int(index) - id_adjust))
                id_adjust += 1
            # if is escoba
            if not self.game.table:
                print "ESCOBA!"
                self.escobas.append(self.hand.pop(player_card))
            else:
                self.cards.append(self.hand.pop(player_card))
            self.game.last_play = self
            return True
        return False
