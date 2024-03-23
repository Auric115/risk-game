import pygame
import sys
import json

#Define retrieval functions for the setup
def get_territories(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        territories_data = data.get('territories', {})
        territories = {territory: tuple(coords) for territory, coords in territories_data.items()}
    return territories

def get_connections(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        connections_data = data.get('connections', [])
        connections = [tuple(connection) for connection in connections_data]
    return connections

def get_continent_mapping(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        continents_mapping = data.get('continents_mapping', {})
    return continents_mapping

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 675
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)
PINK = (255, 192, 203)
VIOLET = (238, 130, 238)
LIME_GREEN = (50, 205, 50)
MAROON = (128, 0, 0)
YELLOW = (255, 255, 0)

# Define continents and their color
continents = {
    'North America': RED,
    'South America': ORANGE,
    'Europe': BLUE,
    'Africa': BROWN,
    'Asia': GREEN,
    'Australia': PURPLE
}

#Define possible player colors
player_colors = [LIGHT_BLUE, PINK, VIOLET, LIME_GREEN, MAROON, YELLOW]

#Define territories and their locations
territories = get_territories('setup.json')
#Define connections between territories
connections = get_connections('setup.json')
# Assign territories to continents
continents_mapping = get_continent_mapping('setup.json')

# Define a dictionary to store numbers in each territory
territory_numbers = {territory: 0 for territory in territories}

# Define a dictionary to store colors of territory borders
territory_border_colors = {territory: BLACK for territory in territories}

# Define a dictionary to store troops count for each player
player_troops = {color: 0 for color in player_colors}

def round_tup(tup, r=1):
    return (round(tup[0] * r), round(tup[1] * r))

# Function to draw the start menu
def draw_start_menu(screen, ratio, num_players, player_color):
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, HEIGHT // 2 - 75, 200, 50))
    font = pygame.font.SysFont(None, round(48 * ratio))
    text = font.render("Start Game", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # Draw button for choosing number of players
    pygame.draw.rect(screen, player_colors[player_color], (WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50))
    font = pygame.font.SysFont(None, round(24 * ratio))
    text = font.render(f"Players: {num_players}", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45))
    screen.blit(text, text_rect)
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 + 20, 50, 50))
    font = pygame.font.SysFont(None, round(48 * ratio))
    text = font.render("-", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 - 125, HEIGHT // 2 + 42))
    screen.blit(text, text_rect)
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 + 100, HEIGHT // 2 + 20, 50, 50))
    font = pygame.font.SysFont(None, round(48 * ratio))
    text = font.render("+", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2 + 125, HEIGHT // 2 + 42))
    screen.blit(text, text_rect)

# Function to draw the sidebar menu
def draw_sidebar(screen, selected_tab):
    pygame.draw.rect(screen, BLACK, (WIDTH * 2/3, 0, WIDTH * 1/3, HEIGHT))  # Sidebar background
    
    tabs = ["Reinforce", "Attack", "Fortify"]
    tab_font = pygame.font.SysFont(None, 24)
    tab_loc = 15
    for i, tab in enumerate(tabs):
        text = tab_font.render(tab, True, WHITE if i != selected_tab else BLACK)
        text_rect = text.get_rect(x=(WIDTH * 2/3 + tab_loc), y=10)
        screen.blit(text, text_rect)
        tab_loc += 160

    # Display content based on selected tab
    content_font = pygame.font.SysFont(None, 32)
    content_text = content_font.render(tabs[selected_tab], True, WHITE)
    content_rect = content_text.get_rect(x=(WIDTH * 2/3 + 10), y=200)
    screen.blit(content_text, content_rect)

# Function to draw the footer menu
def draw_footer(screen, num_players, player_colors, player_troops, ratio):
    footer_height = 150
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - footer_height, WIDTH, footer_height))  # Footer background

    font = pygame.font.SysFont(None, round(24 * ratio))
    text_y = HEIGHT - footer_height + 10
    color_circles = []
    for i, color in enumerate(player_colors):
        if i < num_players:
            pygame.draw.circle(screen, color, (50 + i * 120, HEIGHT - footer_height // 2), 20)  # Draw player color circles
            text = font.render(f"{player_troops[color]} troops", True, WHITE)
            text_rect = text.get_rect(center=(50 + i * 120, text_y))
            screen.blit(text, text_rect)
            color_circles.append((50 + i * 120, HEIGHT - footer_height // 2))
    
    return color_circles
    
# Function to draw the map
def draw_map(screen, ratio):
    screen.fill(WHITE)

    for connection in connections:
        start_pos = territories[connection[0]]
        end_pos = territories[connection[1]]
        pygame.draw.line(screen, BLACK, round_tup(start_pos,ratio), round_tup(end_pos,ratio), 2)  # Draw connections

    for territory, pos in territories.items():
        pygame.draw.circle(screen, BLACK, round_tup(pos,ratio), round(20*ratio))  # Draw territory circles
        pygame.draw.circle(screen, continents[continents_mapping[territory]], round_tup(pos,ratio), round(15*ratio))  # Fill with continent color

        # Display territory numbers
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(territory_numbers[territory]), True, BLACK)
        text_rect = text.get_rect(center=round_tup(pos, ratio))
        screen.blit(text, text_rect)

        # Change territory border color
        pygame.draw.circle(screen, territory_border_colors[territory], round_tup(pos,ratio), round(20*ratio), width=4)  # Border color

# Function to handle window resizing
def handle_resize(screen, new_width, new_height):
    global WIDTH, HEIGHT
    ratio = ((new_width * 1.0) / (WIDTH * 1.0))
    WIDTH, HEIGHT = new_width, new_height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Adjust the screen size
    return ratio

# Function to handle territory clicks
def handle_territory_click(event_pos, ratio, player_color):
    for territory, pos in territories.items():
        distance = (((pos[0] * ratio) - event_pos[0]) ** 2 + ((pos[1] * ratio) - event_pos[1]) ** 2) ** 0.5
        if distance <= 20:  # If click is within the radius of a territory
            print(f"Clicked on territory: {territory}")
            # Add your logic for territory click handling here
            territory_numbers[territory] += 1  # Increment territory number
            territory_border_colors[territory] = player_colors[player_color]  # Change territory border color
            player_troops[player_colors[player_color]] += 1 
            break  # Break the loop if a territory is clicked

# Function to handle clicks on player colors in the footer menu
def handle_player_click(event_pos, ratio, player_color, color_circles):
    for i, circle in enumerate(color_circles):
        center_x, center_y = circle
        distance = ((center_x - event_pos[0]) ** 2 + (center_y - event_pos[1]) ** 2) ** 0.5
        if distance <= (15 * ratio):  # Radius of the color circle
            return i
    return player_color


# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Expand the width for sidebar
    pygame.display.set_caption("Risk Game by BJ Anderson")
    ratio = 1
    start_menu = True
    selected_tab = 0  # Default to first tab
    num_players = 2  # Default number of players
    player_color = 0
    color_circles = []

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_menu:
                    if event.button == 1:  # Left mouse button
                        # Check if clicked on number of players button
                        #(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50))
                        if WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100:
                            if HEIGHT // 2 - 75 <= event.pos[1] <= HEIGHT // 2 - 25:
                                start_menu = False
                            elif HEIGHT // 2 + 20 <= event.pos[1] <= HEIGHT // 2 + 70:                      
                                player_color += 1
                                if player_color > 5:
                                    player_color = 0
                        if HEIGHT // 2 + 20 <= event.pos[1] <= HEIGHT // 2 + 70: 
                            if WIDTH // 2 - 150 <= event.pos[0] <= WIDTH // 2 - 100:
                                num_players = max(2, num_players - 1)
                            elif WIDTH // 2 + 100 <= event.pos[0] <= WIDTH // 2 + 150:
                                num_players = min(6, num_players + 1)
                        
                else:
                    if WIDTH * 2/3 <= event.pos[0] <= WIDTH:  # Check if click is inside sidebar
                        if 0 <= event.pos[1] <= 21: #Check if click is inside tab space
                            selected_tab = (event.pos[0] - round((WIDTH * 2/3) - 15)) // 160
                    elif HEIGHT * (7/9) <= event.pos[1] <= HEIGHT:
                        player_color = handle_player_click(event.pos, ratio, player_color, color_circles)
                    else:
                        handle_territory_click(event.pos, ratio, player_color)
            # Handle window resizing
            elif event.type == pygame.VIDEORESIZE:
                ratio = handle_resize(screen, event.w, event.h)

        if start_menu:
            draw_start_menu(screen, ratio, num_players, player_color)
        else:
            draw_map(screen, ratio)
            color_circles = draw_footer(screen, num_players, player_colors, player_troops, ratio)
            draw_sidebar(screen, selected_tab)

        pygame.display.flip()

if __name__ == "__main__":
    main()
