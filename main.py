import pygame
import sys

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

#Define territories and their locations
territories = {
    'Alaska': (70, 100),
    'Northwest Territory': (170, 100),
    'Greenland': (300, 70),
    'Alberta': (130, 160),
    'Ontario': (200, 160),
    'Quebec': (260, 160),
    'Western United States': (160, 220),
    'Eastern United States': (230, 220),
    'Central America': (190, 280),

    'Venezuela': (220, 340),
    'Peru': (190, 420),
    'Brazil': (280, 400),
    'Argentina': (240, 480),

    'Iceland': (360, 130),
    'Scandinavia': (420, 110),
    'Great Britain': (340, 190),
    'Northern Europe': (420, 200),
    'Western Europe': (360, 250),
    'Southern Europe': (440, 260),
    'Ukraine': (480, 180),

    'North Africa': (380, 360),
    'Egypt': (450, 320),
    'East Africa': (500, 380),
    'Congo': (430, 420),
    'South Africa': (450, 490),
    'Madagascar': (530, 460),

    'Ural': (560, 140),
    'Siberia': (620, 180),
    'Yakutsk': (680, 120),
    'Kamchatka': (740, 100),
    'Irkutsk': (680, 170),
    'Mongolia': (690, 230),
    'Japan': (750, 200),
    'Afghanistan': (550, 220),
    'Middle East': (520, 290),
    'India': (580, 320),
    'China': (640, 280),
    'Siam': (660, 330),

    'Indonesia': (660, 400),
    'New Guinea': (730, 390),
    'Western Australia': (680, 460),
    'Eastern Australia': (740, 440),
}


#Define connections between territories
connections = [
    ('Alaska', 'Northwest Territory'),
    ('Alaska', 'Alberta'),
    ('Northwest Territory', 'Greenland'),
    ('Northwest Territory', 'Alberta'),
    ('Northwest Territory', 'Ontario'),
    ('Greenland', 'Ontario'),
    ('Greenland', 'Quebec'),
    ('Greenland', 'Iceland'),
    ('Alberta', 'Ontario'),
    ('Alberta', 'Western United States'),
    ('Ontario', 'Quebec'),
    ('Ontario', 'Western United States'),
    ('Ontario', 'Eastern United States'),
    ('Quebec', 'Eastern United States'),
    ('Western United States', 'Central America'),
    ('Western United States', 'Eastern United States'),
    ('Eastern United States', 'Central America'),
    ('Central America', 'Venezuela'),
    
    ('Venezuela', 'Peru'),
    ('Venezuela', 'Brazil'),
    ('Peru', 'Brazil'),
    ('Peru', 'Argentina'),
    ('Brazil', 'Argentina'),
    ('Brazil', 'North Africa'),

    ('Iceland', 'Scandinavia'),
    ('Iceland', 'Great Britain'),
    ('Scandinavia', 'Great Britain'),
    ('Scandinavia', 'Northern Europe'),
    ('Scandinavia', 'Ukraine'),
    ('Great Britain', 'Northern Europe'),
    ('Great Britain', 'Western Europe'),
    ('Northern Europe', 'Western Europe'),
    ('Northern Europe', 'Southern Europe'),
    ('Northern Europe', 'Ukraine'),
    ('Western Europe', 'North Africa'),
    ('Western Europe', 'Southern Europe'),
    ('Southern Europe', 'North Africa'),
    ('Southern Europe', 'Egypt'),
    ('Southern Europe', 'Middle East'),
    ('Southern Europe', 'Ukraine'),
    ('Ukraine', 'Ural'),
    ('Ukraine', 'Afghanistan'),
    ('Ukraine', 'Middle East'),

    ('North Africa', 'Egypt'),
    ('North Africa', 'East Africa'),
    ('North Africa', 'Congo'),
    ('Egypt', 'East Africa'),
    ('Egypt', 'Middle East'),
    ('East Africa', 'Congo'),
    ('East Africa', 'South Africa'),
    ('East Africa', 'Madagascar'),
    ('East Africa', 'Middle East'),
    ('Congo', 'South Africa'),
    ('South Africa', 'Madagascar'),
    
    ('Ural', 'Siberia'),
    ('Ural', 'Afghanistan'),
    ('Ural', 'China'),
    ('Siberia', 'Yakutsk'),
    ('Siberia', 'Irkutsk'),
    ('Siberia', 'Mongolia'),
    ('Siberia', 'China'),
    ('Yakutsk', 'Kamchatka'),
    ('Yakutsk', 'Irkutsk'),
    ('Kamchatka', 'Irkutsk'),
    ('Kamchatka', 'Mongolia'),
    ('Kamchatka', 'Japan'),
    ('Irkutsk', 'Mongolia'),
    ('Mongolia', 'Japan'),
    ('Mongolia', 'China'),
    ('Afghanistan', 'Middle East'),
    ('Afghanistan', 'India'),
    ('Afghanistan', 'China'),
    ('Middle East', 'India'),
    ('India', 'China'),
    ('India', 'Siam'),
    ('China', 'Siam'),
    ('Siam', 'Indonesia'),

    ('Indonesia', 'New Guinea'),
    ('Indonesia', 'Western Australia'),
    ('New Guinea', 'Western Australia'),
    ('New Guinea', 'Eastern Australia'),
    ('Western Australia', 'Eastern Australia'),
]


