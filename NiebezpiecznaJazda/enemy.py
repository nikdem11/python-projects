import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, score, speed):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)
        self.score = score
        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > 600:
            self.speed += 0.05
            self.score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
