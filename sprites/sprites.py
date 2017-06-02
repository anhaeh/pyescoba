import pygame
from pygame.locals import *


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card, posx, posy, index, show, is_escoba):
        image_number = card.number
        if card.number > 7:
            image_number = card.number+2
        pygame.sprite.Sprite.__init__(self)
        if show:
            self.image = load_image("images/%s/%d.jpg" % (card.card_type, image_number))
            if is_escoba:
                self.image = pygame.transform.rotate(self.image, 90)
                posx = posx - 50
                posy = posy + 20
        else:
            self.image = load_image("images/back.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.card = card
        self.index = index


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


def draw_text(message, posx, posy, color=(255, 255, 255)):
    font = pygame.font.Font("fonts/DroidSans.ttf", 20)
    out = pygame.font.Font.render(font, message, 1, color)
    out_rect = out.get_rect()
    out_rect.centerx = posx
    out_rect.centery = posy
    return out, out_rect
