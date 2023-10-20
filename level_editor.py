import pygame
from settings import *


class Editor:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH + PLATFORM_SIZE, HEIGHT))
        pygame.display.set_caption("level editor")
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load("images/ba.png")
        pygame.mixer.music.load("sounds/background_sound.mp3")
        self.font = pygame.font.Font(None, 20)
        self.level_map = None
        self.sprite_images = {"grass": pygame.image.load("images/grass.png"),
                              "dirt": pygame.image.load("images/dirt.png"),
                              "lava": pygame.image.load("images/lava.png"),
                              "coin": pygame.image.load("images/coin.png"),
                              "blob": pygame.image.load("images/blob.png"),
                              "finish_point": pygame.image.load("images/fin.png")}

    def new(self):
        # start a new game
        self.create_map()

#        pygame.mixer.music.play(-1, 0.0, 5000)

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
        pass

    def events(self):
        # Editor Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x = mouse_pos[0] // PLATFORM_SIZE
                y = mouse_pos[1] // PLATFORM_SIZE
                print(x, y)


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # Editor Loop - draw
        self.draw_grid()
        pygame.display.flip()

    def draw_grid(self):
        for line in range(0, WIDTH // PLATFORM_SIZE):
            pygame.draw.line(self.screen, BLACK, (line * PLATFORM_SIZE, 0), (line * PLATFORM_SIZE, HEIGHT))
        for line in range(0, HEIGHT // PLATFORM_SIZE):
            pygame.draw.line(self.screen, BLACK, (0, line * PLATFORM_SIZE), (WIDTH, line * PLATFORM_SIZE))

    def create_map(self):
        self.level_map = []
        for i in range(12):
            self.level_map.append([0 for _ in range(20)])


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.is_selected = False


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons_group = pygame.sprite.Group()
        self.sprite_images = {"grass": pygame.image.load("images/grass.png"),
                              "dirt": pygame.image.load("images/dirt.png"),
                              "lava": pygame.image.load("images/lava.png"),
                              "coin": pygame.image.load("images/coin.png"),
                              "blob": pygame.image.load("images/blob.png"),
                              "finish_point": pygame.image.load("images/fin.png")}
    def create_buttons(self):
        counter = 0
        for key, value in self.sprite_images.items():
            self.buttons_group.add(Button(pygame.transform.scale(value, (40, 40)),
                                          [WIDTH + 5, 20 + counter * 40 + 5]))
            counter += 1



editor = Editor()
while editor.running:
    editor.new()

pygame.quit()
