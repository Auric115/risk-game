import json, os, pygame
from game_engine.game_object import TextCircle, Line

def get_continents(filename):
    with open(os.path.abspath('data_files\\' + filename ), 'r') as file:
        data = json.load(file)
        continents_data = data.get('continents', {})
        continents = {continent: tuple(color) for continent, color in continents_data.items()}
    return continents

def get_continent_troops(filename):
    with open(os.path.abspath('data_files\\' + filename ), 'r') as file:
        data = json.load(file)
        continents_data = data.get('continent_troops', {})
        continents = {continent: num for continent, num in continents_data.items()}
    return continents

def get_territories(filename):
    with open(os.path.abspath('data_files\\' + filename ), 'r') as file:
        data = json.load(file)
        territories_data = data.get('territories', {})
        territories = {territory: tuple(coords) for territory, coords in territories_data.items()}
    return territories

def get_connections(filename):
    with open(os.path.abspath('data_files\\' + filename ), 'r') as file:
        data = json.load(file)
        connections_data = data.get('connections', [])
        connections = [tuple(connection) for connection in connections_data]
    return connections

def get_border_connections(filename):
    with open(os.path.abspath('data_files\\' + filename ), 'r') as file:
        data = json.load(file)
        connections_data = data.get('border_connections', [])
        connections = [tuple(connection) for connection in connections_data]
    return connections

def get_continent_mapping(filename):
    with open(os.path.abspath('data_files\\' + filename ), 'r') as file:
        data = json.load(file)
        continents_mapping = data.get('continents_mapping', {})
    return continents_mapping

class MapData:
    def __init__(self, filename):
        self.continents_setup = get_continents(filename)
        self.continent_troops_setup = get_continent_troops(filename)
        self.territories_setup = get_territories(filename)
        self.connections_setup = get_connections(filename)
        self.border_connections_setup = get_border_connections(filename)
        self.continent_mapping_setup = get_continent_mapping(filename)

    def generateTerritories(self):
        territories = []
        for name in self.territories_setup:
            pos = self.territories_setup[name]
            continent = self.continent_mapping_setup[name]
            color = self.continents_setup[continent]

            connections = []
            for c in self.connections_setup:
                if c[0] == name:
                    connections.append(c[1])
                if c[1] == name:
                    connections.append(c[0])
            
            territories.append(Territory(pos, (0.015, 0.015), color, name, continent, connections))
        
        return territories
    
    def generateLines(self):
        connections = []
        for c in self.connections_setup:
            border = False
            pos1 = self.territories_setup[c[0]]
            pos2 = self.territories_setup[c[1]]
            for bc in self.border_connections_setup:
                try: 
                    bc.index(c[0]) 
                    bc.index(c[1])

                    border = True
                except: 
                    continue
            if border:
                avg_y = (pos1[1] + pos2[1]) / 2
                pos3 = (0, avg_y)
                pos4 = (0.7, avg_y)
                if pos1[0] < pos2[0]:
                    connections.append(Line(pos1, pos3, (0, 0, 0), [c[0], c[1]]))
                    connections.append(Line(pos2, pos4, (0, 0, 0), [c[0], c[1]]))
                else:
                    connections.append(Line(pos1, pos4, (0, 0, 0), [c[0], c[1]]))
                    connections.append(Line(pos2, pos3, (0, 0, 0), [c[0], c[1]]))
            else:
                connections.append(Line(pos1, pos2, (0, 0, 0), [c[0], c[1]]))
        return connections
    
    def generateContinents(self, territories):
        continents = []
        for name in self.continents_setup:
            bonus_troops = self.continent_troops_setup[name]
            c_territories = []
            for t in territories:
                if t.name == name:
                    c_territories.append(t)
            continents.append(Continent(name, bonus_troops, territories))

        return continents

class Territory(TextCircle):
    def __init__(self, pos, size, color, name, continent, connections):
        super().__init__(pos, size, color, str(0), 30, (0,0,0))
        self.name = name
        self.continent = continent
        self.connections = connections
        self.owner = None
        self.troops = 0

    def edit_troops(self, n):
        self.troops += n
        self.msg = str(self.troops)
    
    def resize(self, s):
        return super().resize(s)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], 0.05), (self.x, self.y), self.r * 1.25, width=round(self.r*0.25))
        ccolor = (255, 255, 255)
        if self.owner is not None:
            ccolor = self.owner.color
        pygame.draw.circle(screen, ccolor, (self.x, self.y), self.r)
        font = pygame.font.SysFont(None, self.font_size)
        text = font.render(self.msg, True, self.font_color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def collide(self, e):
        return super().collide(e)
    
    def collision(self):
        self.log += ("Territory," + self.name + "," + self.owner.name + "," + str(self.troops))
        return super().collision()
    
    def attack(self, t):
        print(self.name, "attacks", t.name)
        return 2

    def fortify(self, t):
        print(self.name, "fortifies", t.name)
        return 2

class Continent:
    def __init__(self, name, bonus_troops, territories):
        self.name = name
        self.bonus_troops = bonus_troops
        self.territories = territories
    
    def is_conquered(self, player):
        return all(territory.owner == player for territory in self.territories)
    
class Map:
    def __init__(self, filename):
        map_data = MapData(filename)
        self.territories = map_data.generateTerritories()
        self.continents = map_data.generateContinents(self.territories)
        self.lines = map_data.generateLines()
