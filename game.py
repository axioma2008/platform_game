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
        self.create_map()
        self.player: Player = Player(self.platform_group)
        self.player_group = pygame.sprite.GroupSingle()


    def new(self):
        # start a new game
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

    def events(self):
#        self.vertical_collision()
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # Game Loop - draw
        self.platform_group.draw(self.screen)
#        self.draw_grid()
        self.player_group.draw(self.screen)
        self.lava_group.draw(self.screen)
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

    def vertical_collision(self):
        collision = pygame.sprite.spritecollide(self.player, self.platform_group, False)
        for sprite in collision:
            if self.player.gravity < 0:
                self.player.gravity = 0
                self.player.rect.top = sprite.rect.bottom
            elif self.player.gravity > 0:
                self.player.rect.bottom = sprite.rect.top
                self.player.on_ground = True
                self.player.gravity = 0
#            if self.player.direction_x > 0 and


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
