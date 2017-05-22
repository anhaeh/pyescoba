# coding=utf-8


class Card(object):

    CARD_TYPES = ["ORO", "BASTO", "ESPADA", "COPA"]

    def __init__(self, number, card_type):
        self.number = number
        self.card_type = card_type

    def __repr__(self):
        return "%s %s" % (self.number, self.card_type)
