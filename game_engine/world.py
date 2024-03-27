import json, os
from game_engine.game_object import Circle

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
        #rev_connections = [(connection[1], connection[0]) for connection in connections_data]
    #return connections + rev_connections
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

class Territory(Circle):
    def __init__(self, pos, size, color, name, continent, connections):
        super().__init__(pos, size, color)
        self.name = name
        self.continent = continent
        self.connections = connections
        self.owner = None
        self.troops = 0

    def edit_troops(self, n):
        self.troops += n
    
    def resize(self, s):
        return super().resize(s)
    
    def draw(self, screen):
        return super().draw(screen)
    
    def collide(self, e):
        return super().collide(e)

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

def test():
    m = Map('setup.json')
    print(m.territories)
    print(m.continents)