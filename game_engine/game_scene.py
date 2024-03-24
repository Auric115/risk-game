import pygame, sys

class GameScene:
    def __init__(self, size):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        pygame.display.set_caption("Risk Game by BJ Anderson")
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)
        obj.resize(self.size)

    def resize(self, width, height):
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        for obj in self.objects:
            obj.resize(self.size)

    def collide(self, pos):
        for obj in self.objects:
            if obj.collide(pos):
                obj.collision()

    def draw(self):
        for obj in self.objects:
            obj.draw(self.screen)

    def run(self):
        while True:
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