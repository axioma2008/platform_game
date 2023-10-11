import pygame
from settings import *
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, platform_group):
        pygame.sprite.Sprite.__init__(self)
        self.platform_group = platform_group
        self.velocity_y = 0
        self.on_ground = True
        self.direction_x = 0
        self.direction_y = 0
        self.right_images = []
        self.left_images = []
        self.index = 0
        self.counter = 0
        self.gravity = 1
        self.is_killed = False

        for i in range(3, 7):
            image = pygame.image.load(f"images/cat_animation{i}.png")
            image = pygame.transform.scale(image, (PLATFORM_SIZE, PLATFORM_SIZE))
            self.right_images.append(image)
            self.left_images.append(pygame.transform.flip(image, True, False))

        self.standing_images = [
            pygame.transform.scale(pygame.image.load("images/cat_animation7.png"), (PLATFORM_SIZE, PLATFORM_SIZE))]
        self.standing_images.append(pygame.transform.flip(self.standing_images[0], True, False))

        self.image = self.standing_images[0]
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - PLATFORM_SIZE

        self.jump_image = [
            pygame.transform.scale(pygame.image.load("images/cat_animation8.png"), (PLATFORM_SIZE, PLATFORM_SIZE))]
        self.jump_image.append(pygame.transform.flip(self.jump_image[0], True, False))

    def update(self):

        if self.is_killed:
            if self.counter < 90:
                self.rect.y -= 1
                self.counter += 1
            return

        do_animation = False
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            dx -= 3.5
            self.direction_x = -1
            do_animation = True
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            dx += 3.5
            self.direction_x = 1
            do_animation = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -17
            self.on_ground = False
            if self.direction_x == 1:
                self.image = self.jump_image[0]
            elif self.direction_x == -1:
                self.image = self.jump_image[1]

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and self.on_ground:
            if self.direction_x == 1:
                self.image = self.standing_images[0]
            elif self.direction_x == -1:
                self.image = self.standing_images[1]

        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y

        dx, dy = self.check_collision(dx, dy)

        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            dy = 0
            self.on_ground = True
        if do_animation and self.on_ground:
            self.animate()
            self.counter += 1
        else:
            self.index = 0
            self.counter = 0

    def check_collision(self, dx, dy):
        for platform in self.platform_group:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.velocity_y < 0:
                    self.velocity_y = 0
                    dy = platform.rect.bottom - self.rect.top
                elif self.velocity_y >= 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.on_ground = True
                    self.velocity_y = 0
        return dx, dy

    def animate(self):

        if self.counter == 5:
            if self.index >= len(self.right_images):
                self.index = 0
            if self.direction_x == 1:
                self.image = self.right_images[self.index]
            if self.direction_x == -1:
                self.image = self.left_images[self.index]
            self.index += 1
            self.counter = 0

    def game_over(self):
        self.image = pygame.image.load("images/cat_ghost.png")
        self.is_killed = True
        self.counter = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_type):
        pygame.sprite.Sprite.__init__(self)
        if platform_type == 1:
            self.image = pygame.image.load("images/grass.png")
        elif platform_type == 2:
            self.image = pygame.image.load("images/dirt.png")
        self.image = pygame.transform.scale(self.image, (PLATFORM_SIZE, PLATFORM_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/lava.png")
        self.image = pygame.transform.scale(self.image, (PLATFORM_SIZE, PLATFORM_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, is_moving=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"images/Enemy_{random.randint(1, 8)}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_moving = is_moving
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        if self.is_moving:
            self.rect.x += self.move_direction
            self.move_counter += 1
            if self.move_counter > PLATFORM_SIZE:
                self.move_direction *= -1
                self.move_counter = 0

