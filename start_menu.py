from game_engine.game_scene import *
from game_engine.game_object import *

class StartMenu(GameScene):
    def __init__(self, objects=[]):
        super().__init__((500, 500))
        
        for obj in objects:
            self.add_object(obj)
            obj.resize(self.size)
        
        self.startButton = StartMenuButton((0.2, 0.80), (0.6, 0.1), (255, 255, 255), "Start Game", 30, (0, 0, 0))
        self.add_object(self.startButton)
        self.startButton.resize(self.size)
        
        title = TextRect((0.2, 0.02), (0.6, 0.1), (0, 0 , 0), "Risk", 50, (255, 255, 255))
        self.add_object(title)
        title.resize(self.size)

    def run(self):
        while True:
            self.running = self.startButton.active
            if not self.running:
                pygame.display.quit()
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.collide(event.pos)

            self.draw()
            pygame.display.update()
        
class StartMenuButton(TextRect):
    def __init__(self, pos, size, color, msg, font_size, font_color):
        super().__init__(pos, size, color, msg, font_size, font_color)
        self.active = True

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.w, self.h))

        font = pygame.font.SysFont(None, self.font_size)
        text = font.render(self.msg, True, self.font_color)
        text_rect = text.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        screen.blit(text, text_rect)

    def collision(self):
        self.active = not self.active
        return self.active
        
def init_start_menu(players):
    # Calculate the number of rows and columns based on the number of players
    num_players = len(players)
    num_cols = int(num_players ** 0.5)
    num_rows = (num_players + num_cols - 1) // num_cols

    # Calculate the width and height of each rectangle
    w = 4.0 / ( 6 * num_cols + 1) 
    h = 4.0 / ( 11 * num_rows + 1)

    # Calculate the horizontal and vertical gap between rectangles
    x_gap = (0.8 - w * num_cols) / (num_cols + 1)
    y_gap = (0.8 - h * num_rows) / (num_rows + 1)

    rectangles = []

    for i, player in enumerate(players):
        # Calculate the row and column indices for the current player
        row = i // num_cols
        col = i % num_cols

        # Calculate the position of the top-left corner of the rectangle
        x = 0.1 + (col + 1) * x_gap + col * w
        y = 0.05 + (row + 1) * y_gap + row * h

        rect = StartMenuButton((x, y), (w, h), player.color, player.name, 30, (0, 0, 0))     

        rectangles.append(rect)

    return rectangles
