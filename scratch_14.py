import pygame, math

import sys
import pygame
from moviepy.editor import *
import pygame_menu, math

pygame.init()
surface = pygame.display.set_mode((1280, 720))
song_start = pygame.mixer.Sound('Sounds/8bitlong.mp3')
music_logic = 1
size = width, height = 400, 400
FPS = 40
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
table_border = pygame.sprite.Group()
break_border = pygame.sprite.Group()
list_of_break = list()
lenght_of_table = 20
table_x = 180
table_y = 300
flag = True
life = 3


def music_play():
    song_start.play()
    global music_logic
    music_logic = 1


def music_stop():
    song_start.stop()
    global music_logic
    music_logic = 0


def start_game():
    start()


class StartPage():
    menu = pygame_menu.Menu(720, 1280, 'Arcanoid', theme=pygame_menu.themes.THEME_DARK)
    menu.add_button('Музыка Вкл', music_play())
    menu.add_button('Музыка Выкл', music_stop())
    menu.add_label('')
    menu.add_label('')
    menu.add_button('Играть', start_game)
    menu.add_label('')
    menu.add_button('Выйти', pygame_menu.events.EXIT)


class Break(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.len = 20
        self.x = x
        self.y = y
        self.image = pygame.Surface((2 * 20, 2 * 20), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("blue"),
                         (0, 0, 20, 20))
        self.rect = pygame.Rect((x, y, 20, 20))
        self.add(break_border)
        # list_of_break.append(self)


class Table(pygame.sprite.Sprite):
    def __init__(self, length):
        super().__init__(all_sprites)
        self.len = length
        self.image = pygame.Surface((2 * length, 2 * length), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("white"),
                         (0, 0, 40, length))
        self.rect = pygame.Rect((180, 300, 40, length))
        self.add(table_border)
        self.v = 0

    def update(self):
        global table_x
        self.rect = self.rect.move(self.v, 0)
        table_x += self.v
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            print('*')
            self.v = 0
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.v = 0
            print('/')


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.first_start = True
        self.vx = 0
        self.vy = 0

    def update(self):
        # print(self.vx, self.vy)
        global table_x
        global height
        global flag
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            print('*')
            print(self.rect.y)
            if self.rect.y > 355:
                print('########################3')
                # quit()
                flag = False
                self.vy = 0
                self.vx = 0
            else:
                self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
            print('/')
        if pygame.sprite.spritecollideany(self, table_border):
            print(self.rect.x, self.rect.y, table_x)
            temp = lenght_of_table / 90
            p_vx = min(lenght_of_table / 2, abs(self.rect.x - table_x - lenght_of_table / 2))
            if self.rect.x - table_x - lenght_of_table / 2 < 0:
                p_vx *= -1
            p_vy = lenght_of_table / 2
            if p_vy > 0:
                p_vy *= -1
            p_xy = math.sqrt(p_vx ** 2 + p_vy ** 2)
            kf = 5 / p_xy
            print(p_vy, p_xy, p_vx, kf)
            self.vx = p_vx * kf
            self.vy = p_vy * kf

            print(self.vy, self.vx)
        if pygame.sprite.spritecollideany(self, break_border):
            gets_hit = pygame.sprite.spritecollideany(self, break_border)
            print(gets_hit.x, gets_hit.y, self.rect.x, self.rect.y, '*****************')
            if gets_hit.x <= self.rect.x and gets_hit.x + 20 >= self.rect.x:
                self.vy = -self.vy
            if gets_hit.y <= self.rect.y and gets_hit.y + 20 >= self.rect.y:
                self.vx = -self.vx
            for some_sprite in break_border:
                # print(some_sprite)
                if gets_hit == some_sprite:
                    break_border.remove(some_sprite)
                    some_sprite.kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def first_level():
    temp_x = 11
    temp_y = 10
    for j in range(5):
        for i in range(18):
            Break(temp_x, temp_y)
            temp_x += 20 + 1
        temp_x = 11
        temp_y += 30


def start():
    global life
    global flag
    pygame.init()
    pygame.display.set_caption('Жёлтый круг')

    screen = pygame.display.set_mode(size)
    screen.fill('black')
    running = True
    ball = Ball(15, 180, 269)
    table = Table(lenght_of_table)
    clock = pygame.time.Clock()
    Border(10, 10, width - 10, 10)
    Border(10, height - 10, width - 10, height - 10)
    Border(10, 10, 10, height - 10)
    Border(width - 10, 10, width - 10, height - 10)
    x_pos = 100
    y_pos = 100
    first_level()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ball.first_start is True:
                    ball.vy = -5
                    ball.first_start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if ball.first_start is True:
                        ball.vx = 2
                    print('aasas')
                    table.v = 2
                if event.key == pygame.K_LEFT:
                    if ball.first_start is True:
                        ball.vx = -2
                    print('aasas')
                    table.v = -2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if ball.first_start is True:
                        ball.vx = 0
                    print('aasas')
                    table.v = 0
                if event.key == pygame.K_LEFT:
                    if ball.first_start is True:
                        ball.vx = 0
                    print('aasas')
                    table.v = 0
        if ball.first_start is True:
            ball.rect = ball.rect.move(table.rect.x - ball.rect.x, 269 - ball.rect.y)
        all_sprites.update()

        # Рендеринг
        screen.fill('black')
        all_sprites.draw(screen)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        if flag is False:
            if life > 0:
                print(ball.rect.x, ball.rect.y, '+++++++++')
                table.rect = table.rect.move(180 - table.rect.x, 0)
                ball.rect = ball.rect.move(table.rect.x - ball.rect.x, 269 - ball.rect.y)
                print(ball.rect.x, ball.rect.y, '+++++++++')
                flag = True
                life -= 1
                ball.first_start = True



            else:
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


if __name__ == '__main__':
    pygame.display.set_caption('Arcanoid')
    clip = VideoFileClip(r"images/StartMovie.mp4")
    clip.preview()
    song_start.play()
    pygame.display.set_mode((1280, 720))

    StartP = StartPage()
    StartP.menu.mainloop(surface)
