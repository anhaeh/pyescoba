import pygame
from pygame.locals import RLEACCEL


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card, posx, posy, index, show_card):
        self.image_number = card.number
        if card.number > 7:
            self.image_number = card.number + 2
        pygame.sprite.Sprite.__init__(self)

        self.rect = None
        self.image = None
        self.card = card
        self.index = index
        self.set_image(posx, posy, show_card)

    def set_image(self, posx, posy, show_card):
        if show_card:
            image = load_image("images/%s/%d.jpg" % (self.card.card_type, self.image_number))
        else:
            image = load_image("images/back.jpg")
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy


class EscobaSprite(CardSprite):
    def __init__(self, card, posx, posy, index):
        super(EscobaSprite, self).__init__(card, posx, posy, index, True)

    def set_image(self, posx, posy, show=True):
        self.image = load_image("images/%s/%d.jpg" % (self.card.card_type, self.image_number))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = posx - 50
        self.rect.y = posy + 20


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
