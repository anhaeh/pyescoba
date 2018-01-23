# coding=utf-8
"""
Implementation for a human player
"""

from player import Player


class HumanPlayer(Player):

    def __init__(self, name, game):
        super(HumanPlayer, self).__init__(name, game)

    def play(self):
        """
        Human player implementation
        """
        while 1:
            try:
                print "My Hand"
                for card in self.hand:
                    print card

                player_card = int(raw_input("Pick a card of your hand[0-2](99 to throw): "))
                if player_card == 99:
                    my_card = int(raw_input("which throw[0-2]: "))
                    self.throw_card(my_card)
                    break

                table_cards = raw_input("Pick cards of table[ex: 0,1,2]: ")
                table_cards = table_cards.split(",")
                result = self.make_a_move(player_card, table_cards)
                if result:
                    break
                print "Not sum 15"
            except Exception, e:
                print str(e)
