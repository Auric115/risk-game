import pygame, sys
from game_engine.game_scene import GameScene
from game_engine.game_object import TextRect

class StartMenu(GameScene):
    def __init__(self, objects=[]):
        super().__init__((500, 500))
        
        self.startButton = StartMenuButton((0.2, 0.80), (0.6, 0.1), (255, 255, 255), "Start Game", 30, (0, 0, 0))
        self.add_object(self.startButton)
        self.startButton.resize(self.size)
        
        title = TextRect((0.2, 0.02), (0.6, 0.1), (0, 0 , 0), "Risk", 50, (255, 255, 255))
        self.add_object(title)
        title.resize(self.size)
        
        # 0: start button, 2: title, 3+ : players
        for obj in objects:
            self.add_object(obj)
            obj.resize(self.size)

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
    
    def players(self):
        players = []
        for i in range(2, len(self.objects)):
            players.append(self.objects[i].active)
        return players
        
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
