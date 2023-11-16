import pygame
import random
from enemy import Enemy


class Enemy3(Enemy):
    def __init__(self, score):
        super().__init__(score, speed=11)
        self.image = pygame.image.load("autko1.png")

    def move(self):
        self.rect.move_ip(0, self.speed/2)
        self.rect.move_ip(1, 0)
        self.rect.move_ip(0, self.speed/2)
        if self.rect.top > 600:
            self.speed += 0.05
            self.score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)
