from ..game_engine import *

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


def retrieve_setup():
    return True