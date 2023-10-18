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
        self.platform_group = None
        self.lava_group = None
        self.coin_group = None
        self.enemy_group = None
        self.player = None
        self.player_group = None
        self.f_point_group = None
        self.coin_sound = pygame.mixer.Sound("sounds/coin.wav")
        pygame.mixer.music.load("sounds/background_sound.mp3")
        self.score = 0
        self.font = pygame.font.Font(None, 20)

        self.finish = None

    def new(self):
        # start a new game
        self.platform_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.f_point_group = pygame.sprite.GroupSingle()
        self.create_map()
        self.player: Player = Player(self.platform_group)
        self.player_group = pygame.sprite.GroupSingle()
        self.score = 0

        pygame.mixer.music.play(-1, 0.0, 5000)
        self.player_group.add(self.player)
        self.run()

    def run(self):
        # Editor Loop
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Editor Loop - Update
        self.player_group.update()
        self.enemy_group.update()

    def events(self):
        self.collision()
        # Editor Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == GAME_OVER_EVENT:
                self.show_go_screen()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # Editor Loop - draw
        self.platform_group.draw(self.screen)
        # self.draw_grid()

        text = self.font.render(f"SCORE: {self.score}", True, BLACK)
        self.screen.blit(text, (0, 0))

        self.player_group.draw(self.screen)
        self.lava_group.draw(self.screen)
        self.coin_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.f_point_group.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BLACK)
        pygame.display.flip()

        # if self.wait_for_key():
        #     self.new()
        image = pygame.image.load("images/finish_screen.png")

        button_rect = pygame.rect.Rect((315, 340), (315, 100))
        #        pygame.draw.rect(self.screen, BLACK, button_rect)

        self.screen.blit(image, (0, 0))

        pygame.display.flip()

        if self.wait_for_key(button_rect):
            self.new()

    def show_win_screen(self):
        image = pygame.image.load("images/win.png")

        button_rect = pygame.rect.Rect((380, 413), (257, 43))
#        pygame.draw.rect(self.screen, BLACK, button_rect)

        font = pygame.font.Font(None, 50)
        text = font.render(str(self.score), True, YELLOW)
        image.blit(text, (290, 235))

        self.screen.blit(image, (275, 100))

        pygame.display.flip()

        if self.wait_for_key(button_rect):
            self.new()

    def wait_for_key(self, button):
        a = True
        while a:
            mouse_pos = pygame.mouse.get_pos()
            if button.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    return True
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return True
                if event.type == pygame.QUIT:
                    a = False
                    self.running = False

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

                elif col == 9:
                    f_point = FinishPoint(col_number * PLATFORM_SIZE + PLATFORM_SIZE // 2, row_number * PLATFORM_SIZE)
                    self.f_point_group.add(f_point)

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
            self.player.game_over()

        if pygame.sprite.spritecollideany(self.player, self.enemy_group):
            self.player.game_over()

        if pygame.sprite.spritecollideany(self.player, self.f_point_group):
            self.show_win_screen()

        if pygame.sprite.spritecollide(self.player, self.coin_group, dokill=True):
            self.coin_sound.play()
            self.score += 1


g = Game()
g.show_start_screen()
while g.running:
    g.new()

pygame.quit()
