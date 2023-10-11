import pygame
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load("images/ba.png")
        self.platform_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.create_map()
        self.player: Player = Player(self.platform_group)
        self.player_group = pygame.sprite.GroupSingle()
        self.coin_sound = pygame.mixer.Sound("sounds/coin.wav")
        pygame.mixer.music.load("sounds/background_sound.mp3")
        self.score = 0
        self.font = pygame.font.Font(None, 20)


    def new(self):
        # start a new game
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.player_group.add(self.player)
        self.run()

    def run(self):
        # Game Loop
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.player_group.update()
        self.enemy_group.update()

    def events(self):
        self.collision()
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # Game Loop - draw
        self.platform_group.draw(self.screen)
        # self.draw_grid()

        text = self.font.render(f"SCORE: {self.score}", True, BLACK)
        self.screen.blit(text, (0, 0))

        self.player_group.draw(self.screen)
        self.lava_group.draw(self.screen)
        self.coin_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        pygame.display.flip()


    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

    def draw_grid(self):
        for line in range(0, WIDTH // PLATFORM_SIZE):
            pygame.draw.line(self.screen, BLACK, (line * PLATFORM_SIZE, 0), (line * PLATFORM_SIZE, HEIGHT))
        for line in range(0, HEIGHT // PLATFORM_SIZE):
            pygame.draw.line(self.screen, BLACK, (0, line * PLATFORM_SIZE), (WIDTH, line * PLATFORM_SIZE))

    def create_map(self):
        for row_number, row in enumerate(map_list):
            for col_number, col in enumerate(row):
                if col == 1 or col == 2:
                    new_platform = Platform(col_number * PLATFORM_SIZE, row_number * PLATFORM_SIZE, col)
                    self.platform_group.add(new_platform)
                elif col == -1:
                    new_lava = Lava(col_number * PLATFORM_SIZE, row_number * PLATFORM_SIZE + PLATFORM_SIZE // 2)
                    self.lava_group.add(new_lava)
                elif col == 3:
                    new_coin = Coin(col_number * PLATFORM_SIZE + PLATFORM_SIZE // 4, row_number * PLATFORM_SIZE + PLATFORM_SIZE // 4)
                    self.coin_group.add(new_coin)
                elif col == 4 or col == 5:
                    new_enemy = Enemy(col_number * PLATFORM_SIZE, row_number * PLATFORM_SIZE, col == 4)
                    self.enemy_group.add(new_enemy)

    def collision(self):
        # collision = pygame.sprite.spritecollide(self.player, self.platform_group, False)
        # for sprite in collision:
        #     if self.player.velocity_y < 0:
        #         self.player.velocity_y = 0
        #         self.player.rect.top = sprite.rect.bottom
        #     elif self.player.velocity_y > 0:
        #         self.player.rect.bottom = sprite.rect.top
        #         self.player.on_ground = True
        #         self.player.velocity_y = 0
#            if self.player.direction_x > 0 and
        if pygame.sprite.spritecollideany(self.player, self.lava_group):
            self.player.kill()
        if pygame.sprite.spritecollideany(self.player, self.enemy_group):
            self.player.game_over()
        if pygame.sprite.spritecollide(self.player, self.coin_group, dokill=True):
            self.coin_sound.play()
            self.score += 1


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
