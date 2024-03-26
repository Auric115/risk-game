from game_engine.start_menu import StartMenuButton

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