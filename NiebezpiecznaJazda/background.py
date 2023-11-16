import pygame


class Background:
    def __init__(self):
        self.bgimage = pygame.image.load('droga2.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY = 0
        self.moving_speed = 5

    def update(self):
        self.bgY += self.moving_speed
        if self.bgY >= self.rectBGimg.height:
            self.bgY = 0

    def render(self, surface):
        surface.blit(self.bgimage, (0, self.bgY))
        surface.blit(self.bgimage, (0, self.bgY - self.rectBGimg.height))
