import json

def transform_coordinates(data):
    territories = data["territories"]
    transformed_territories = {}
    
    for territory, coordinates in territories.items():
        x, y = coordinates
        transformed_x = x / 1200.0
        transformed_y = y / 675.0
        transformed_territories[territory] = [transformed_x, transformed_y]
    
    transformed_data = {
        "territories": transformed_territories,
        "connections": data["connections"],
        "continents_mapping": data["continents_mapping"]
    }
    
    return transformed_data

def main():
    with open("setup.json", "r") as f:
        data = json.load(f)
    
    transformed_data = transform_coordinates(data)
    
    with open("temp.json", "w") as f:
        json.dump(transformed_data, f, indent=4)

if __name__ == "__main__":
    main()
