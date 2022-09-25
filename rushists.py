import pygame

class Rashist(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = 'graphics/rashist_' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 65))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, direction):
        self.rect.x +=direction

class Putin(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('graphics/rashist_putin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 65))
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft=(x, 20))

    def update(self):
        self.rect.x += self.speed