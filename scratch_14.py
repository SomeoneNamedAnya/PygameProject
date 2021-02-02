import pygame, math

FPS = 40
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
table_border = pygame.sprite.Group()
lenght_of_table = 20
table_x = 180
table_y = 300


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
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            print('*')
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


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('Жёлтый круг')
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    running = True
    ball = Ball(15, 180, 100)
    table = Table(lenght_of_table)
    clock = pygame.time.Clock()
    Border(10, 10, width - 10, 10)
    Border(10, height - 10, width - 10, height - 10)
    Border(10, 10, 10, height - 10)
    Border(width - 10, 10, width - 10, height - 10)
    x_pos = 100
    y_pos = 100
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
                    print('aasas')
                    table.v = 2
                if event.key == pygame.K_LEFT:
                    print('aasas')
                    table.v = -2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    print('aasas')
                    table.v = 0
                if event.key == pygame.K_LEFT:
                    print('aasas')
                    table.v = 0

        all_sprites.update()

        # Рендеринг
        screen.fill('black')
        all_sprites.draw(screen)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
