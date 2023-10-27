import pygame
from settings import *

ELEMENT_SELECTED_EVENT = pygame.USEREVENT + 1


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
        self.menu = Menu(self.screen)
        self.selected_element = None

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
        self.menu.buttons_group.update()

    def events(self):
        # Editor Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < 1000:
                    x = mouse_pos[0] // PLATFORM_SIZE
                    y = mouse_pos[1] // PLATFORM_SIZE
                    self.add_to_map(x, y)
            if event.type == ELEMENT_SELECTED_EVENT:
                if self.selected_element:
                    self.selected_element.is_selected = False
                self.selected_element = event.message

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.menu.buttons_group.draw(self.screen)
        for button in self.menu.buttons_group:
            button.draw_border(self.screen)

        # Editor Loop - draw
        self.draw_grid()
        self.draw_map()

        pygame.display.flip()

    def draw_map(self):
        for row_number, row in enumerate(self.level_map):
            for col_number, col in enumerate(row):
                if col == 1 or col == 2:
                    self.screen.blit(self.menu.sprite_images[col],
                                     (col_number * PLATFORM_SIZE, row_number * PLATFORM_SIZE))

                elif col == -1:
                    self.screen.blit(self.menu.sprite_images[col], (col_number * PLATFORM_SIZE,
                                                                    row_number * PLATFORM_SIZE + PLATFORM_SIZE // 2))

                elif col == 3:
                    self.screen.blit(
                        self.menu.sprite_images[col],
                        (col_number * PLATFORM_SIZE + PLATFORM_SIZE // 4,
                         row_number * PLATFORM_SIZE + PLATFORM_SIZE // 4)
                    )

                elif col == 4 or col == 5:
                    self.screen.blit(
                        self.menu.sprite_images[col],
                        (col_number * PLATFORM_SIZE, row_number * PLATFORM_SIZE)
                    )

                elif col == 9:
                    self.screen.blit(
                        self.menu.sprite_images[col],
                        (col_number * PLATFORM_SIZE + PLATFORM_SIZE // 2, row_number * PLATFORM_SIZE)
                    )

    def draw_grid(self):
        for line in range(0, WIDTH // PLATFORM_SIZE):
            pygame.draw.line(self.screen, BLACK, (line * PLATFORM_SIZE, 0), (line * PLATFORM_SIZE, HEIGHT))
        for line in range(0, HEIGHT // PLATFORM_SIZE):
            pygame.draw.line(self.screen, BLACK, (0, line * PLATFORM_SIZE), (WIDTH, line * PLATFORM_SIZE))

    def create_map(self):
        self.level_map = []
        for i in range(12):
            self.level_map.append([0 for _ in range(20)])

    def add_to_map(self, x, y):
        if self.selected_element:
            self.level_map[y][x] = self.selected_element.value
        print(self.level_map)

    

class Button(pygame.sprite.Sprite):
    def __init__(self, image, value, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image: pygame.surface.Surface = image
        self.value = value
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.is_selected = False
        self.border_color = pygame.Color("white")

    def update(self, *args, **kwargs):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.is_selected:
            if pygame.mouse.get_pressed()[0]:
                self.on_pressed()
            else:
                self.border_color.update("cornsilk3")
        elif not self.is_selected:
            self.border_color.update("white")

    def draw_border(self, screen):
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
    def on_pressed(self):
        self.is_selected = True
        self.border_color.update(RED)
        pygame.event.post(pygame.event.Event(ELEMENT_SELECTED_EVENT, message=self))


class SaveButton(Button):
    def __init__(self):
        super().__init__(pygame.image.load("images/save.png"), None, [WIDTH + 5, 40])
        self.file_name = "map_level_{level}"


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons_group = pygame.sprite.Group()
        self.sprite_images = {1: pygame.transform.scale(pygame.image.load("images/grass.png"), (PLATFORM_SIZE,
                                                                                                PLATFORM_SIZE)),
                              2: pygame.transform.scale(pygame.image.load("images/dirt.png"), (PLATFORM_SIZE,
                                                                                               PLATFORM_SIZE)),
                              -1: pygame.transform.scale(pygame.image.load("images/lava.png"), (PLATFORM_SIZE,
                                                                                                PLATFORM_SIZE // 2)),
                              3: pygame.transform.scale(pygame.image.load("images/coin.png"), (30, 30)),
                              5: pygame.image.load("images/Enemy_6.png"),
                              4: pygame.image.load("images/Enemy_tuda_suda.png"),
                              9: pygame.transform.scale(pygame.image.load("images/fin.png"), (15, 50)),
                              0: pygame.transform.scale(pygame.image.load("images/stirka.jpg"), (PLATFORM_SIZE,
                                                                                                 PLATFORM_SIZE))}

        self.screen.fill((0, 120, 100))

        self.font = pygame.font.Font(None, 25)
        self.text = self.font.render("Menu", True, WHITE)
        self.screen.blit(self.text, (1002, 10))

        self.create_buttons()

    def create_buttons(self):
        counter = 0
        for key, value in self.sprite_images.items():
            self.buttons_group.add(Button(pygame.transform.scale(value, (40, 40)), key,
                                          [WIDTH + 5, 85 + counter * 60]))
            counter += 1
        self.buttons_group.add(SaveButton())


editor = Editor()
while editor.running:
    editor.new()

pygame.quit()
