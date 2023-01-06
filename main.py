import pygame
import random
import os
import sys


def draw_field_of_play(scr):
    scr.fill((0, 0, 0))

    # все линии, значки паузы и рестарта
    pygame.draw.line(scr, (255, 255, 255), (0, 0), (0, 780), width=9)
    pygame.draw.line(scr, (255, 255, 255), (510, 0), (510, 780), width=10)
    pygame.draw.line(scr, (255, 255, 255), (0, 780), (510, 780), width=10)

    pygame.draw.line(scr, (255, 255, 255), (0, 72), (510, 72), width=5)
    pygame.draw.line(scr, (255, 255, 255), (77, 0), (77, 72), width=5)
    pygame.draw.line(scr, (255, 255, 255), (432, 0), (432, 72), width=5)

    pygame.draw.rect(scr, (255, 255, 255), (20, 15, 15, 40))
    pygame.draw.rect(scr, (255, 255, 255), (45, 15, 15, 40))

    pygame.draw.circle(scr, (255, 255, 255), (467, 35), 25, width=14)
    pygame.draw.rect(scr, (0, 0, 0), (467, 35, 25, 25))
    pygame.draw.polygon(scr, (255, 255, 255), ((472, 35), (498, 35), (485, 48)))

    # ведение счёта
    font = pygame.font.Font(None, 80)
    text = font.render(str(score), True, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    scr.blit(text, (text_x, 10))


# экран паузы/стартовый экран
def draw_standby_screen(scr):
    scr.fill((0, 0, 0))
    font = pygame.font.Font(None, 90)
    if start:
        text = font.render('Пауза', True, (255, 255, 255))
    else:
        text = font.render('Старт', True, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    scr.blit(text, (text_x, 300))
    pygame.draw.polygon(scr, (255, 255, 255), ((230, 400), (270, 420), (230, 440)))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def create_new_fig():
    with open('data/figures.txt') as file:
        figs = file.read().split('\n\n')
        figure = Figure(figs[random.randint(0, len(figs) - 1)])
        figure.left = 100
        figure.top = 100
    return figure


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.board = []
        self.bricks = pygame.sprite.Group()
        self.move = 0
        self.is_game = True

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.bricks.draw(screen)

    def get_cell(self, pos):
        x_coord = (pos[0] - self.left) // self.cell_size
        y_coord = (pos[1] - self.top) // self.cell_size
        return (x_coord, y_coord)

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def __str__(self):
        output = ''
        for line in self.board:
            for elem in line:
                if elem == 0 or isinstance(elem, EmptyBrick):
                    output += ' '
                else:
                    output += '*'
            output += '\n'
        return output


class Figure(Board):
    def __init__(self, form, speed=100):
        super().__init__(len(form.split('\n')), len(form.split('\n')[0]))

        for line in form.split('\n'):
            self.board.append([])
            for cell in line:
                if cell == ' ':
                    self.board[-1].append(0)
                else:
                    self.board[-1].append(1)

        self.color = random.choice(['red', 'green', 'blue'])
        self.bricks = pygame.sprite.Group()
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 1:
                    brick = Brick(f'{self.color}_brick.png',
                                  (self.cell_size * x, self.cell_size * y), self)
                    self.bricks.add(brick)
                else:
                    brick = EmptyBrick((self.cell_size * x, self.cell_size * y), self)
                self.board[y][x] = brick

        # центральный блок (вокруг него вращается фигура) изначально в позиции (0, 0)
        self.center_index = (0, 0)
        print(self)
        self.center_brick = self.board[self.center_index[0]][self.center_index[1]]

        self.speed = speed

        self.update_bricks_pos()

    def update(self, fps):
        self.bricks.update()

        self.top += self.speed / fps

        stop = self.bottom_border() >= screen.get_height()
        print(self.bottom_border(), screen.get_height())
        print(stop)
        for brick in self.bricks:
            if pygame.sprite.spritecollideany(brick, board.bricks):
                stop = True
                break
        print(stop)
        print()
        if stop:
            self.join_to_board()

    def rotate_left(self):
        m2 = [[0 for i in range(len(self.board))] for i in range(len(self.board[0]))]
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                x2 = y
                y2 = len(self.board[0]) - x - 1
                m2[y2][x2] = self.board[y][x]
        
        # просчитываем новую позицию центрального блока в матрице
        self.center_index = (len(self.board[0]) - self.center_index[1] - 1,
                             self.center_index[0])
        self.board = m2

        self.update_bricks_pos()

        if self.left_border() < 0 or self.right_border() > screen.get_width():
            self.rotate_right()

    def rotate_right(self):
        m2 = [[0 for i in range(len(self.board))] for i in range(len(self.board[0]))]
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                x2 = len(self.board) - y - 1
                y2 = x
                m2[y2][x2] = self.board[y][x]
        
        # просчитываем новую позицию центрального блока в матрице
        self.center_index = (self.center_index[1],
                             len(self.board) - self.center_index[0] - 1)
        self.board = m2

        self.update_bricks_pos()

        if self.left_border() < 0 or self.right_border() > screen.get_width():
            self.rotate_left()

    def update_bricks_pos(self):
        """После поворотов переопределяем позиции блоков относительно центрального"""
        x1 = self.center_index[1]
        y1 = self.center_index[0]
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.board[y][x].pos = (self.cell_size * (x - x1),
                                        self.cell_size * (y - y1))

    def move_right(self):
        if self.right_border() + self.cell_size > screen.get_width():
            print('wall')
            return
        self.left += self.cell_size

    def move_left(self):
        if self.left_border() - self.cell_size < 0:
            print('wall')
            return
        self.left -= self.cell_size

    def render(self, screen):
        self.bricks.update()
        self.bricks.draw(screen)
    
    def left_border(self):
        br = [(brick, brick.pos[0] + self.left) for brick in self.bricks]
        return min(br, key=lambda b: b[1])[1]

    def right_border(self):
        br = [(brick, brick.pos[0] + self.left + self.cell_size) for brick in self.bricks]
        return max(br, key=lambda b: b[1])[1]

    def top_border(self):
        br = [(brick, brick.pos[1] + self.top) for brick in self.bricks]
        return min(br, key=lambda b: b[1])[1]

    def bottom_border(self):
        br = [(brick, brick.pos[1] + self.top + self.cell_size) for brick in self.bricks]
        return max(br, key=lambda b: b[1])[1]

    def join_to_board(self):
        for brick in self.bricks:
            index = board.get_cell((brick.pos[0] + self.cell_size // 2 + self.left,
                                    brick.pos[1] + self.cell_size // 2 + self.top))
            board.board[int(index[1])][int(index[0])] = brick
            board.bricks.add(brick)
        self.board = []
        self.bricks = pygame.sprite.Group()


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos, fig, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (fig.cell_size, fig.cell_size))
        self.rect = pygame.Rect(0, 0, fig.cell_size, fig.cell_size)
        # pos - это позиция относительно левого верхнего края фигуры
        self.pos = pos
        self.fig = fig

    def update(self):
        self.rect.x = self.fig.left + self.pos[0]
        self.rect.y = self.fig.top + self.pos[1]


# У него нет картинки и он не наследник класса pygame.sprite.Sprite,
# но позиция определяется так же, как у Brick
class EmptyBrick():
    def __init__(self, pos, fig):
        self.rect = pygame.Rect(0, 0, fig.cell_size, fig.cell_size)
        self.pos = pos
        self.fig = fig

    def update(self):
        self.rect.x = self.fig.left + self.pos[0]
        self.rect.y = self.fig.top + self.pos[1]


if __name__ == '__main__':
    pygame.init()

    size = width, height = 510, 780
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Тетрис')

    board = Board(10, 20)
    board.set_view(0, 0, 30)
    board.board = [[0 for i in range(100)] for i in range(100)]
    fps = 50
    clock = pygame.time.Clock()
    running = True
    pause = True
    start = False
    score = 0
    figure = create_new_fig()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                start = True
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
                elif event.key == pygame.K_KP_ENTER:
                    pause = True
                    start = False

                # повернуть по часовой стрелке - K_UP
                # повернуть против часовой стрелки - K_DOWN
                # подвинуть вправо - K_RIGHT
                # подвинуть влево - K_LEFT

                if event.key == pygame.K_DOWN:
                    figure.rotate_left()
                    print(figure)
                if event.key == pygame.K_UP:
                    figure.rotate_right()
                    print(figure)
                if event.key == pygame.K_RIGHT:
                    figure.move_right()
                if event.key == pygame.K_LEFT:
                    figure.move_left()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button not in [4, 5]: # 4 и 5 - прокручивания мыши
                    if pause:
                        pause = False
                    elif event.pos[0] > 0 and event.pos[0] < 75 and event.pos[1] > 0 and event.pos[1] < 70:
                        pause = True
                    elif event.pos[0] > 435 and event.pos[0] < 510 and event.pos[1] > 0 and event.pos[1] < 70:
                        pause = True
                    start = False
                    
        board.render(screen)
        # отрисовка экрана
        if pause:
            draw_standby_screen(screen)
        else:
            start = True
            draw_field_of_play(screen)
            if len(figure.bricks) <= 0:
                figure = create_new_fig()
            figure.update(fps)
            figure.render(screen)
            board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

