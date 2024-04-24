import numpy as np
import pygame


class Game:
    def __init__(self, _screen):
        self.game_array = None
        self.screen = _screen
        self.generation_count = 0

        self.size_of_pixel = 5
        self.width = self.screen.get_size()[0] // self.size_of_pixel
        self.height = self.screen.get_size()[1] // self.size_of_pixel

        self.running = True
        self.background_color = (0, 0, 0)
        self.cell_color = (255, 255, 255)

        self.setup_start_array()

    def run(self):
        # main loop
        while self.running:
            screen.fill(self.background_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.calculate_new_generation()
                    print(f"generation number: {self.generation_count}")

            self.print_game_array()
            pygame.display.update()

    def setup_start_array(self):
        self.game_array = (np.random.default_rng().random((self.height, self.width)) + 0.4).astype(np.byte)
        # self.game_array = np.zeros((self.height, self.width), np.uint8)
        # self.game_array[0][0] = 1
        # self.game_array[0][1] = 1
        # self.game_array[0][2] = 1
        # self.game_array[1][0] = 1
        # self.game_array[2][1] = 1

    def print_game_array(self):
        for i, row in enumerate(self.game_array):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.cell_color,
                                     pygame.Rect(j * self.size_of_pixel, i * self.size_of_pixel, self.size_of_pixel,
                                                 self.size_of_pixel))

    def calculate_neighbors(self):
        (w, h) = (self.width, self.height)
        neighbors = np.zeros((h, w), np.uint8)

        for i in range(1, h - 1):
            for j in range(1, w - 1):
                neighbors[i][j] = self.game_array[i + 1][j - 1] + self.game_array[i + 1][j] + self.game_array[i + 1][
                    j + 1] + self.game_array[i][j - 1] + self.game_array[i][j + 1] + self.game_array[i - 1][j - 1] + \
                                  self.game_array[i - 1][j] + self.game_array[i - 1][j + 1]

            # left
            neighbors[i][0] = (
                    self.game_array[i - 1][w - 1] + self.game_array[i - 1][0] + self.game_array[i - 1][1]
                    + self.game_array[i][w - 1] + self.game_array[i][1] +
                    self.game_array[i + 1][w - 1] + self.game_array[i + 1][0] + self.game_array[i + 1][1])
            # right
            neighbors[i][w - 1] = (
                    self.game_array[i - 1][w - 2] + self.game_array[i - 1][w - 1] +
                    self.game_array[i - 1][0]
                    + self.game_array[i][w - 2] + self.game_array[i][0] +
                    self.game_array[i + 1][w - 2] + self.game_array[i + 1][w - 1] +
                    self.game_array[i + 1][0])

        for i in range(1, w - 1):
            # up
            neighbors[0][i] = (
                    self.game_array[h - 1][i - 1] + self.game_array[h - 1][i] + self.game_array[h - 1][i + 1] +
                    self.game_array[0][i - 1] + self.game_array[0][i + 1] + self.game_array[1][i - 1] +
                    self.game_array[1][i] + self.game_array[1][i + 1])
            # down
            neighbors[h - 1][i] = (
                    self.game_array[h - 2][i - 1] + self.game_array[h - 2][i] + self.game_array[h - 2][i + 1] +
                    self.game_array[h - 1][i - 1] + self.game_array[h - 1][i + 1] + self.game_array[0][i - 1] +
                    self.game_array[0][i] + self.game_array[0][i + 1])

        neighbors[0][0] = (self.game_array[h - 1][w - 1] + self.game_array[h - 1][0] +
                           self.game_array[h - 1][1] + self.game_array[0][w - 1] +
                           self.game_array[0][1] +
                           self.game_array[1][w - 1] + self.game_array[1][0] + self.game_array[1][1])
        neighbors[h - 1][0] = \
            (self.game_array[h - 2][w - 1] + self.game_array[h - 2][0] +
             self.game_array[h - 2][1]
             + self.game_array[h - 1][w - 1] + self.game_array[h - 1][1] +
             self.game_array[0][w - 1] + self.game_array[0][0] + self.game_array[0][1])
        neighbors[0][w - 1] = \
            (self.game_array[h - 1][w - 2] + self.game_array[h - 1][w - 1] +
             self.game_array[h - 1][0]
             + self.game_array[0][w - 2] + self.game_array[0][0] +
             self.game_array[1][w - 2] + self.game_array[1][w - 1] + self.game_array[1][0])
        neighbors[h - 1][w - 1] = \
            (self.game_array[h - 2][w - 2] + self.game_array[h - 2][w - 1] +
             self.game_array[h - 2][0]
             + self.game_array[h - 1][w - 2] + self.game_array[h - 1][0] +
             self.game_array[0][w - 2] + self.game_array[0][w - 1] + self.game_array[0][0])
        return neighbors

    def calculate_new_generation(self):
        self.generation_count += 1
        (w, h) = (self.width, self.height)
        neighbors = self.calculate_neighbors()

        for i in range(h):
            for j in range(w):
                if self.game_array[i][j] == 1 and (neighbors[i][j] == 3 or neighbors[i][j] == 2):  # before /
                    self.game_array[i][j] = 1
                elif self.game_array[i][j] == 0 and neighbors[i][j] == 3:  # after /
                    self.game_array[i][j] = 1
                else:
                    self.game_array[i][j] = 0


if __name__ == '__main__':
    pygame.init()
    disp_size = (800, 600)
    screen = pygame.display.set_mode(disp_size)

    Game(screen).run()
    pygame.quit()
    exit()
