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

        self.cell_size = 2
        self.width = self.display_size[0] // self.cell_size
        self.height = self.display_size[1] // self.cell_size
        self.surface_to_draw = pygame.Surface((self.width, self.height))  # const size like self.game_array

        self.game_array = None
        self.generation_count = 0
        self.life_amount = 0

        self.running = True
        self.pause = False
        self.info_display = True
        self.background_color = (0, 0, 0)
        self.cell_color = (255, 255, 255)
        self.color_value = self.cell_color[0] * 256 ** 2 + self.cell_color[1] * 256 + self.cell_color[2]

        self.text_color = (0, 0, 0)
        self.outline_color = (255, 255, 255)

        self.random_seed = np.random.default_rng(2137)
        self.probability_of_white = 0.3
        self.setup_start_array()

        self.max_fps = 30
        self.clock = pygame.time.Clock()
        # pygame.font.SysFont('arial', size)
        self.font = pygame.font.SysFont('arial', 15)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.turn_off()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.reset_generation()
                    elif event.key == pygame.K_SPACE:
                        self.toggle_pause()
                    elif event.key == pygame.K_RIGHT and self.pause:
                        self.next_frame()
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_i:
                        self.toggle_info()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.turn_off()
                elif event.type == pygame.VIDEORESIZE:
                    self.handle_video_resize(event)

            if self.pause:
                pygame.time.wait(100)
            else:
                self.next_frame()

    def print_info(self):
        while self.screen.get_locked():
            self.screen.unlock()
        offset = 10
        height = self.font.get_height()
        self.print_text(offset, offset + height * 0, 'frames per sec:  ' + str(int(self.clock.get_fps())))
        self.print_text(offset, offset + height * 1, 'life amount:     ' + str(int(self.life_amount)))
        self.print_text(offset, offset + height * 2, 'generation nr:   ' + str(int(self.generation_count)))

        self.print_text(offset, offset + height * 3, 'info on/off:  i')
        self.print_text(offset, offset + height * 4, 'full screen:  f')
        self.print_text(offset, offset + height * 5, 'new breed:  n')
        self.print_text(offset, offset + height * 6, 'pause:  SPACE')
        self.print_text(offset, offset + height * 7, 'next generation:  right arrow')
        self.print_text(offset, offset + height * 8, 'exit:  ESC')

    def print_text(self, x, y, text_to_render):
        outline_render = self.font.render(text_to_render, True, self.outline_color)
        text_render = self.font.render(text_to_render, True, self.text_color)

        outline_thickness = 2
        w = text_render.get_width() + outline_thickness * 2
        h = text_render.get_height() + outline_thickness * 2

        outline_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        outline_surface.fill((0, 0, 0, 0))

        # Blit the outline with different offsets for each direction
        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                if abs(dx) == outline_thickness or abs(dy) == outline_thickness:
                    outline_surface.blit(outline_render, (dx + outline_thickness, dy + outline_thickness))

        # Blit the text onto the target surface
        outline_surface.blit(text_render, (outline_thickness, outline_thickness))

        # Blit the outline onto the surface
        self.screen.blit(outline_surface, (x, y))

    def next_frame(self):
        self.clock.tick(self.max_fps)

        self.calculate_new_generation()
        self.print_game_array()

        if self.info_display:
            self.print_info()

        pygame.display.flip()

    def reset_generation(self):
        self.generation_count = 0
        self.setup_start_array()
        self.next_frame()

    def setup_start_array(self):
        self.game_array = (self.random_seed.random((self.width, self.height)) + self.probability_of_white).astype(
            np.byte)
        # self.game_array = np.zeros(( self.width,self.height), np.uint8)
        # self.game_array[0][0] = 1
        # self.game_array[0][1] = 1
        # self.game_array[0][2] = 1
        # self.game_array[1][0] = 1
        # self.game_array[2][1] = 1

    def print_game_array(self):
        while self.screen.get_locked():
            self.screen.unlock()

        surface_array = pygame.surfarray.pixels2d(self.surface_to_draw)
        surface_array[:] = np.multiply.outer(self.game_array, self.color_value)

        self.screen.blit(pygame.transform.scale(self.surface_to_draw, self.screen.get_rect().size), (0, 0))

    def calculate_new_generation(self):
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

        self.generation_count += 1
        self.life_amount = self.game_array.sum()

    def handle_video_resize(self, event):
        self.screen = pygame.display.set_mode(event.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    def turn_off(self):
        self.running = False

    def toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()

    def toggle_pause(self):
        self.pause = not self.pause

    def toggle_info(self):
        self.info_display = not self.info_display


def main():
    pygame.init()
    Game().run()
    pygame.quit()


if __name__ == '__main__':
    main()
    exit()
