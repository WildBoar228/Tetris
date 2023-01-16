import pygame
import random
import time
import os
import sys


def draw_field_of_play(scr):
    if bg:
        name = os.path.join('background', f'bg_{bg}.png')
        image = pygame.image.load(name)
        all_sprites = pygame.sprite.Group()
        arrow = pygame.sprite.Sprite(all_sprites)
        arrow.image = image
        arrow.rect = arrow.image.get_rect()
        all_sprites.add(arrow)
        arrow.rect.x = 0
        arrow.rect.y = 75
        all_sprites.draw(screen)

    # все линии, значки паузы и рестарта
    pygame.draw.rect(scr, (0, 0, 0), (0, 0, 510, 75))

    pygame.draw.line(scr, color, (0, 0), (0, 780), width=9)
    pygame.draw.line(scr, color, (510, 0), (510, 780), width=10)
    pygame.draw.line(scr, color, (0, 780), (510, 780), width=10)

    pygame.draw.line(scr, color, (0, 72), (510, 72), width=5)
    pygame.draw.line(scr, (255, 0, 0), (0, 190), (510, 190), width=5)
    pygame.draw.line(scr, color, (77, 0), (77, 72), width=5)
    pygame.draw.line(scr, color, (432, 0), (432, 72), width=5)

    pygame.draw.rect(scr, color, (20, 15, 15, 40))
    pygame.draw.rect(scr, color, (45, 15, 15, 40))

    pygame.draw.circle(scr, color, (467, 35), 25, width=14)
    pygame.draw.rect(scr, (0, 0, 0), (467, 35, 25, 25))
    pygame.draw.polygon(scr, color, ((472, 35), (498, 35), (485, 48)))

    # ведение счёта
    font = pygame.font.Font(None, 80)
    text = font.render(str(score), True, color)
    text_x = width // 2 - text.get_width() // 2
    scr.blit(text, (text_x, 10))


