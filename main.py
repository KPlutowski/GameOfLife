import pygame


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

    def run(self):

        # main loop
        while self.running:
            # screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    disp_size = (800, 600)
    screen = pygame.display.set_mode(disp_size)

    Game(screen).run()

    pygame.quit()
    exit()
