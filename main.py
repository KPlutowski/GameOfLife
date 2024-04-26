import cProfile
import pstats

import numpy as np
import pygame
from scipy.signal import convolve2d


class Game:
    def __init__(self, _screen):
        self.game_array = None
        self.screen = _screen
        self.generation_count = 0

        self.cell_size = 2
        self.width = self.screen.get_size()[0] // self.cell_size
        self.height = self.screen.get_size()[1] // self.cell_size
        self.alive_surface = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))

        self.running = True
        self.background_color = (0, 0, 0)
        self.cell_color = (255, 255, 255)

        self.setup_start_array()

        self.max_fps = 30
        self.clock = pygame.time.Clock()
        self.start_timer = pygame.time.get_ticks()

    def run(self):
        # main loop
        while self.running:
            screen.fill(self.background_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            # print(self.start_timer)
            # print(f"generation number: {self.generation_count}")

            self.calculate_new_generation()
            self.print_game_array(self.screen)
            pygame.display.update()

            self.clock.tick(self.max_fps)

    def setup_start_array(self):
        self.game_array = (np.random.default_rng().random((self.height, self.width)) + 0.4).astype(np.byte)
        # self.game_array = np.zeros((self.height, self.width), np.uint8)
        # self.game_array[0][0] = 1
        # self.game_array[0][1] = 1
        # self.game_array[0][2] = 1
        # self.game_array[1][0] = 1
        # self.game_array[2][1] = 1

    def print_game_array(self, _screen):
        alive_cells = np.argwhere(self.game_array == 1)
        cell_size = self.cell_size

        self.alive_surface.fill(self.background_color)

        # Draw all alive cells onto the alive surface
        for y, x in alive_cells:
            pygame.draw.rect(self.alive_surface, self.cell_color, (x * cell_size, y * cell_size, cell_size, cell_size))

        # Blit the alive surface onto the screen
        _screen.blit(self.alive_surface, (0, 0))

    def calculate_new_generation(self):
        self.generation_count += 1

        # Define the kernel for convolution
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.uint8)

        # Compute the convolution
        neighbors = convolve2d(self.game_array, kernel, mode='same', boundary='wrap')

        # Apply game rules
        alive_mask = (self.game_array == 1)
        neighbors_2_or_3 = (neighbors == 2) | (neighbors == 3)
        neighbors_3 = (neighbors == 3)

        self.game_array[alive_mask & neighbors_2_or_3] = 1
        self.game_array[~alive_mask & neighbors_3] = 1
        self.game_array[~(alive_mask & neighbors_2_or_3) & ~(~alive_mask & neighbors_3)] = 0


if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()

    pygame.init()
    disp_size = (800, 600)
    screen = pygame.display.set_mode(disp_size)
    Game(screen).run()
    pygame.quit()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
    stats.dump_stats('profile_results.prof')
    exit()