# Define continents and their color
continents = {
    'North America': RED,
    'South America': ORANGE,
    'Europe': BLUE,
    'Africa': BROWN,
    'Asia': GREEN,
    'Australia': PURPLE
}


# Assign territories to continents
continents_mapping = {
    'Alaska': 'North America',
    'Northwest Territory': 'North America',
    'Greenland': 'North America',
    'Alberta': 'North America',
    'Ontario': 'North America',
    'Quebec': 'North America',
    'Western United States': 'North America',
    'Eastern United States': 'North America',
    'Central America': 'North America',

    'Venezuela': 'South America',
    'Peru': 'South America',
    'Brazil': 'South America',
    'Argentina': 'South America',

    'Iceland': 'Europe',
    'Scandinavia': 'Europe',
    'Great Britain': 'Europe',
    'Northern Europe': 'Europe',
    'Western Europe': 'Europe',
    'Southern Europe': 'Europe',
    'Ukraine': 'Europe',

    'North Africa': 'Africa',
    'Egypt': 'Africa',
    'East Africa': 'Africa',
    'Congo': 'Africa',
    'South Africa': 'Africa',
    'Madagascar': 'Africa',

    'Ural': 'Asia',
    'Siberia': 'Asia',
    'Yakutsk': 'Asia',
    'Kamchatka': 'Asia',
    'Irkutsk': 'Asia',
    'Mongolia': 'Asia',
    'Japan': 'Asia',
    'Afghanistan': 'Asia',
    'Middle East': 'Asia',
    'India': 'Asia',
    'China': 'Asia',
    'Siam': 'Asia',

    'Indonesia': 'Australia',
    'New Guinea': 'Australia',
    'Western Australia': 'Australia',
    'Eastern Australia': 'Australia',
}


# Define a dictionary to store numbers in each territory
territory_numbers = {territory: 0 for territory in territories}

# Define a dictionary to store colors of territory borders
territory_border_colors = {territory: BLACK for territory in territories}

def round_tup(tup, r=1):
    return (round(tup[0] * r), round(tup[1] * r))

# Function to draw the start menu
def draw_start_menu(screen, ratio):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, round(48*ratio))
    text = font.render("Start Game", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
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

# Function to draw the map
def draw_map(screen, ratio, selected_tab):
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

    draw_sidebar(screen, selected_tab)

# Function to handle window resizing
def handle_resize(screen, new_width, new_height):
    global WIDTH, HEIGHT
    ratio = ((new_width * 1.0) / (WIDTH * 1.0))
    WIDTH, HEIGHT = new_width, new_height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Adjust the screen size
    return ratio

# Function to handle territory clicks
def handle_territory_click(event_pos, ratio):
    for territory, pos in territories.items():
        distance = (((pos[0] * ratio) - event_pos[0]) ** 2 + ((pos[1] * ratio) - event_pos[1]) ** 2) ** 0.5
        if distance <= 20:  # If click is within the radius of a territory
            print(f"Clicked on territory: {territory}")
            # Add your logic for territory click handling here
            territory_numbers[territory] += 1  # Increment territory number
            territory_border_colors[territory] = RED  # Change territory border color
            break  # Break the loop if a territory is clicked

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Expand the width for sidebar
    pygame.display.set_caption("Risk Game by BJ Anderson")
    ratio = 1
    start_menu = True
    selected_tab = 0  # Default to first tab

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_menu:
                    if event.button == 1:  # Left mouse button
                        start_menu = False
                else:
                    if WIDTH * 2/3 <= event.pos[0] <= WIDTH:  # Check if click is inside sidebar
                        if 0 <= event.pos[1] <= 21: #Check if click is inside tabspace
                            selected_tab = (event.pos[0] - round((WIDTH * 2/3) - 15)) // 160
                    else:
                        handle_territory_click(event.pos, ratio)
            # Handle window resizing
            elif event.type == pygame.VIDEORESIZE:
                ratio = handle_resize(screen, event.w, event.h)

        if start_menu:
            draw_start_menu(screen, ratio)
        else:
            draw_map(screen, ratio, selected_tab)

        pygame.display.flip()

if __name__ == "__main__":
    main()