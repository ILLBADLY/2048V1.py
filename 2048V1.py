import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Определение размеров окна
WINDOW_SIZE = (500, 600)

# Определение размеров ячейки и отступов
CELL_SIZE = 100
CELL_PADDING = 10

# Определение шрифта
FONT = pygame.font.Font(None, 64)

# Создание окна
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048")


# Генерация новой случайной плитки
def generate_tile(grid):
    # Поиск свободных ячеек
    empty_cells = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                empty_cells.append((row, col))

    # Если нет свободных ячеек
    if len(empty_cells) == 0:
        return

    # Выбираем случайную свободную ячейку
    row, col = random.choice(empty_cells)

    # Генерируем случайное значение плитки (2 или 4)
    value = random.choice([2, 4])

    # Устанавливаем значение плитки в выбранной ячейке
    grid[row][col] = value


# Отрисовка сетки
def draw_grid(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # Определение координат верхнего левого угла ячейки
            x = col * CELL_SIZE + (col + 1) * CELL_PADDING
            y = row * CELL_SIZE + (row + 1) * CELL_PADDING

            # Определение цвета плитки на основе ее значения
            if grid[row][col] == 0:
                color = GRAY
            else:
                color = WHITE

            # Отрисовка прямоугольника с заданными координатами и цветом
            pygame.draw.rect(window, color, (x, y, CELL_SIZE, CELL_SIZE))

            # Если значение плитки не равно 0, выводим его на экран
            if grid[row][col] != 0:
                # Создание поверхности для отображения значения плитки
                text_surface = FONT.render(str(grid[row][col]), True, BLACK)

                # Определение координат для центрирования значения плитки
                text_x = x + CELL_SIZE / 2 - text_surface.get_width() / 2
                text_y = y + CELL_SIZE / 2 - text_surface.get_height() / 2

                # Отрисовка значения плитки на экране
                window.blit(text_surface, (text_x, text_y))


# Объединение плиток
def merge(grid):
    # Сдвигаем плитки влево
    for row in range(len(grid)):
        merged = False
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                continue
            for prev_col in range(col - 1, -1, -1):
                if grid[row][prev_col] == 0:
                    continue
                if grid[row][prev_col] == grid[row][col]:
                    grid[row][prev_col] *= 2
                    grid[row][col] = 0
                    merged = True
                    break
                else:
                    break
            if merged:
                break

    # Сдвигаем плитки влево еще раз (для удаления пустых ячеек между плитками)
    for row in range(len(grid)):
        for col in range(len(grid[row]) - 1):
            if grid[row][col] == 0 and grid[row][col + 1] != 0:
                grid[row][col] = grid[row][col + 1]
                grid[row][col + 1] = 0


# Проверка возможности перемещения плиток
def check_move_possible(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                return True
            if row - 1 >= 0 and grid[row][col] == grid[row - 1][col]:
                return True
            if row + 1 < len(grid) and grid[row][col] == grid[row + 1][col]:
                return True
            if col - 1 >= 0 and grid[row][col] == grid[row][col - 1]:
                return True
            if col + 1 < len(grid[row]) and grid[row][col] == grid[row][col + 1]:
                return True
    return False


# Генерация новой плитки и проверка возможности хода после каждого перемещения
def make_move(grid, direction):
    # Поворачиваем сетку в соответствии с направлением движения
    if direction == "up":
        grid = list(map(list, zip(*grid[::-1])))
    elif direction == "down":
        grid = list(map(list, zip(*grid)))[::-1]
    elif direction == "left":
        grid = [list(row) for row in grid]
    elif direction == "right":
        grid = [list(row[::-1]) for row in grid]

    # Сохраняем сетку до перемещения для последующего сравнения
    previous_grid = [list(row) for row in grid]

    # Объединяем плитки
    merge(grid)

    # Генерируем новую случайную плитку
    generate_tile(grid)

    # Проверяем, возможен ли ход
    if previous_grid != grid or check_move_possible(grid):
        return grid
    else:
        return None


# Инициализируем сетку 4x4 и генерируем две случайные плитки
grid = [[0] * 4 for _ in range(4)]
generate_tile(grid)
generate_tile(grid)

# Основной цикл игры
running = True
while running:
    window.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                grid = make_move(grid, "up")
            elif event.key == pygame.K_DOWN:
                grid = make_move(grid, "down")
            elif event.key == pygame.K_LEFT:
                grid = make_move(grid, "left")
            elif event.key == pygame.K_RIGHT:
                grid = make_move(grid, "right")

    # Отрисовка сетки
    draw_grid(grid)

    # Обновление экрана
    pygame.display.flip()

# Выход из игры
pygame.quit()