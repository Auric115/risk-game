class Territory:
    def __init__(self, name, continent, pos):
        self.name = name
        self.continent = continent
        self.pos = pos
        self.owner = None
        self.troops = 0
    
    def edit_troops(self, n):
        self.troops += n

class Continent:
    def __init__(self, name, bonus_troops):
        self.name = name
        self.bonus_troops = bonus_troops
        self.territories = []
    
    def is_conquered(self, player):
        return all(territory.owner == player for territory in self.territories)