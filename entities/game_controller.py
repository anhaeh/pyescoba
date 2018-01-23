# coding=utf-8
"""
This class manage all the game and its players
"""

from random import shuffle
from entities.card import Card
from entities.cpu_player import CpuPlayer
from entities.human_player import HumanPlayer


class GameController(object):

    def __init__(self):
        self.deck = []
        self.table = []
        self.players = []
        self.round = 0
        self.last_play = None
        self.winner = None

    def add_human_player(self, name):
        player = HumanPlayer(name, self)
        self._add_player(player)

    def add_cpu_player(self, name):
        player = CpuPlayer(name, self)
        self._add_player(player)

    def _add_player(self, player):
        """
        Add a player to the game
        """
        self.players.append(player)

    def begin_game(self):
        while not self.someone_win():
            self.start_round()
        print "FINISH in %d rounds" % self.round
        print "The winner is %s with %s points" % (self.winner.name, self.winner.points)

    def generate_deck(self):
        """
        Generates the deck of 40 cards
        """
        for card_type in Card.CARD_TYPES:
            for i in range(1, 11):
                card = Card(i, card_type)
                self.deck.append(card)

    def someone_win(self):
        """
        Find if there is a winner in the game
        """
        winner = None
        for player in self.players:
            if player.points >= 15:
                if winner is None or (winner and player.points > winner.points):
                    winner = player
                elif winner and player.points == winner.points:
                    winner = None
        if winner:
            self.winner = winner
            return True
        return False

    def start_round(self):
        """
        Start a new game. Generate the deck, deal cards and players play their moves
        """
        self.round += 1
        print "--- ROUND", self.round, "---"
        self.generate_deck()
        self.mix_deck()
        self.give_cards_to_table()
        while 1:
            self.give_cards_to_players()
            for x in range(0, 3):
                for player in self.players:
                    print "TABLE"
                    for card in self.table:
                        print card
                    player.play()
            if not self.deck:
                break
        self.update_points()
        self.clear_players()

    def mix_deck(self):
        """
        Shuffle the generated deck of cards
        """
        shuffle(self.deck)

    def give_cards_to_players(self):
        """
        Deal 3 cards to each player
        """
        for player in self.players:
            for x in range(0, 3):
                player.add_card_to_hand(self.deck.pop(0))

    def give_cards_to_table(self):
        """
        Deal 4 cards to the table at the beginning of the game
        """
        for x in range(0, 4):
            self.table.append(self.deck.pop(0))

    def update_points(self):
        """
        Count the cards of each player and update the points of each
        """
        for player in self.players:
            # the last player take all
            if self.last_play.name == player.name and self.table:
                player.cards.extend(self.table)
            count_seven = 0
            count_gold = 0
            have_gold_seven = False
            for card in player.cards:
                if card.number == 7:
                    count_seven += 1
                    if card.card_type == Card.GOLD:
                        have_gold_seven = True
                if card.card_type == Card.GOLD:
                    count_gold += 1
            if have_gold_seven:
                player.round_points += 1
            if count_seven > 2:
                player.round_points += 1
            if count_gold > 5:
                player.round_points += 1
            if len(player.cards) > 20:
                player.round_points += 1

            player.round_points += len(player.escobas)
            print "* %s scored %d points" % (player.name, player.round_points)
            print "** %s has %d total points" % (player.name, player.points + player.round_points)

    def clear_players(self):
        """
        Clear player variables at the end of the round
        """
        self.table = []
        for player in self.players:
            player.clear()
