import pygame, sys, json

from game_engine.game_scene import *
from game_engine.game_object import *
from game_engine.player import *
from rival_engine import *
from setup_routine import *
from user_interface import *
from start_menu import *
from colors import *

class RiskGame(GameScene):
    def __init__(self, size):
        super().__init__(size)

def init_players(n):
    player_colors = [LIGHT_BLUE, PINK, VIOLET, LIME_GREEN, MAROON, YELLOW]
    players = []
    for i in range(n):
        players.append(Player(f"Player {i+1}", player_colors[i]))
    return players

def main():
    if not StartMenu(init_start_menu(init_players(6))).run():
        RiskGame((1200, 675)).run()

if __name__ == "__main__":
    main()