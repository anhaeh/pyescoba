import pygame
from pygame.locals import *


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, number, card_type):
        image_numer = number
        if number > 7:
            image_numer = number+2
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/%s/%d.jpg" % (card_type, image_numer))
        self.rect = self.image.get_rect()
        #self.rect.centerx = 200
        #self.rect.centery = 200


def load_image(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image
