import pygame
from settings import *
from sprites import *


class Game:
    def __init__(self, player):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.player = player
        self.all_sprites = pygame.sprite.Group()
        self.running = True
        self.background = pygame.image.load("images/background.png")

    def new(self):
        # start a new game
        self.all_sprites.add(self.player)
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
        self.all_sprites.update()

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # Game Loop - draw

        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


player = Player()
g = Game(player)
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
