import pygame, sys, json

from game_engine.game_scene import *
from game_engine.game_object import *
from game_engine.player import *
from game_engine.start_menu import *
from rival_engine import *
from init_start_menu import *
from user_interface import *
from game_engine.start_menu import *
from colors import *
from init_start_menu import init_start_menu

class RiskGame(GameScene):
    def __init__(self, size, players):
        super().__init__(size)
        self.players = players

def init_players(n):
    player_colors = [LIGHT_BLUE, PINK, VIOLET, LIME_GREEN, MAROON, YELLOW, RED, ORANGE, GREEN, BLUE, PURPLE, BROWN]
    players = []
    for i in range(n):
        players.append(Player(f"Player {i+1}", player_colors[i]))
    return players

def main():
    players = init_players(6)
    start_menu = StartMenu(init_start_menu(players))
    i = 0
    if not start_menu.run():
        RiskGame((1200, 675), [p for p, condition in zip(players, start_menu.players()) if condition]).run()

if __name__ == "__main__":
    main()