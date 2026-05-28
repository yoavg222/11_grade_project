import pygame


class Game:
    def __init__(self,network):
        pygame.init()
        self.network = network
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 570
        self.BLUE = (0, 0, 128)
        self.GRID_SIZE = 10
        self.CELL_SIZE = 40
        self.START_Y = 125
        self.LINE_COLOR = (200, 200, 200)
        self.START_X_LEFT = 50
        self.START_X_RIGHT = 500
        self.TEXT_COLOR = (255, 255, 255)
        self.ABC = "ABCDEFGHIJ"
        self.server_msg = ""

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 30, bold=True)

        self.background_img = pygame.transform.scale(pygame.image.load(r"C:\Users\user\Downloads\final_img.png"),
                                                     (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.submarine_img = pygame.transform.scale(pygame.image.load(r"C:\Users\user\Downloads\submarine.png"),
                                                    (self.CELL_SIZE, self.CELL_SIZE))

        self.user_input = ""
        self.finish = False
        pygame.mouse.set_visible(True)

    def is_valid_input(self, user_input):
        if len(user_input) < 2 or len(user_input) > 3: return False
        letter = user_input[0].upper()
        number_str = user_input[1:]
        if letter not in self.ABC or not number_str.isdigit(): return False
        number = int(number_str)
        return 1 <= number <= 10

    def draw_grid(self):
        for i in range(self.GRID_SIZE + 1):
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.START_X_LEFT + i * self.CELL_SIZE, self.START_Y),
                             (self.START_X_LEFT + i * self.CELL_SIZE, self.START_Y + self.GRID_SIZE * self.CELL_SIZE),
                             2)
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.START_X_LEFT, self.START_Y + i * self.CELL_SIZE),
                             (self.START_X_LEFT + self.GRID_SIZE * self.CELL_SIZE, self.START_Y + i * self.CELL_SIZE),
                             2)
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.START_X_RIGHT + i * self.CELL_SIZE, self.START_Y),
                             (self.START_X_RIGHT + i * self.CELL_SIZE, self.START_Y + self.GRID_SIZE * self.CELL_SIZE),
                             2)
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.START_X_RIGHT, self.START_Y + i * self.CELL_SIZE),
                             (self.START_X_RIGHT + self.GRID_SIZE * self.CELL_SIZE, self.START_Y + i * self.CELL_SIZE),
                             2)

    def run(self):
        while not self.finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.is_valid_input(self.user_input):
                            print(f"Selected: {self.user_input}")
                        self.user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += event.unicode.upper()

            self.screen.fill(self.BLUE)
            self.screen.blit(self.background_img, (0, 0))
            self.draw_grid()

            you_text = self.title_font.render("YOU", True, self.TEXT_COLOR)
            rival_text = self.title_font.render("RIVAL", True, self.TEXT_COLOR)

            self.screen.blit(you_text, (self.START_X_LEFT + (self.GRID_SIZE * self.CELL_SIZE // 2) - 30, 50))
            self.screen.blit(rival_text, (self.START_X_RIGHT + (self.GRID_SIZE * self.CELL_SIZE // 2) - 40, 50))

            for i in range(self.GRID_SIZE):
                num_surf = self.font.render(str(i + 1), True, self.TEXT_COLOR)
                self.screen.blit(num_surf, (self.START_X_LEFT - 25, self.START_Y + i * self.CELL_SIZE + 10))
                self.screen.blit(num_surf, (self.START_X_RIGHT - 25, self.START_Y + i * self.CELL_SIZE + 10))
                let_surf = self.font.render(self.ABC[i], True, self.TEXT_COLOR)
                self.screen.blit(let_surf, (self.START_X_LEFT + i * self.CELL_SIZE + 15, self.START_Y - 30))
                self.screen.blit(let_surf, (self.START_X_RIGHT + i * self.CELL_SIZE + 15, self.START_Y - 30))

            input_surf = self.font.render(f"Input: {self.user_input}", True, (255, 255, 0))
            self.screen.blit(input_surf, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()