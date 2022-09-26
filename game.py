import pygame, sys
from player import Player
import obstacle
from rushists import Rashist,Putin
import random
from gun import Gun

class Game:
    def __init__(self):
        #Player setup
        player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #healt and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('graphics/player_with_patron.png').convert_alpha()
        self.live_surf = pygame.transform.scale(self.live_surf, (35, 45))
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('font/Pixeltype.ttf',40)

        #Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_position = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_position, x_start=screen_width / 15,y_start=580)

        #Rashist setup
        self.rashists = pygame.sprite.Group()
        self.rashist_setup(rows=5, cols=10)
        self.rashists_direction = 1
        self.rashist_guns = pygame.sprite.Group()

        #extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = random.randint(40,80)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,  x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def rashist_setup(self, rows, cols,x_distance = 60, y_distance = 88, x_offset=70, y_offset=70):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: rushist_sprite = Rashist('general', x, y)
                elif 1 <= row_index <= 2: rushist_sprite = Rashist('drunk', x, y)
                else: rushist_sprite = Rashist('red', x, y)
                self.rashists.add(rushist_sprite)

    def rashists_position_checker(self):
        all_rashists = self.rashists.sprites()
        for rashist in all_rashists:
            if rashist.rect.right >= screen_width:
                self.rashists_direction = -1
                self.rashists_move_down(2)
            if rashist.rect.left <= 0:
                self.rashists_direction = 1
                self.rashists_move_down(2)

    def rashists_move_down(self, distance):
        if self.rashists:
            for rashist in self.rashists.sprites():
                rashist.rect.y += distance

    def rashists_shot(self):
        if self.rashists.sprites():
            random_rashist = random.choice(self.rashists.sprites())
            gun_sprite = Gun(random_rashist.rect.center,6,screen_height)
            self.rashist_guns.add(gun_sprite)

    def extra_rashist_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Putin(random.choice(['right','left']),screen_width))
            self.extra_spawn_time = random.randint(400, 800)

    def collision_checks(self):
        # player gun
        if self.player.sprite.guns:
            for gun in self.player.sprite.guns:
                #obstacle collision
                if pygame.sprite.spritecollide(gun, self.blocks, True):
                    gun.kill()
                #rashists collisions
                rashists_hit = pygame.sprite.spritecollide(gun, self.rashists,True)
                if rashists_hit:
                    for rashist in rashists_hit:
                        self.score += rashist.value
                    gun.kill()

                #extra collisions
                if pygame.sprite.spritecollide(gun, self.extra, True):
                    self.score += 500
                    gun.kill()

        #rushists gun
        if self.rashist_guns:
            for gun in self.rashist_guns:
                # obstacle collision
                if pygame.sprite.spritecollide(gun, self.blocks, True):
                    gun.kill()

                # obstacle collision
                if pygame.sprite.spritecollide(gun, self.player, False):
                    gun.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        #rushists
        if self.rashists:
            for rushist in self.rashists:
                # obstacle collision
                pygame.sprite.spritecollide(rushist, self.blocks, True)

                if pygame.sprite.spritecollide(rushist, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * self.live_surf.get_size()[0] + 10)
            screen.blit(self.live_surf, (x,8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft=(10,10))
        screen.blit(score_surf,score_rect)


    def run(self):
        self.player.sprite.guns.draw(screen)
        self.player.update()
        self.rashists.update(self.rashists_direction)
        self.rashists_position_checker()
        self.rashist_guns.update()
        self.extra.update()
        self.extra_rashist_timer()
        self.collision_checks()

        self.player.draw(screen)
        self.blocks.draw(screen)
        self.rashists.draw(screen)
        self.rashist_guns.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()



if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    bg_img = pygame.image.load('graphics/bg_game.jpg')
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    RUSHISTGUN = pygame.USEREVENT + 1
    pygame.time.set_timer(RUSHISTGUN,800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == RUSHISTGUN:
                game.rashists_shot()

        screen.blit(bg_img, (0,0))
        game.run()

        pygame.display.flip()
        clock.tick(60)
