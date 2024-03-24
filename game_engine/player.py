class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.territories = []

    def troops(self):
        return sum(self.territories.troops)