import pandas as pd

class Player:

    def __init__(self, name, age, height, weight, image_path):
        self.name = name
        self.age = age
        self.image_path = image_path

        #If the player's weight was blank kn the database, set it to -1
        if pd.isna(weight):
            self.weight = -1
        else:
            self.weight = int(weight)

        #Height is separated into inches and feet
        if pd.isna(height):
            self.height_ft = -1
            self.height_inch = -1
        else:
            ft, inch = height.split("-")
            self.height_ft = int(ft)
            self.height_inch = int(inch)


    def __repr__(self):
        return f"Player({self.name})"

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name and self.age == other.age and self.height == other.height and self.weight == other.weight and self.image_path == other.image_path

    def __hash__(self):
        return hash((self.name, self.age, self.height, self.weight, self.image_path))