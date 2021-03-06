import pygame
import random


pygame.init()

FPS = 60

scr_size = (width, height) = (800, 600)

clock = pygame.time.Clock()
# цвета для нашей игры(их константы)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption('PygamePingPongProject')  # название приложения

"""
функция для показа и выводы текста
"""


def displaytext(text, fontsize, x, y, color):  # параметры текста
    font = pygame.font.SysFont('Arial', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)


"""
функция для движения противника
она будет двигатся, основываясь на координатах мячика
"""


def cpumove(cpu, ball):
    if ball.movement[0] > 0:  # бортик противника двигается только когда он летит на него
        # иногда противник будет пропускать мячик
        if ball.rect.bottom > cpu.rect.bottom + cpu.rect.height/4:
            cpu.movement[1] = 10
        elif ball.rect.top < cpu.rect.top - cpu.rect.height/4:
            cpu.movement[1] = -10
        else:
            cpu.movement[1] = 0
    else:
        cpu.movement[1] = 0


def usermove(paddle, ball):
    if ball.movement[0] > 0:  # бортик противника двигается только когда он летит на него
        # иногда противник будет пропускать мячик
        if ball.rect.bottom > paddle.rect.bottom + paddle.rect.height/4:
            paddle.movement[1] = 10
        elif ball.rect.top < paddle.rect.top - paddle.rect.height/4:
            paddle.movement[1] = -10
        else:
            paddle.movement[1] = 0
    else:
        paddle.movement[1] = 0


class Paddle(pygame.sprite.Sprite):  # класс для создания игровых бортиков))
    def __init__(self, x, y, sizex, sizey, color):  # данные бортиков(их цвет, размер и тд)
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.image = pygame.Surface((sizex, sizey), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image, self.color, (0, 0, sizex, sizey))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.points = 0
        self.movement = [0, 0]

    # метод, не дающий бортикам выйти за пределы поля
    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    # метод, обновляющий состояние бортика
    def update(self):
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    # метод, который отрисовывает бортики
    def draw(self):
        screen.blit(self.image, self.rect)


"""
класс для работы с игровым мячом
"""


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, movement=[0, 0]):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.movement = movement  # движение мячика по x и y (отражено в списке соот. параметрами)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, (int(self.rect.width / 2),
                                                    int(self.rect.height / 2)),
                           int(size / 2))
        self.rect.centerx = x
        self.rect.centery = y
        self.maxspeed = 20
        self.score = 0
        self.movement = movement

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    # метод определяет как будет двигаться мяч
    def update(self):
        # изменяет скорость по вертикали при взаимодействии с верхом и низом
        if self.rect.top == 0 or self.rect.bottom == height:
            self.movement[1] = -1 * self.movement[1]
        if self.rect.left == 0:  # обновляет положение мяча и засчитывает очко противнику
            self.rect.centerx = width / 2
            self.rect.centery = height / 2
            self.movement = [random.randrange(-1, 2, 2) * 4, random.randrange(-1, 2, 2) * 4]
            self.score = 1

        if self.rect.right == width:  # обновляет положение мяча и засчитывает очко нам
            self.rect.centerx = width / 2
            self.rect.centery = height / 2
            self.movement = [random.randrange(-1, 2, 2) * 4, random.randrange(-1, 2, 2) * 4]
            self.score = -1

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        pygame.draw.circle(self.image, self.color, (int(self.rect.width / 2), int(self.rect.height / 2)),
                           int(self.size / 2))
        screen.blit(self.image, self.rect)


def main():
    gameOver = False  # задает начальное состояние игры
    paddle = Paddle(width / 10, height / 2, width / 60, height / 8, white)  # создает бортик для нас
    cpu = Paddle(width - width / 10, height / 2, width / 60, height / 8, (0, 0, 255))  # создает бортик для противника
    ball = Ball(width / 2, height / 2, 12, red, [4, 4])  # создает мячик

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # нажали вверх
                    paddle.movement[1] = -8   # бортик поднимается вверз
                elif event.key == pygame.K_DOWN:  # нажали вниз
                    paddle.movement[1] = 8       # бортик двигается вниз
            if event.type == pygame.KEYUP:    # отпускаем кнопку
                paddle.movement[1] = 0        # бортик останавливается

        cpumove(cpu, ball)  # перемещает бордик противника

        screen.fill(black)   # делает фон черным

        #  отрисовка бордиков и мяча
        paddle.draw()
        cpu.draw()
        ball.draw()

        #  показ очков игроков
        displaytext(str(paddle.points),
                    20, width / 8, 25, (255, 255, 255))
        displaytext(str(cpu.points),
                    20, width - width / 8, 25, (255, 255, 255))

        """
        даем проверку на 'хитбокс' бортикам и мячу
        т.е. чтобы соприкосновение с мячем и бортиком было максимально близким , и потом
        уже отталкивание
        """
        if pygame.sprite.collide_mask(paddle, ball):
            ball.movement[0] = -1 * ball.movement[0]
            ball.movement[1] = ball.movement[1] - int(0.1 * random.randrange(5, 10) * paddle.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1 * ball.maxspeed:
                ball.movement[1] = -1 * ball.maxspeed

        if pygame.sprite.collide_mask(cpu, ball):
            ball.movement[0] = -1 * ball.movement[0]
            ball.movement[1] = ball.movement[1] - int(0.1*random.randrange(5, 10) * cpu.movement[1])
            if ball.movement[1] > ball.maxspeed:
                ball.movement[1] = ball.maxspeed
            if ball.movement[1] < -1 * ball.maxspeed:
                ball.movement[1] = -1 * ball.maxspeed

        # даем баллы игрокам
        if ball.score == 1:
            cpu.points += 1
            ball.score = 0
        elif ball.score == -1:
            paddle.points += 1
            ball.score = 0

        # обновляем состояния объектам
        paddle.update()
        ball.update()
        cpu.update()

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()


main()