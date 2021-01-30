import pygame, random

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 0.0025
        self.vy = 0.025

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


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
    ball = Ball(20, 100, 100)
    clock = pygame.time.Clock()
    horizontal_borders.add(Border(5, 5, width - 5, 5))
    horizontal_borders.add(Border(5, height - 5, width - 5, height - 5))
    vertical_borders.add(Border(5, 5, 5, height - 5))
    vertical_borders.add(Border(width - 5, 5, width - 5, height - 5))
    x_pos = 100
    y_pos = 100
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('black')
        ball.update()

        x_pos += ball.vx
        y_pos += ball.vy

        screen.blit(ball.image, (x_pos, y_pos))

        pygame.display.flip()
