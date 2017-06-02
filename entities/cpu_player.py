# coding=utf-8
from player import Player


class CpuPlayer(Player):

    def __init__(self, name, game):
        Player.__init__(self, name, game)
        # List of values ​​associated with each card for decision making
        self.card_values = {
            "1ORO": 1,
            "2ORO": 1,
            "3ORO": 1,
            "4ORO": 1,
            "5ORO": 1,
            "6ORO": 1,
            "8ORO": 1,
            "9ORO": 1,
            "10ORO": 1,
            "7BASTO": 3,
            "7COPA": 3,
            "7ESPADA": 3,
            "7ORO": 7
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
        table_cards = sorted(self.game.table, key=lambda x: x.number)
        for hand_card in self.hand:
            for x in range(0, len(table_cards)):
                total = hand_card.number
                actual_cards = [hand_card]
                for table_card in table_cards:
                    if total + table_card.number <= 15:
                        total += table_card.number
                        actual_cards.append(table_card)
                        if total == 15:
                            actual_cards.sort(key=lambda x: x.number)
                            if actual_cards not in moves:
                                moves.append(actual_cards)
                                break
                table_cards.append(table_cards.pop(0))
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

            # IF ESCOBA
            if rest_cards_on_table.__len__() == 0:
                points_of_move += 20

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

        # get indices of cards
        index = 0
        for card in self.hand:
            if card in best_move_hand_card:
                hand_card = index
                break
            index += 1
        index = 0
        table_cards = []
        for card in self.game.table:
            if card in best_move_table_cards:
                table_cards.append(index)
            index += 1

        return hand_card, table_cards

    @staticmethod
    def _calculate_points_of_rest(rest_cards_on_table):
        """
        Calculates the value of the play by evaluating the rest to be left on the table
        """
        rest_points = sum([x.number for x in rest_cards_on_table])
        if rest_points < 5:
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
