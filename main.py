import pygame
import random
import time
import os
import sys


if __name__ == '__main__':
    pygame.init()
    
    screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption('Тетрис')


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

        self.color = random.choice(['red', 'green', 'blue'])
        self.bricks = pygame.sprite.Group()
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 1:
                    brick = Brick(f'{self.color}_brick.png',
                                  (self.cell_size * x, self.cell_size * y), self)
                    self.board[y][x] = brick
                    self.bricks.add(brick)

    def rotate_left(self):
        m2 = [[0 for i in range(len(self.board))] for i in range(len(self.board[0]))]
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                y2 = x
                x2 = len(self.board[0]) - y - 1
                m2[x2][y2] = self.board[x][y]
        self.board = m2

        self.update_bricks_pos()

    def rotate_right(self):
        for i in range(3):
            self.rotate_left()

    def update_bricks_pos(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] != 0:
                    self.board[y][x].pos = (self.cell_size * x, self.cell_size * y)

    def render(self, screen):
        self.bricks.update()
        self.bricks.draw(screen)


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos, fig, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (fig.cell_size, fig.cell_size))
        self.rect = pygame.Rect(0, 0, fig.cell_size, fig.cell_size)
        self.pos = pos
        self.fig = fig

    def update(self):
        self.rect.x = self.fig.left + self.pos[0]
        self.rect.y = self.fig.top + self.pos[1]


if __name__ == '__main__':
    board = Board(10, 20)
    board.set_view(0, 0, 30)
    fps = 50
    clock = pygame.time.Clock()
    running = True

    with open('data/figures.txt') as file:
        figs = file.read().split('\n\n')[:-1]
        figure = Figure(figs[random.randint(0, len(figs))])
        figure.left = 100
        figure.top = 100
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print(1)
                    figure.rotate_left()
                    print(figure)
                if event.key == pygame.K_RIGHT:
                    figure.rotate_right()
                    print(2)
                    print(figure)
        
        screen.fill((0, 0, 0))
        board.render(screen)
        figure.render(screen)
        pygame.display.flip()

        clock.tick(fps)
    
    pygame.quit()

