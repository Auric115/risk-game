from game_engine.game_scene import GameScene
from game_engine.world import Map

class RiskGame(GameScene):
    def __init__(self, size, filename, players):
        super().__init__(size, (255, 255, 255))
        self.players = players
        self.map = Map(filename)
        for t in self.map.territories:
            self.add_object(t)

    def add_object(self, obj):
        return super().add_object(obj)
    
    def resize(self, width, height):
        return super().resize(width, height)
    
    def collide(self, pos):
        return super().collide(pos)
    
    def draw(self):
        return super().draw()
    
    def run(self):
        return super().run()