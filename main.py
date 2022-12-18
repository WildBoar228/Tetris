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


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.move = 0
        self.is_game = True

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        '''for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 pygame.Rect(self.left + self.cell_size * x,
                                             self.top + self.cell_size * y,
                                             self.cell_size, self.cell_size),
                                 width=1)'''

    def get_cell(self, mouse_pos):
        if mouse_pos[0] < self.left or mouse_pos[0] > self.left + self.width * self.cell_size:
            return None
        if mouse_pos[1] < self.top or mouse_pos[1] > self.top + self.height * self.cell_size:
            return None
        x_coord = (mouse_pos[0] - self.left) // self.cell_size
        y_coord = (mouse_pos[1] - self.top) // self.cell_size
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
                if elem == 0:
                    output += ' '
                else:
                    output += '*'
            output += '\n'
        return output


class Figure(Board):
    def __init__(self, form):
        super().__init__(len(form.split('\n')), len(form.split('\n')[0]))

        for line in form.split('\n'):
            self.board.append([])
            for cell in line:
                if cell == ' ':
                    self.board[-1].append(0)
                else:
                    self.board[-1].append(1)

        self.bricks = pygame.sprite.Group()

    def rotate(self):
        print('rotate 90')
        m2 = [[0 for i in range(len(self.board))] for i in range(len(self.board[0]))]
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                y2 = x
                x2 = len(self.board[0]) - y - 1
                m2[x2][y2] = self.board[x][y]
        self.board = m2


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos, fig):
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.fig = fig

    def update(self):
        self.rect.x = self.fig.rect.x + self.pos[0]
        self.rect.y = self.fig.rect.y + self.pos[1]


if __name__ == '__main__':
    pygame.init()

    size = width, height = 510, 780
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Тетрис')

    board = Board(10, 20)
    board.set_view(0, 0, 30)
    fps = 50
    clock = pygame.time.Clock()
    running = True
    pause = True
    start = False
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not start:
                    with open('data/figures.txt') as file:
                        figs = file.read().split('\n\n')[:-1]
                        figure = Figure(random.choice(figs))
                        print(figure)
                        figure.rotate()
                        print(figure)
                        figure.rotate()
                        print(figure)
                        figure.rotate()
                        print(figure)
                        figure.rotate()
                start = True
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
                elif event.key == pygame.K_KP_ENTER:
                    pause = True
                    start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button not in [4, 5]: # 4 и 5 - прокручивания мыши
                    if not start:
                        with open('data/figures.txt') as file:
                            figs = file.read().split('\n\n')[:-1]
                            figure = Figure(random.choice(figs))
                            print(figure)
                            figure.rotate()
                            print(figure)
                            figure.rotate()
                            print(figure)
                            figure.rotate()
                            print(figure)
                            figure.rotate()
                    if pause:
                        pause = False
                    elif event.pos[0] > 0 and event.pos[0] < 75 and event.pos[1] > 0 and event.pos[1] < 70:
                        pause = True
                    elif event.pos[0] > 435 and event.pos[0] < 510 and event.pos[1] > 0 and event.pos[1] < 70:
                        pause = True
                    start = False

            # отрисовка экрана
            if pause:
                draw_standby_screen(screen)
            else:
                start = True
                draw_field_of_play(screen)
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

