class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.territories = []

    def troops(self):
        total = 0
        for t in self.territories:
            total += t.troops
        return total