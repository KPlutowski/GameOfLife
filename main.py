import cProfile
import pstats

import numpy as np
import pygame


class Game:
    def __init__(self, ):
        pygame.display.set_caption('Game Of Life')
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)

        # self.display_size = (1920, 1080)
        self.display_size = (800, 600)

        self.screen = pygame.display.set_mode(self.display_size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

        self.cell_size = 1
        self.width = self.display_size[0] // self.cell_size
        self.height = self.display_size[1] // self.cell_size
        self.surface_to_draw = pygame.Surface((self.width, self.height))  # const size like self.game_array

        self.game_array = None
        self.generation_count = 0

        self.running = True
        self.pause = False
        self.background_color = (0, 0, 0)
        self.cell_color = (255, 255, 255)
        self.color_value = self.cell_color[0] * 256 ** 2 + self.cell_color[1] * 256 + self.cell_color[2]

        self.random_seed = np.random.default_rng(2137)
        self.probability_of_white = 0.3
        self.setup_start_array()

        self.max_fps = 30
        self.clock = pygame.time.Clock()

    def run(self):
        # main loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.setup_start_array()
                    elif event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                    elif event.key == pygame.K_RIGHT:
                        if self.pause:
                            # self.calculate_new_generation()
                            # self.print_game_array(self.screen)
                            self.next_frame()
                    elif event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size,
                                                          pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                    # self.width = self.screen.get_size()[1] // self.cell_size
                    # self.height = self.screen.get_size()[0] // self.cell_size
                    # self.setup_start_array()

            if self.pause:
                pygame.time.wait(1)
            else:
                self.next_frame()



    def next_frame(self):
        self.calculate_new_generation()
        self.print_game_array(self.screen)



        self.screen.blit(pygame.transform.scale(self.surface_to_draw, self.screen.get_rect().size), (0, 0))
        pygame.display.flip()

        self.clock.tick(self.max_fps)
        print(self.clock.get_fps())

    def setup_start_array(self):
        self.game_array = (self.random_seed.random((self.width, self.height)) + self.probability_of_white).astype(
            np.byte)
        # self.game_array = np.zeros(( self.width,self.height), np.uint8)
        # self.game_array[0][0] = 1
        # self.game_array[0][1] = 1
        # self.game_array[0][2] = 1
        # self.game_array[1][0] = 1
        # self.game_array[2][1] = 1

    def print_game_array(self, _screen):
        # start_timer = pygame.time.get_ticks()

        while self.screen.get_locked():
            self.screen.unlock()

        surface_array = pygame.surfarray.pixels2d(self.surface_to_draw)
        surface_array[:] = np.multiply.outer(self.game_array, self.color_value)

        # end_timer = pygame.time.get_ticks()
        # print(end_timer-start_timer)

    def calculate_new_generation(self):
        # start_timer = pygame.time.get_ticks()

        # Pad the game array to handle boundary conditions
        padded_game_array = np.pad(self.game_array, 1, mode='wrap')
        neighbor_count = (
                padded_game_array[:-2, :-2] + padded_game_array[:-2, 1:-1] + padded_game_array[:-2, 2:] +
                padded_game_array[1:-1, :-2] + padded_game_array[1:-1, 2:] +
                padded_game_array[2:, :-2] + padded_game_array[2:, 1:-1] + padded_game_array[2:, 2:]
        )
        # Apply game rules
        born_cells = (neighbor_count == 3)
        survive_cells = np.logical_and(self.game_array, np.isin(neighbor_count, [2, 3]))
        self.game_array = np.array(born_cells | survive_cells, dtype=np.uint8)

        # end_timer = pygame.time.get_ticks()
        # print(end_timer-start_timer)


def main():
    pygame.init()
    Game().run()
    pygame.quit()


if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
    stats.dump_stats('profile_results.prof')
    exit()
