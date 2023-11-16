import pygame
from enemy import Enemy


class Enemy1(Enemy):
    def __init__(self, score):
        super().__init__(score, speed=10)
        self.image = pygame.image.load("autko1.png")
