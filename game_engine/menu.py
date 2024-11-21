from game_engine.game_object import Background, Rect
class Menu:
    def __init__(self):
        self.background = Background((0.7, 0), (0.3, 1), (111, 111, 111))

        self.tabs = [Rect((0.7, 0),(0.1, 0.05), (0, 0, 255), "Reinforce"),
                     Rect((0.8, 0),(0.1, 0.05), (255, 0, 0), "Attack"),
                     Rect((0.9, 0),(0.1, 0.05), (128, 0, 128), "Fortify")]

        self.attack_roll = [0, 0, 0]
        self.attack_dice = [Rect((0.71, 0.4), (0.08, 0.14222), (255, 0, 0), str(self.attack_roll[0]),90),
                            Rect((0.81, 0.4), (0.08, 0.14222), (255, 0, 0), str(self.attack_roll[1]),90),
                            Rect((0.91, 0.4), (0.08, 0.14222), (255, 0, 0), str(self.attack_roll[2]),90)]
        self.defend_roll = [0, 0]
        self.defend_dice = [Rect((0.71, 0.58), (0.08, 0.14222), (0, 0, 255), str(self.defend_roll[0]),90),
                            Rect((0.81, 0.58), (0.08, 0.14222), (0, 0, 255), str(self.defend_roll[1]),90)]
        
        self.roll_button = Rect((0.91, 0.615), (0.08, 0.07111), (128, 0, 128), "Roll", 45)
        self.next_button = Rect((0.8667, 0.9244), (0.1333, 0.0736), (128, 0, 128), "Next Phase", 40)