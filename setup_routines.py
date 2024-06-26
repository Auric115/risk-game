from game_engine.player import Player
from game_engine.start_menu import StartMenuButton
from colors import *

def init_players(n, names=False):
    player_colors = [LIGHT_BLUE, PINK, VIOLET, LIME_GREEN, MAROON, YELLOW, RED, ORANGE, GREEN, BLUE, PURPLE, BROWN]
    player_names = ['Eisenhower', 'Cleopatra', 'Alexander', 'Patton', 'Napoleon', 'Sun Tzu', 'Genghis Khan', 'Hannibal', 'Washington', 'Nelson', 'Attila', 'Caesar']

    players = []
    if not names:
        for i in range(n):
            players.append(Player(f"Player {i+1}", player_colors[i]))
    else:
        for i in range(n):
            players.append(Player(player_names[i], player_colors[i]))
    return players

def init_start_menu(players):
    # Calculate the number of rows and columns based on the number of players
    num_players = len(players)
    num_cols = int(num_players ** 0.5)
    num_rows = (num_players + num_cols - 1) // num_cols

    # Calculate the width and height of each rectangle
    w = 4.0 / ( 6 * num_cols + 1) 
    h = 4.0 / ( 11 * num_rows + 1)

    # Calculate the horizontal and vertical gap between rectangles
    x_gap = (0.8 - w * num_cols) / (num_cols + 1)
    y_gap = (0.8 - h * num_rows) / (num_rows + 1)

    rectangles = []

    for i, player in enumerate(players):
        # Calculate the row and column indices for the current player
        row = i // num_cols
        col = i % num_cols

        # Calculate the position of the top-left corner of the rectangle
        x = 0.1 + (col + 1) * x_gap + col * w
        y = 0.05 + (row + 1) * y_gap + row * h

        rect = StartMenuButton((x, y), (w, h), player.color, player.name, 30, (0, 0, 0))     

        rectangles.append(rect)

    return rectangles
