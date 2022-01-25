# coding=utf-8

# constants
GOLD = "ORO"
SWORD = "ESPADA"
CUP = "COPA"
STICK = "BASTO"


class Card(object):

    CARD_TYPES = [GOLD, SWORD, CUP, STICK]

    def __init__(self, number, card_type):
        self.number = number
        self.card_type = card_type

    def __repr__(self):
        return "%s %s" % (self.number, self.card_type)
