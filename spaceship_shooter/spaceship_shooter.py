import pygame
from pygame.math import Vector2
import numpy as np
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
GREEN = (0, 128, 0)
MAROON = (128, 0, 0)
BRIGHT_BLUE = (0, 0, 255)
BLUE = (0, 0, 128)

ASSETS_DIR = "../assets/"
BACKGROUND_IMG_PATH = ASSETS_DIR + "background.png"
SPACESHIP_IMG_PATH = ASSETS_DIR + "spaceship.png"
ASTEROID_IMG_PATH = ASSETS_DIR + "asteroid.png"
BULLET_IMG_PATH = ASSETS_DIR + "bullet.png"
EXPLOSION_IMG_PATHS = [ASSETS_DIR+"explosions/regularExplosion0%d.png" % i for i in range(9)]

pygame.init()


def draw_game_window(x=None, y=None):

    info_object = pygame.display.Info()
    if y is None:
        y = info_object.current_h
    if x is None:
        x = info_object.current_w

    return pygame.display.set_mode([x, y], pygame.RESIZABLE), x, y


def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def draw_button(surface, message, pos_x, pos_y, width, height, inactive_color, active_color):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos_x + width > mouse[0] > pos_x and pos_y + height > mouse[1] > pos_y:
        pygame.draw.rect(surface, active_color, (pos_x, pos_y, width, height))

        if click[0] == 1:
            return True

    else:
        pygame.draw.rect(surface, inactive_color, (pos_x, pos_y, width, height))

    button_font = pygame.font.SysFont("serif", height // 3 * 2)
    display_text(message, button_font, WHITE, (pos_x + (width / 2)), (pos_y + (height / 2)))

    return False


def quit_game():
    pygame.quit()
    quit()


def menu(screen, screen_width, screen_height, headline):
        while True:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    screen_width = event.w
                    screen_height = event.h

            headline_font = pygame.font.SysFont("serif", screen_width // 10)
            display_text(headline, headline_font, BLACK, (screen_width / 2), (screen_height / 2))

            button_play = draw_button(screen, "Go!", screen_width / 7 * 2, screen_height / 3 * 2, screen_width // 7,
                                      screen_height // 20, GREEN, BRIGHT_GREEN)
            button_quit = draw_button(screen, "Quit :(", screen_width / 7 * 4, screen_height / 3 * 2, screen_width // 7,
                                      screen_height // 20, MAROON, BRIGHT_RED)

            pygame.display.update()

            if button_play:
                return True, screen, screen_width, screen_height
            elif button_quit:
                return False


def pause(screen_width, screen_height):

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    quit_game()

        screen.fill(WHITE)

        larger_font = pygame.font.SysFont("serif", screen_width // 10)
        display_text("Paused", larger_font, BLACK, (screen_width / 2), (screen_height / 2))
        smaller_font = pygame.font.SysFont("serif", screen_width // 30)
        display_text("Press C to continue or Q to quit.", smaller_font, BLACK, (screen_width / 4), (screen_height / 4))
        pygame.display.update()


class Player(pygame.sprite.Sprite):

    def __init__(self, player_image, center):
        super().__init__()

        self.image = player_image.copy()
        self.rect = self.image.get_rect(center=center)
        self.original_image = self.image

        self.angle = 90
        self.angle_speed = 0

    def update(self):

        if self.angle_speed:

            self.angle += self.angle_speed
            self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)

    def redraw(self, new_image, new_center):
        self.image = new_image.copy()
        self.original_image = self.image

        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=new_center)


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, center, vel, angle, screen_width, screen_height, asteroid_image):
        super().__init__()

        self.image = asteroid_image.copy()
        self.rect = self.image.get_rect(center=center)
        self.vel = vel
        self.angle = angle

        self.boundary_w = screen_width
        self.boundary_h = screen_height

    def update(self):
        self.rect = self.rect.move(self.vel)

        if self.rect.center[0] > self.boundary_w or self.rect.center[0] < 0 \
           or self.rect.center[1] > self.boundary_h or self.rect.center[1] < 0:
            self.kill()

    def redraw(self, new_image, new_vel, new_screen_width, new_screen_height):
        self.image = new_image.copy()
        self.vel = new_vel
        self.boundary_w = new_screen_width
        self.boundary_h = new_screen_height


class Bullet(pygame.sprite.Sprite):

    def __init__(self, player, bullet_image, vel):
        super().__init__()
        self.angle = player.angle
        self.image = pygame.transform.rotate(bullet_image.copy(), self.angle - 90)
        self.rect = self.image.get_rect(center=player.rect.center)

        self.vel = Vector2(0, vel)
        self.vel.rotate_ip(-self.angle + 90)

    def update(self):

        self.rect = self.rect.move(self.vel)
        if self.rect.y < -10:
            self.kill()

    def redraw(self, new_image, new_vel):
        self.image = pygame.transform.rotate(new_image.copy(), self.angle - 90)
        self.vel = Vector2(0, new_vel)
        self.vel.rotate_ip(-self.angle + 90)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()

        self.image = pygame.image.load(EXPLOSION_IMG_PATHS[0]).convert_alpha()
        self.rect = self.image.get_rect(center=center)
        self.frame = 0

    def update(self):

        if self.frame == len(EXPLOSION_IMG_PATHS):
            self.kill()
        else:
            self.image = pygame.image.load(EXPLOSION_IMG_PATHS[self.frame]).convert_alpha()
            self.rect = self.image.get_rect(center=self.rect.center)

        self.frame += 1


class SpaceshipShooter:

    def __init__(self, screen, player):
        self.screen = screen

        self.asteroid_image = pygame.transform.scale(pygame.image.load(ASTEROID_IMG_PATH).convert_alpha(),
                                                     (self.screen_width // 25, self.screen_width // 25))
        self.bullet_image = pygame.transform.scale(pygame.image.load(BULLET_IMG_PATH).convert_alpha(),
                                                   (self.screen_width // 120, self.screen_width // 120 * 18 // 10))

        self.player = player
        self.asteroid_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.explosion_list = pygame.sprite.Group()
        
        self.score = 0
        self.seconds_before_next_call = None
        self.last_record_time = None
        self.counter_clockwise = True

    @property
    def screen_width(self):
        return self.screen.get_width()

    @property
    def screen_height(self):
        return self.screen.get_height()

    @property
    def radius(self):
        return math.sqrt((self.screen_width / 2) ** 2 + self.screen_height ** 2)

    def draw_screen(self):
        self.screen.blit(pygame.transform.scale(background, (self.screen_width, self.screen_height)), (0, 0))

        self.screen.blit(self.player.image, self.player.rect)
        self.bullet_list.draw(self.screen)
        self.asteroid_list.draw(self.screen)
        self.explosion_list.draw(self.screen)

        score_font = pygame.font.SysFont("serif", self.screen_width // 30)
        display_text("Score: %d" % self.score, score_font, WHITE, self.screen_width / 15, self.screen_height / 30)

    def get_position_on_screen_edge(self, angle):
        radius = math.sqrt((self.screen_width / 2) ** 2 + self.screen_height ** 2)
        pos_x = radius * math.cos(math.radians(angle))
        pos_y = radius * math.sin(math.radians(angle))

        if pos_x >= 0:
            pos_x = min(pos_x, self.screen_width / 2) + self.screen_width / 2
        else:
            pos_x = max(pos_x, -self.screen_width / 2) + self.screen_width / 2

        pos_y = self.screen_height - min(pos_y, self.screen_height)

        return pos_x, pos_y

    def generate_asteroid(self, speed, position, angle):
        return Asteroid(position, speed, angle, self.screen_width, self.screen_height, self.asteroid_image)

    def generate_sprite_with_random_speed_and_angle_on_screen_edge(
            self,
            speed_mean,
            speed_variance,
            angle_mean,
            angle_variance,
            counter_clockwise
    ):

        vel = Vector2(0, -np.random.normal(size=1, loc=speed_mean, scale=speed_variance))
        if vel[1] == 0:
            vel[1] = -speed_mean

        # counter_clockwise = True

        if counter_clockwise:
            angle = np.random.normal(size=1, loc=angle_mean, scale=angle_variance) + angle_variance
        else:
            angle = np.random.normal(size=1, loc=angle_mean, scale=angle_variance) - angle_variance

        vel.rotate_ip(-angle + 270)

        position = self.get_position_on_screen_edge(angle)
        return self.generate_asteroid(vel, position, angle)

    def generate_sprite_with_a_random_frequency(self, lam, *args):

        if self.seconds_before_next_call is None:
            self.seconds_before_next_call = np.random.poisson(lam)

        curr_record_time = pygame.time.get_ticks()

        if curr_record_time - self.last_record_time >= self.seconds_before_next_call:
            self.last_record_time = curr_record_time
            self.seconds_before_next_call = None
            return self.generate_sprite_with_random_speed_and_angle_on_screen_edge(*args)

    def check_hit_update_score(self):

        for bullet in self.bullet_list:

            asteroid_hit_list = pygame.sprite.spritecollide(bullet, self.asteroid_list, True)

            for asteroid in asteroid_hit_list:
                exp = Explosion((asteroid.rect.center[0], asteroid.rect.center[1]))
                self.explosion_list.add(exp)

                self.score += 1
                print(self.score)

            if len(asteroid_hit_list) is not 0:
                bullet.kill()

    def update_all_sprites(self):
        self.player.update()
        self.explosion_list.update()
        self.asteroid_list.update()
        self.bullet_list.update()

    def redraw_all_sprites(self):

        new_player_image = pygame.transform.scale(pygame.image.load(SPACESHIP_IMG_PATH).convert_alpha(),
                                                  (self.screen_width // 20, self.screen_width // 80 * 7))

        self.asteroid_image = pygame.transform.scale(pygame.image.load(ASTEROID_IMG_PATH).convert_alpha(),
                                                     (self.screen_width // 25, self.screen_width // 25))

        self.bullet_image = pygame.transform.scale(pygame.image.load(BULLET_IMG_PATH).convert_alpha(),
                                                   (self.screen_width // 120, self.screen_width // 200 * 3))

        self.player.redraw(new_player_image, (self.screen_width / 2, self.screen_height / 22 * 20))

        for asteroid in self.asteroid_list:
            new_vel = Vector2(0, -np.random.normal(size=1, loc=self.radius // 150, scale=1))
            new_vel.rotate_ip(-asteroid.angle + 270)
            asteroid.redraw(self.asteroid_image, new_vel, self.screen_width, self.screen_height)
        for bullet in self.bullet_list:
            new_vel = -self.radius // 150
            bullet.redraw(self.bullet_image, new_vel)

    def spaceship_game_loop(self):

        self.last_record_time = pygame.time.get_ticks()

        while True:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.player.angle >= 180:
                            self.counter_clockwise = False

                        if self.player.angle < 180:
                            self.player.angle_speed = 10

                    elif event.key == pygame.K_RIGHT:
                        if self.player.angle <= 0:
                            self.counter_clockwise = True

                        if self.player.angle > 0:
                            self.player.angle_speed = -10

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.angle_speed = 0

                    elif event.key == pygame.K_RIGHT:
                        self.player.angle_speed = 0

                    elif event.key == pygame.K_SPACE:
                        vel = -self.radius//150
                        bullet = Bullet(self.player, self.bullet_image, vel)
                        self.bullet_list.add(bullet)

                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.redraw_all_sprites()

            asteroid = self.generate_sprite_with_a_random_frequency(1500,
                                                                    self.radius//170,
                                                                    1,
                                                                    self.player.angle,
                                                                    10,
                                                                    self.counter_clockwise)

            if asteroid is not None:
                self.asteroid_list.add(asteroid)

            self.check_hit_update_score()

            self.update_all_sprites()

            self.draw_screen()

            button_pause = draw_button(self.screen, "Pause", self.screen_width / 15 * 12, self.screen_height / 40,
                                       self.screen_width // 7, self.screen_height // 20, BLUE, BRIGHT_BLUE)
            if button_pause:
                pause(self.screen_width, self.screen_height)

            pygame.display.flip()


if __name__ == '__main__':

    screen, screen_width, screen_height = draw_game_window(600, 600)
    pygame.display.set_caption("Spaceship Game")
    play, screen, screen_width, screen_height = menu(screen, screen_width, screen_height, "Spaceship Shooter")

    background = pygame.image.load(BACKGROUND_IMG_PATH)
    asteroids_generate_interval = 3000
    player_image = pygame.transform.scale(pygame.image.load(SPACESHIP_IMG_PATH).convert_alpha(),
                                          (screen_width // 20, screen_width // 20 * 7 // 4))

    if play:
        player = Player(player_image, (screen_width / 2, screen_height / 22 * 20))
        space_shooter = SpaceshipShooter(screen, player)
        space_shooter.spaceship_game_loop()

    else:
        quit_game()
