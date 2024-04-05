from game_engine.game_object import Background, TextCircle
class Profile(TextCircle):
    def __init__(self, pos, size, color, msg, font_size, font_color, player):
        super().__init__(pos, size, color, msg, font_size, font_color)
        self.player = player
    
    def collision(self):
        return "Profile," + self.player.name

class Footer:
    def __init__(self, players):
        self.background = Background((0, 0.8), (0.7, 0.2), (211, 211, 211))
        self.player_profiles = []
        i = 0.1
        for p in players:
            pos = (i, 0.9)
            size = (0.035, 0.035)
            color = p.color
            msg = str(p.troops())
            profile = Profile(pos, size, color, msg, 35, (0, 0, 0), p)
            self.player_profiles.append(profile)
            i += 0.1

    def update(self):
        for p in self.player_profiles:
            p.msg = str(p.player.troops())