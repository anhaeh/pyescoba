# coding=utf-8
"""
Implementation for a IA player. It use a list of values associated with each card for decision making
"""
from copy import copy
from itertools import combinations
from player import Player
from entities.card import CUP, GOLD, SWORD, STICK


class CpuPlayer(Player):

    def __init__(self, name, game):
        super(CpuPlayer, self).__init__(name, game)
        self.card_values = {
            "1%s" % GOLD: 1,
            "2%s" % GOLD: 1,
            "3%s" % GOLD: 1,
            "4%s" % GOLD: 1,
            "5%s" % GOLD: 1,
            "6%s" % GOLD: 1,
            "8%s" % GOLD: 1,
            "9%s" % GOLD: 1,
            "10%s" % GOLD: 1,
            "7%s" % STICK: 3,
            "7%s" % CUP: 3,
            "7%s" % SWORD: 3,
            "7%s" % GOLD: 7
        }

    def play(self):
        """
        Cpu game implementation
        """
        moves = self._get_possible_moves()
        if not moves:
            throw_index_card = self._search_a_card_to_throw()
            self.throw_card(throw_index_card)
        else:
            player_card, table_cards = self._get_best_move(moves)
            self.make_a_move(player_card, table_cards)

    def _get_possible_moves(self):
        """
        Evaluate all possible games to run
        """
        moves = []
        table_cards = copy(self.game.table)
        combinations_in_table = []
        for comb_length in range(len(table_cards)):
            combinations_in_table += list(combinations(table_cards, comb_length + 1))

        for hand_card in self.hand:
            # make combinations by card
            for combination in iter(combinations_in_table):
                possible_move = list(combination)
                possible_move.append(hand_card)
                sum_cards = sum([x.number for x in possible_move])
                if sum_cards == 15:
                    moves.append(possible_move)
        return moves

    def _get_best_move(self, moves):
        """
        Select the best play to play using the value of the cards, and the remaining cards on the table
        """
        best_move = 0
        best_move_hand_card = None
        best_move_table_cards = None

        for move in moves:
            rest_cards_on_table = filter(lambda x: x not in move, self.game.table)
            points_of_move = self._calculate_points_of_rest(rest_cards_on_table)

            for card in move:
                key = "%d%s" % (card.number, card.card_type)
                points_of_move += 1
                if self.card_values.get(key):
                    points_of_move += self.card_values[key]
            if points_of_move > best_move:
                best_move = points_of_move
                best_move_hand_card = filter(lambda x: x not in self.game.table, move)
                best_move_table_cards = filter(lambda x: x not in best_move_hand_card, move)

        print "CPU use:", best_move_hand_card.__str__()
        print "And Get:", best_move_table_cards.__str__()

        # get indexes of cards
        hand_card_index = self.hand.index(best_move_hand_card[0])
        table_cards_indexes = []
        for card in iter(best_move_table_cards):
            table_cards_indexes.append(self.game.table.index(card))
        return hand_card_index, table_cards_indexes

    @staticmethod
    def _calculate_points_of_rest(rest_cards_on_table):
        """
        Calculates the value of the play by evaluating the rest to be left on the table
        """
        rest_points = sum([x.number for x in rest_cards_on_table])

        if rest_points == 0:  # is escoba
            points_of_move = 20
        elif rest_points < 5:
            points_of_move = 2
        elif rest_points > 14:
            points_of_move = 1
        else:
            points_of_move = 0
        return points_of_move

    def _search_a_card_to_throw(self):
        """
        Find the best card to throw
        """
        table_cards = self.game.table[:]
        best_index_card = None
        best_points = -100
        actual_card = 0
        for card in self.hand:
            points_of_move = self._calculate_points_of_rest(table_cards + [card])
            key = "%d%s" % (card.number, card.card_type)
            if self.card_values.get(key):
                points_of_move -= self.card_values[key]

            if points_of_move > best_points:
                best_points = points_of_move
                best_index_card = actual_card
            actual_card += 1
        print "CPU throw:", self.hand[best_index_card]
        return best_index_card
