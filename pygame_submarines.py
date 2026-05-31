import pygame
from constants import DELIMITER, TUR, MIS, HIT, ATT


class Game:
    def __init__(self, network):
        pygame.init()
        self.network = network

        # הגדרות חלון ומסכים
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

        # אתחול תצוגה וגופנים
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 30, bold=True)

        # מצב המשחק ומידע
        self.my_choices = []
        self.my_hits = []
        self.my_misses = []
        self.rival_hits = []
        self.game_phase = "PLACING"
        self.my_turn = False
        self.last_attack_was_mine = False
        self.winner_message = ""

        # טעינת תמונות
        self.background_img = pygame.transform.scale(
            pygame.image.load(r"C:\Users\user\Downloads\final_img.png"),
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )
        self.submarine_img = pygame.transform.scale(
            pygame.image.load(r"C:\Users\user\Downloads\submarine.png"),
            (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.destroy_submarine = pygame.transform.scale(
            pygame.image.load(r"C:\Users\user\Downloads\submarine_destroy.png"),
            (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.x_img = pygame.transform.scale(
            pygame.image.load(r"C:\Users\user\Downloads\red_x.png"),
            (self.CELL_SIZE, self.CELL_SIZE)
        )

        self.user_input = ""
        self.finish = False
        self.network.sock.settimeout(0.01)

    def is_valid_input(self, user_input):
        if len(user_input) < 2 or len(user_input) > 3:
            return False

        letter = user_input[0].upper()
        number_str = user_input[1:]

        if letter not in self.ABC or not number_str.isdigit():
            return False

        return 1 <= int(number_str) <= 10

    def get_coords(self, cell_str, is_rival):
        letter = cell_str[0].upper()
        number = int(cell_str[1:])
        col = self.ABC.index(letter)
        row = number - 1

        x = (self.START_X_RIGHT if is_rival else self.START_X_LEFT) + (col * self.CELL_SIZE)
        y = self.START_Y + (row * self.CELL_SIZE)
        return x, y

    def run(self):
        while not self.finish:
            # --- טיפול באירועים (Events) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True

                if event.type == pygame.KEYDOWN and self.winner_message == "":
                    if event.key == pygame.K_RETURN:
                        # שלב מיקום הצוללות
                        if self.game_phase == "PLACING":
                            if self.is_valid_input(self.user_input):
                                self.my_choices.append(self.user_input)
                                self.user_input = ""  # איפוס הקלט לאחר הזנה מוצלחת

                                if len(self.my_choices) == 3:
                                    self.network.send_with_size("PIC" + DELIMITER + DELIMITER.join(self.my_choices))
                                    self.game_phase = "ATTACKING"

                        # שלב התקיפה
                        elif self.game_phase == "ATTACKING" and self.my_turn:
                            if self.is_valid_input(self.user_input):
                                self.network.send_with_size(f"{ATT}{DELIMITER}{self.user_input}")
                                self.last_attack_was_mine = True
                                self.my_turn = False
                                self.user_input = ""

                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += event.unicode.upper()

            # --- תקשורת וקבלת הודעות מהשרת ---
            try:
                msg = self.network.recv_by_size()
                if msg:
                    data = msg.decode().split(DELIMITER)

                    if data[0] == HIT:
                        if data[1] in self.my_choices:
                            # היריב פגע בי
                            self.rival_hits.append(data[1])
                        else:
                            # אני פגעתי ביריב - מתעדכן רק אם אני זה שתקפתי
                            if self.last_attack_was_mine:
                                self.my_hits.append(data[1])
                                self.last_attack_was_mine = False

                    elif data[0] == MIS:
                        # הוספת איקס רק לשחקן שתקף והחטיא באמת
                        if self.last_attack_was_mine:
                            self.my_misses.append(data[1])
                            self.last_attack_was_mine = False

                    elif data[0] == TUR:
                        self.my_turn = True
                        # ליתר ביטחון, כשמתחיל תור חדש, מאפסים את הגנת התקיפה האחרונה
                        self.last_attack_was_mine = False

                    elif data[0] == "WIN":
                        self.winner_message = "YOU WON!"
                        self.my_turn = False

                    elif data[0] == "LOS":
                        self.winner_message = "YOU LOST!"
                        self.my_turn = False
            except:
                pass

            # --- ציור וגרפיקה (Drawing) ---
            self.screen.fill(self.BLUE)
            self.screen.blit(self.background_img, (0, 0))

            # ציור רשתות המשחק (גריד)
            for i in range(11):
                for start_x in [self.START_X_LEFT, self.START_X_RIGHT]:
                    pygame.draw.line(self.screen, self.LINE_COLOR, (start_x + i * 40, self.START_Y),
                                     (start_x + i * 40, self.START_Y + 400), 2)
                    pygame.draw.line(self.screen, self.LINE_COLOR, (start_x, self.START_Y + i * 40),
                                     (start_x + 400, self.START_Y + i * 40), 2)

            # ציור אלמנטים על הלוח
            for pos in self.my_choices:
                self.screen.blit(self.submarine_img, self.get_coords(pos, False))
            for pos in self.rival_hits:
                self.screen.blit(self.destroy_submarine, self.get_coords(pos, False))
            for pos in self.my_hits:
                self.screen.blit(self.destroy_submarine, self.get_coords(pos, True))
            for pos in self.my_misses:
                self.screen.blit(self.x_img, self.get_coords(pos, True))

            # כותרות וטקסטים קבועים
            self.screen.blit(self.title_font.render("YOU", True, self.TEXT_COLOR), (200, 50))
            self.screen.blit(self.title_font.render("RIVAL", True, self.TEXT_COLOR), (650, 50))
            self.screen.blit(self.font.render(f"Input: {self.user_input}", True, (255, 255, 0)), (10, 10))

            # הודעת תור
            if self.my_turn and not self.winner_message:
                self.screen.blit(self.font.render("YOUR TURN!", True, (0, 255, 0)), (450, 10))

            # הודעת ניצחון / הפסד
            if self.winner_message:
                color = (0, 255, 0) if "WON" in self.winner_message else (255, 0, 0)
                self.screen.blit(self.title_font.render(self.winner_message, True, color), (430, 250))

            # ציור מספרי שורות ואותיות עמודות (A-J, 1-10)
            for i in range(10):
                self.screen.blit(self.font.render(str(i + 1), True, self.TEXT_COLOR),
                                 (self.START_X_LEFT - 25, self.START_Y + i * 40 + 10))
                self.screen.blit(self.font.render(str(i + 1), True, self.TEXT_COLOR),
                                 (self.START_X_RIGHT - 25, self.START_Y + i * 40 + 10))
                self.screen.blit(self.font.render(self.ABC[i], True, self.TEXT_COLOR),
                                 (self.START_X_LEFT + i * 40 + 15, self.START_Y - 30))
                self.screen.blit(self.font.render(self.ABC[i], True, self.TEXT_COLOR),
                                 (self.START_X_RIGHT + i * 40 + 15, self.START_Y - 30))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()