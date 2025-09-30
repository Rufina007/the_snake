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

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()
 

class GameObject:
    '''Основной класс, который содержит позицию и цвет объекта.'''
    
    def __init__(self) -> None:
        '''
        Инициализация позиции объекта в центре экрана  и его цвета.
        '''
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        '''
        метод для отрисовки объекта.
        '''
        pass


class Apple(GameObject):
    '''Отвечает за создание координат яблока и его отображения.'''
    
    def __init__(self):
        '''
        Инициализирует цвет яблока и его рандомную позицию.
        '''
        super().__init__()
        self.body_color = APPLE_COLOR  
        self.randomize_position()
                                
    def randomize_position(self):
        '''
        Генерирует случайные координаты яблока.
        '''
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE 
        self.position = (x, y)
        
    def draw(self):
        '''
        Отвечает за отрисовку яблока.
        '''
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    '''Класс, отвечающий за движение змейки и отрисовки на поле.'''
    
    def __init__(self):
        '''
        Инициализация змейки: длинна - 1, начальная позиция - центр,
        направление - вправо, цвет.
        '''
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None  # следующее направление движения.
        self.body_color = SNAKE_COLOR
        self.last = None  # хранения позиции последнего сегмента змейки
                   
    def update_direction(self):
        '''
        Метод обновления направления после нажатия на кнопку.
        '''
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        '''
        Обновляет позицию змейки, добавляя новую голову в начало списка
        positions и удаляя последний элемент, если длина змейки не увеличилась.
        '''
        x, y = self.direction
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None
   
    def draw(self):
        '''
        Отрисовывает тело и голову змеи, отвечает за стирание последнего
        сегмента змеи, если он смещен.
        '''
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
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
        '''
        Возвращает координаты головы змеи.
        '''
        return self.positions[0]
    
        
    def reset(self): 
        '''
        Cбрасывает змейку в начальное состояние: длина - 1,
        позиция - центр, направление - рандомное.
        '''  
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))] 
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
                          
def handle_keys(game_object):
    '''
    Обрабатывает нажатия клавиш, чтобы изменить направление движения змейки.
    '''
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


def main():
    '''
    Основной цикл игры: инициализация, создание объектов, обработка событий, 
    обновление игры и отрисовка.
    '''
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
        
        # проверка, что змея съела яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            
        # проверка, что змея не врезалась в себя.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()   
                
        pygame.display.update()

if __name__ == '__main__':
    main()










