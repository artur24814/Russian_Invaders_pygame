import pygame
from gun import Gun

class Player(pygame.sprite.Sprite):
    def __init__(self,pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('graphics/player_with_patron.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 75))
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.gun_time = 0
        self.gun_cooldown = 600

        self.guns = pygame.sprite.Group()
        self.gun_sound = pygame.mixer.Sound('audio/Gunshot.mp3')
        self.gun_sound.set_volume(0.13)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_gun()
            self.ready = False
            self.gun_time = pygame.time.get_ticks()
            self.gun_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.gun_time >= self.gun_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_gun(self):
        self.guns.add(Gun(self.rect.center, -8, self.rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.guns.update()