import random as rd
import os, pygame
from game_engine.game_scene import GameScene
from game_engine.world import Map
from game_engine.footer import Footer

class RiskGame(GameScene):
    def __init__(self, size, filename, logname, players):
        super().__init__(size, (255, 255, 255))
        # stateNum: turn, player, stage, logId
        self.stateNum = [0, 0, 0, 0]

        self.players = players
        self.num_players = len(self.players)
        self.logname = os.path.abspath('data_files\\' + logname)
        self.map = Map(filename)
        for l in self.map.lines:
            self.add_object(l)

        for t in self.map.territories:
            self.add_object(t)

        rng = [i for i in range(self.num_players)]
        for t in self.map.territories:
            if len(rng) == 0:
                rng = [i for i in range(self.num_players)]
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
        self.attack_src = None
        self.accessible = []
        self.fortify_src = None
          
    def add_object(self, obj):
        return super().add_object(obj)
    
    def resize(self, width, height):
        return super().resize(width, height)
    
    def collide(self, pos):
        with open(self.logname, 'a') as log_file:
            for obj in self.objects:
                if obj.collide(pos):
                    log = obj.collision()
                    data = str(self.stateNum) + " " + log + "\n"
                    log = log.split(',')
                    #print(data, end="")
                    #print(self.stateNum, log)
                    if self.stateNum[0] == 0: 
                    #if it is turn 0, initial reinforce
                        if log[0] == 'Territory':
                            res = self.initial_reinforce(log)

                            if res <= 0:
                                return
                            elif res == 1:
                                self.footer.update()
                                self.stateNum[1] += 1
                                self.stateNum[1] %= self.num_players
                                self.stateNum[3] += 1
                            elif res == 2:
                                self.stateNum = [1, 0, 0, 0] 
                        
                    else:
                    #otherwise go through turn cycle
                    # (calc forces) => reinforce => attack => fortify
                        if log[0] == 'Territory':
                            if self.stateNum[2] == 0: #calc forces
                                self.calc_forces(self.stateNum[1])
                                self.stateNum[2] += 1
                            if self.stateNum[2] <= 1: #reinforce
                                res = self.reinforce(log)
                                if res <= 0:
                                    return
                                elif res == 1:
                                    self.stateNum[3] += 1
                                elif res == 2:
                                    self.stateNum[2] += 1
                                    self.stateNum[3] += 1
                            elif self.stateNum[2] == 2: #attack
                                res = self.attack(log)
                                if res <= 0:
                                    return
                                else:
                                    self.stateNum[3] += 1
                                self.footer.update()
                            elif self.stateNum[2] == 3: #fortify
                                res = self.fortify(log)
                                if res <= 0:
                                    return
                                elif res == 1:
                                    self.stateNum[3] += 1;
                                elif res == 2:
                                    self.stateNum[1] += 1
                                    self.stateNum[2] = 0
                                    if self.stateNum[1] > self.num_players:
                                        self.stateNum = [self.stateNum[0] + 1, 0, 0, 0]
                        if log[0] == 'Profile':
                            if self.players[self.stateNum[1]].name == log[1]:
                                if self.stateNum[2] <= 1:
                                    print("Selecting cards")
                                elif self.stateNum[2] == 2:
                                    self.stateNum[2] += 1
                                    for l in self.map.lines:
                                        l.change_color((0, 0, 0))
                                    self.attack_src = None
                                elif self.stateNum[2] == 3:
                                    self.stateNum[1] += 1
                                    self.stateNum[2] = 0
                                    if self.stateNum[1] > self.num_players:
                                        self.stateNum = [self.stateNum[0] + 1, 0, 0, 0]
     
    def draw(self):
        return super().draw()

    def run(self):
        return super().run()
    
    def initial_reinforce(self, log):
        if sum(self.forces) <= 0:
            return 2
        
        player = self.stateNum[1]
        owner = log[2]

        if self.players[player].name != owner:
            return 0
        
        territory = log[1]

        for t in self.map.territories:
            if t.name == territory:
                t.edit_troops(1)
                self.forces[player] -= 1
                return 1

        return 0

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
    
    def calc_forces(self, p):
        self.forces[p] = len(self.players[p].territories) // 3
        for continent in self.map.continents:
                if continent.is_conquered(self.players[p]):
                    self.forces[p] += continent.bonus_troops
        self.forces[p] = max(3, self.forces[p])

    def reinforce(self, log):
        player = self.stateNum[1]
        owner = log[2]
        
        if self.players[player].name != owner:
            return 0
        
        territory = log[1]

        for t in self.players[player].territories:
            if t.name == territory:
                t.edit_troops(1)
                self.forces[player] -= 1
                self.footer.update()
                if self.forces[player] <= 0:
                    return 2
                return 1
               
        return 0
    
    def attack(self, log):
        player = self.stateNum[1]
        territory = log[1]
        owner = log[2]
        for t in self.map.territories:
            if t.name == territory:
                if self.players[player].name == owner:
                    self.attack_src = t
                    for l in self.map.lines:
                        if t.name in l.names:
                            l.change_color((255, 0, 0))
                        else:
                            l.change_color((0, 0, 0))
                    return 1
                else:
                    if self.attack_src is not None:
                        if self.attack_src.name in t.connections:
                            for l in self.map.lines:
                                l.change_color((0, 0, 0))
                            tmp = self.attack_src    
                            self.attack_src = None
                            res = tmp.attack(t)

                    for l in self.map.lines:
                        l.change_color((0, 0, 0))
                    self.attack_src = None
                    return res

    def search(self, territory, visited=None):
        if visited is None:
            visited = set()

        visited.add(territory)
        connected_territories = [territory]

        # Find the territory object corresponding to the given territory name
        territory_obj = None
        for t in self.players[self.stateNum[1]].territories:
            if t.name == territory:
                territory_obj = t
                break

        if territory_obj is None:
            return connected_territories  # No connected territories found

        for adjacent_territory_name in territory_obj.connections:
            if adjacent_territory_name not in visited:
                # Recursively search for connected territories
                connected_territories.extend(self.search(adjacent_territory_name, visited))

        return connected_territories

    def fortify(self, log):
        player = self.stateNum[1]
        owner = log[2]

        if self.players[player].name != owner:
            return 0
        
        territory = log[1]

        if self.fortify_src is None:
            linked = self.search(territory)
            for n in linked:
                for t in self.players[player].territories:
                    if t.name == territory:
                        self.fortify_src = t

                    if t.name == n:
                        self.accessible.append(n)
            
            for l in self.map.lines:
                if l.names[0] in self.accessible and l.names[1] in self.accessible:
                    l.change_color((255, 0, 0))
                else:
                    l.change_color((0, 0, 0))

            return 1
        else:
            print("check fortify", territory)
            print(self.accessible)
            for t in self.map.territories:
                if t.name == territory:
                    if t in self.accessible:
                        print("Fortified:", t.name)
                        if t != self.fortify_src:
                            tmp = self.fortify_src
                            self.fortify_src = None
                            res = tmp.fortify(t)
            for l in self.map.lines:
                l.change_color((0, 0, 0))

            return 2
