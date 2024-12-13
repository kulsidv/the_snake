"""Игра Змейка."""

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Абстрактный класс, от которого наследуются остальные."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=None,):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Абстрактный метод"""
        pass


class Apple(GameObject):
    """Класс яблока, его положение определяется рандомно."""

    def __init__(self):
        super().__init__(self.randomize_position(), APPLE_COLOR)

    def randomize_position(self):
        """Определяет позицию яблока"""
        x = randint(0, GRID_WIDTH) * GRID_SIZE
        y = randint(0, GRID_HEIGHT) * GRID_SIZE
        return (x, y)

    def draw(self):
        """Отрисовывает яблоко"""
        self.rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, self.rect)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 1)


class Snake(GameObject):
    """Класс Змейки, обладает длиной и направлением движения"""

    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.position = self.get_head_position()

    def update_direction(self):
        """Обновляет направление змейки"""
        """в соответствии с действиями пользователя"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Создает видимость движения змейки"""
        self.position = self.get_head_position()
        width = self.position[0] + self.direction[0] * GRID_SIZE
        height = self.position[1] + self.direction[1] * GRID_SIZE
        new_x = width % SCREEN_WIDTH
        new_y = height % SCREEN_HEIGHT
        body = self.positions[1:len(self.positions) - 1]
        if new_x in body or new_y in body:
            self.reset()
        else:
            self.positions.insert(0, (new_x, new_y))
            if len(self.position) > self.length:
                self.positions.pop()

    def draw(self):
        """Отрисовывает змейку"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку до начала"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def main():
    """Основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple = Apple()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    # Функция обработки действий пользователя
    main()


def handle_keys(game_object):
    """Отклик на действия пользоватля"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