# экран паузы/стартовый экран
def draw_standby_screen(scr):
    scr.fill((0, 0, 0))
    if bg:
        name = os.path.join('background', f'bg_{bg}.png')
        image = pygame.image.load(name)
        all_sprites = pygame.sprite.Group()
        arrow = pygame.sprite.Sprite(all_sprites)
        arrow.image = image
        arrow.rect = arrow.image.get_rect()
        all_sprites.add(arrow)
        arrow.rect.x = 0
        arrow.rect.y = 75
        all_sprites.draw(screen)

    pygame.draw.line(screen, color, (0, 72), (510, 72), width=5)

    pygame.draw.rect(screen, color, ((32, 10), (20, 50)))
    pygame.draw.rect(screen, color, ((12, 10), (60, 10)))

    pygame.draw.rect(screen, color, ((97, 10), (20, 50)))
    pygame.draw.rect(screen, color, ((97, 10), (60, 10)))
    pygame.draw.rect(screen, color, ((97, 30), (60, 10)))
    pygame.draw.rect(screen, color, ((97, 50), (60, 10)))

    pygame.draw.rect(screen, color, ((202, 10), (20, 50)))
    pygame.draw.rect(screen, color, ((182, 10), (60, 10)))

    pygame.draw.rect(screen, color, ((267, 10), (20, 50)))
    pygame.draw.rect(screen, color, ((307, 10), (20, 30)))
    pygame.draw.rect(screen, color, ((267, 10), (60, 10)))
    pygame.draw.rect(screen, color, ((267, 30), (60, 10)))

    pygame.draw.rect(screen, color, ((352, 10), (20, 50)))
    pygame.draw.rect(screen, color, ((392, 10), (20, 50)))
    pygame.draw.polygon(screen, color, ((352, 60), (392, 10), (411, 10), (370, 60)))

    pygame.draw.rect(screen, color, ((437, 10), (20, 50)))
    pygame.draw.rect(screen, color, ((437, 10), (60, 10)))
    pygame.draw.rect(screen, color, ((437, 50), (60, 10)))

    font = pygame.font.Font(None, 90)
    if start:
        text = font.render('Пауза', True, color)
    else:
        text = font.render('Старт', True, color)
    text_x = width // 2 - text.get_width() // 2
    scr.blit(text, (text_x, 180))
    pygame.draw.polygon(scr, color, ((230, 290), (270, 310), (230, 330)))

    pygame.draw.line(scr, color, (0, 440), (510, 440), 3)
    pygame.draw.line(scr, color, (255, 440), (255, 780), 3)
    font = pygame.font.Font(None, 30)

    text = font.render('Выбор фона', True, color)
    text_x = width // 4 - text.get_width() // 2
    scr.blit(text, (text_x, 470))
    pygame.draw.polygon(scr, color, ((220, 600), (240, 610), (220, 620)))
    pygame.draw.polygon(scr, color, ((40, 600), (20, 610), (40, 620)))

    text = font.render('Выбор цвета', True, color)
    text_x = width // 4 - text.get_width() // 2
    scr.blit(text, (text_x + width // 2, 470))
    pygame.draw.polygon(scr, color, ((470, 600), (490, 610), (470, 620)))
    pygame.draw.polygon(scr, color, ((290, 600), (270, 610), (290, 620)))
    pygame.draw.circle(scr, color, (382, 610), 30)


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
        w = len(figure.board[0]) * figure.cell_size
        figure.left = (width / 2 - w / 2) // board.cell_size * board.cell_size
        figure.top = 100
    return figure


def add_score(sc):
    global score
    score += sc


def new_game():
    global score
    score = 0
    board.is_game = True
    board.board = [[0 for i in range(17)] for i in range(100)]
    board.bricks = pygame.sprite.Group()
    create_new_fig()


class Board:
    def __init__(self):
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.board = []
        self.bricks = pygame.sprite.Group()
        self.is_game = True

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(26):
            if all(self.board[y]):
                print(1234)
                for brick in self.board[y]:
                    self.bricks.remove(brick)
                    add_score(brick.price)
                self.board[y] = [0 for i in range(len(self.board[y]))]
                for i in range(y, 0, -1):
                    self.board[i] = self.board[i - 1]
                    for brick in self.board[i]:
                        if isinstance(brick, Brick):
                            brick.pos = (brick.pos[0], brick.pos[1] + self.cell_size)

        self.bricks.update()
        self.bricks.draw(screen)

    def get_cell(self, pos):
        x_coord = (pos[0] - self.left) // self.cell_size
        y_coord = (pos[1] - self.top) // self.cell_size
        return (x_coord, y_coord)

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
        super().__init__()

        for line in form.split('\n'):
            self.board.append([])
            for cell in line:
                if cell == ' ':
                    self.board[-1].append(0)
                else:
                    self.board[-1].append(1)

        self.color = random.choice(['red', 'green', 'blue', 'yellow', 'cian', 'purple'])
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

        if self.bottom_border() >= screen.get_height() or self.is_touching_board():
            self.join_to_board()

    def rotate_left(self):
        try:
            if self.top < 630:
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
                self.bricks.update()

                if self.left_border() < 0 or self.right_border() > screen.get_width():
                    self.rotate_right()

                if self.is_touching_board():
                    self.rotate_right()
        except IndexError:
            pass

    def rotate_right(self):
        try:
            if self.top < 630:
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
                self.bricks.update()

                if self.left_border() < 0 or self.right_border() > screen.get_width():
                    self.rotate_left()

                if self.is_touching_board():
                    self.rotate_left()
        except IndexError:
            pass

    def update_bricks_pos(self):
        """После поворотов переопределяем позиции блоков относительно центрального"""
        x1 = self.center_index[1]
        y1 = self.center_index[0]
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.board[y][x].pos = (self.cell_size * (x - x1),
                                        self.cell_size * (y - y1))

    def move_right(self):
        try:
            if self.right_border() + self.cell_size > screen.get_width():
                print('wall')
                return
            self.left += self.cell_size
            self.update_bricks_pos()
            self.bricks.update()

            if self.is_touching_board():
                self.move_left()
        except Exception:
            pass

    def move_left(self):
        try:
            if self.left_border() - self.cell_size < 0:
                print('wall')
                return
            self.left -= self.cell_size
            self.update_bricks_pos()
            self.bricks.update()

            if self.is_touching_board():
                self.move_right()
        except Exception:
            pass

    def render(self, screen):
        self.bricks.draw(screen)

    def left_border(self):
        br = [(brick, brick.pos[0] + self.left) for brick in self.bricks if brick is not None]
        return min(br, key=lambda b: b[1])[1]

    def right_border(self):
        br = [(brick, brick.pos[0] + self.left + self.cell_size) for brick in self.bricks if brick is not None]
        return max(br, key=lambda b: b[1])[1]

    def top_border(self):
        br = [(brick, brick.pos[1] + self.top) for brick in self.bricks if brick is not None]
        return min(br, key=lambda b: b[1])[1]

    def bottom_border(self):
        br = [(brick, brick.pos[1] + self.top + self.cell_size) for brick in self.bricks if brick is not None]
        return max(br, key=lambda b: b[1])[1]

    def join_to_board(self):
        for brick in self.bricks:
            if brick.rect.y < 190:
                board.is_game = False
            index = board.get_cell((brick.pos[0] + self.cell_size // 2 + self.left + self.center_index[0],
                                    brick.pos[1] + self.cell_size // 2 + self.top + self.center_index[1]))
            print(index)
            board.board[int(index[1])][int(index[0])] = brick
            brick.pos = (index[0] * self.cell_size, index[1] * self.cell_size)
            brick.fig = board
            board.bricks.add(brick)
        self.board = []
        self.bricks = pygame.sprite.Group()

    def is_touching_board(self):
        stop = False
        for brick in self.bricks:
            if pygame.sprite.spritecollideany(brick, board.bricks):
                stop = True
                break
        return stop


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos, fig, *group):
        super().__init__(*group)

        if random.randint(1, 10) == 1:
            self.price = 30
            self.image = load_image('golden_brick1.png')
            self.image_index = 0
            self.images = [load_image('golden_brick1.png'),
                           load_image('golden_brick2.png'),
                           load_image('golden_brick3.png')]
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.scale(self.images[i], (fig.cell_size, fig.cell_size))
            self.last_change_time = time.time()
        else:
            self.price = 10
            self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (fig.cell_size, fig.cell_size))
        self.rect = pygame.Rect(0, 0, fig.cell_size, fig.cell_size)
        # pos - это позиция относительно левого верхнего края фигуры
        self.pos = pos
        self.fig = fig

    def update(self):
        self.rect.x = self.fig.left + self.pos[0]
        self.rect.y = self.fig.top + self.pos[1]

        if self.price == 30 and time.time() - self.last_change_time > 0.5:
            self.image_index += 1
            self.image_index %= len(self.images)
            self.last_change_time = time.time()
            self.image = self.images[self.image_index]


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

    board = Board()
    board.set_view(0, 0, 30)
    board.board = [[0 for i in range(17)] for i in range(100)]
    fps = 50
    clock = pygame.time.Clock()
    running = True
    pause = True
    start = False
    score = 0
    color = (255, 255, 255)
    bg = 0

    # MOVING = pygame.USEREVENT + 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not start:
                        start = True
                        figure = create_new_fig()
                    if pause:
                        pause = False
                    else:
                        pause = True
                elif event.key == pygame.K_KP_ENTER:
                    new_game()
                    pause = True
                    start = False

                # повернуть по часовой стрелке - K_UP
                # повернуть против часовой стрелки - K_DOWN
                # подвинуть вправо - K_RIGHT
                # подвинуть влево - K_LEFT

                if board.is_game:
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
                if event.button not in [4, 5]:  # 4 и 5 - прокручивания мыши
                    if pause:
                        if event.pos[0] > 382 and event.pos[0] < 510 and event.pos[1] > 440 and event.pos[1] < 780:
                            if color == (255, 255, 255):
                                color = (255, 155, 155)
                            elif color == (255, 155, 155):
                                color = (155, 255, 155)
                            elif color == (155, 255, 155):
                                color = (155, 155, 255)
                            elif color == (155, 155, 255):
                                color = (155, 255, 255)
                            elif color == (155, 255, 255):
                                color = (255, 255, 155)
                            elif color == (255, 255, 155):
                                color = (255, 155, 255)
                            else:
                                color = (255, 255, 255)
                        if event.pos[0] > 255 and event.pos[0] < 382 and event.pos[1] > 440 and event.pos[1] < 780:
                            if color == (255, 255, 255):
                                color = (255, 155, 255)
                            elif color == (255, 155, 155):
                                color = (255, 255, 255)
                            elif color == (155, 255, 155):
                                color = (255, 155, 155)
                            elif color == (155, 155, 255):
                                color = (155, 255, 155)
                            elif color == (155, 255, 255):
                                color = (155, 155, 255)
                            elif color == (255, 255, 155):
                                color = (155, 255, 255)
                            else:
                                color = (255, 255, 155)
                        if event.pos[0] > 0 and event.pos[0] < 127 and event.pos[1] > 440 and event.pos[1] < 780:
                            if not bg:
                                bg = 15
                            else:
                                bg -= 1
                        if event.pos[0] > 127 and event.pos[0] < 255 and event.pos[1] > 440 and event.pos[1] < 780:
                            if bg == 15:
                                bg = 0
                            else:
                                bg += 1
                        if event.pos[1] < 440:
                            pause = False
                            if not start:
                                start = True
                                figure = create_new_fig()
                    elif event.pos[0] > 0 and event.pos[0] < 75 and event.pos[1] > 0 and event.pos[1] < 70:
                        pause = True
                    elif event.pos[0] > 435 and event.pos[0] < 510 and event.pos[1] > 0 and event.pos[1] < 70:
                        new_game()
                        pause = True
                        start = False

            '''if pause:
                pygame.time.set_timer(MOVING, 0)
            else:
                pygame.time.set_timer(MOVING, 1000)

            if event.type == MOVING:
                figure.top += 30'''

        # отрисовка экрана
        if pause:
            draw_standby_screen(screen)
        else:
            start = True
            screen.fill((0, 0, 0))
            figure.render(screen)
            draw_field_of_play(screen)
            if len(figure.bricks) <= 0:
                figure = create_new_fig()
            board.render(screen)
            if board.is_game:
                figure.update(fps)
                figure.render(screen)

        # Оповещение о проигрыше
        if not board.is_game:
            font = pygame.font.Font(None, 80)
            text = font.render('GAME OVER', True, (237, 28, 36))
            text_x = width // 2 - text.get_width() // 2
            screen.blit(text, (text_x, 250))

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()