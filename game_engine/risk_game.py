import random as rd
import os
from game_engine.game_scene import GameScene
from game_engine.world import Map
from game_engine.footer import Footer

class RiskGame(GameScene):
    def __init__(self, size, filename, logname, players):
        super().__init__(size, (255, 255, 255))
        # stateNum: turn, player, stage, logid
        self.stateNum = [0, 0, 0, 0]


        self.players = players
        self.logname = os.path.abspath('data_files\\' + logname)
        self.map = Map(filename)
        for t in self.map.territories:
            self.add_object(t)

        rng = [i for i in range(len(self.players))]
        for t in self.map.territories:
            if len(rng) == 0:
                rng = [i for i in range(len(self.players))]
            i = rd.choice(rng)
            t.owner = self.players[i]
            self.players[i].territories.append(t)
            t.edit_troops(1)
            rng.remove(i)

        self.forces = [20 for player in self.players]
        
        self.footer = Footer(players)
        self.add_object(self.footer.background)
        for p in self.footer.player_profiles:
            self.add_object(p)
        
        self.auto_initial_reinforce()
          
    def add_object(self, obj):
        return super().add_object(obj)
    
    def resize(self, width, height):
        return super().resize(width, height)
    
    def collide(self, pos):
        with open(self.logname, 'a') as log_file:
            for obj in self.objects:
                if obj.collide(pos):
                    clog = obj.collision()
                    data = str(self.stateNum) + " " + clog + "\n"
                    print(data, end="")
                    if self.stateNum[0] == 0:
                        if self.initial_reinforce(clog) == 1:
                            log_file.write(data)
                            self.stateNum[3] += 1
                            self.stateNum[1] += 1
                            self.stateNum[1] %= len(self.players)
     
    def draw(self):
        return super().draw()

    def run(self):
        return super().run()
    
    def initial_reinforce(self, log):
        if sum(self.forces) <= 0:
            self.stateNum[0] == 1
            return 2
        
        slog = log.split(',')
        player = self.stateNum[1]
        owner = slog[1]

        if self.players[player].name != owner:
            return -1
        
        territory = slog[0]
        
        for t in self.map.territories:
            if t.name == territory:
                t.edit_troops(1)
                self.forces[player] -= 1
                self.footer.update()
                return 1
        
        return -1

    def auto_initial_reinforce(self):
        l = len(self.map.territories)
        while sum(self.forces) > 0:
            t = self.map.territories[rd.randint(0, l-1)]
            p = self.players.index(t.owner)
            if self.forces[p] > 0:
                t.edit_troops(1)
                self.forces[p] -= 1
        self.stateNum[0] = 1
        self.footer.update()