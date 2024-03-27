import pygame, sys, json

from game_engine.game_scene import *
from game_engine.game_object import *
from game_engine.player import *
from game_engine.start_menu import *
from game_engine.risk_game import *
from rival_engine import *
from setup_routines import *
from user_interface import *
from game_engine.start_menu import *
from colors import *
from setup_routines import init_start_menu
from game_engine.world import test

def main():
    #test()
    players = init_players(6)
    start_menu = StartMenu(init_start_menu(players))
    if not start_menu.run():
        RiskGame((1200, 675),'setup.json', [p for p, condition in zip(players, start_menu.players()) if condition]).run()

if __name__ == "__main__":
    main()