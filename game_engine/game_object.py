import pygame

class GameObject:
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color

    def resize(self, s):
        return None

    def draw(self, screen):
        return None

    def collide(self, e):
        return None
    
    def collision(self):
        print("collided")
        return None

class Rect(GameObject):
    def __init__(self, pos, size, color):
        super().__init__(pos, size, color)
        self.x, self.y, self.w, self.h = 0, 0, 0, 0

    def resize(self, s):
        self.x, self.y = round(self.pos[0] * s[0]), round(self.pos[1] * s[1])
        self.w, self.h = round(self.size[0] * s[0]), round(self.size[1] * s[1])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

    def collide(self, e):
        if self.x <= e[0] <= self.x + self.w:
            if self.y <= e[1] <= self.y + self.h:
                return True
        
        return None

class TextRect(Rect):
    def __init__(self, pos, size, color, msg, font_size, font_color):
        super().__init__(pos, size, color, )
        self.msg = msg
        self.font_size = font_size
        self.font_color = font_color
        self.x, self.y, self.w, self.h = 0, 0, 0, 0

    def resize(self, s):
        old_x, old_y = self.x, self.y
        
        super().resize(s)

        if old_x + old_y != 0:
            self.font_size = round(self.font_size * (self.x/old_x + self.y/old_y) / 2)
    
    def draw(self, screen):
        Rect.draw(self, screen)
        font = pygame.font.SysFont(None, self.font_size)
        text = font.render(self.msg, True, self.font_color)
        text_rect = text.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        screen.blit(text, text_rect)

class Circle(GameObject):
    def __init__(self, pos, size, color):
        super().__init__(pos, size, color)
        self.x, self.y, self.r = 0, 0, 0

    def resize(self, s):
        self.x, self.y = round(self.pos[0] * s[0]), round(self.pos[1] * s[1])
        self.r = round(self.size[0] * s[0]) + round(self.size[1] * s[1]) // 2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def collide(self, e):
        dist = ((self.x - e[0]) ** 2 + (self.y - e[1]) ** 2) ** 0.5
        if dist <= self.r:
            return True
        
        return None