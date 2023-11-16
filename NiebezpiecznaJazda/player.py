import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("autko2.png")
        self.rect = self.image.get_rect()  # tworzy prostokąt o wymiarach obrazku
        self.rect.center = (160, 480)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:  # nieumożliwienie ucieczki z ekranu
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < 400:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
