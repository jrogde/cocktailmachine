import logging
import json
from pump_service import PumpService


logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class DrinkService:
    pump_service = PumpService()

    drink_ingredients = {
        1: "Vodka",
        2: "Rum",
        3: "Tequila",
        4: "Gin",
        5: "Whiskey",
        6: "Triple Sec",
        7: "Lime Juice",
        8: "Lemon Juice",
        9: "Orange Juice",
        10: "Cranberry Juice",
        11: "Grenadine",
        12: "Simple Syrup",
        13: "Cola",
        14: "Tonic Water",
        15: "Club Soda",
        16: "Bitters"
    }

    drink_types = [
        {
            "Name": "Tequila Sunrise",
            "Ingredients": {
                3: (60, "ml"),  # Tequila
                9: (90, "ml"),  # Orange Juice
                11: (15, "ml")  # Grenadine
            }
        },
        {
            "Name": "Gin and Tonic",
            "Ingredients": {
                4: (60, "ml"),  # Gin
                14: (90, "ml")  # Tonic Water
            }
        },
        {
            "Name": "Vodka Cranberry",
            "Ingredients": {
                1: (60, "ml"),  # Vodka
                10: (90, "ml")  # Cranberry Juice
            }
        },
        {
            "Name": "Whiskey Sour",
            "Ingredients": {
                5: (60, "ml"),  # Whiskey
                7: (30, "ml"),  # Lemon Juice
                12: (15, "ml")  # Simple Syrup
            }
        },
        {
            "Name": "Rum Punch",
            "Ingredients": {
                2: (60, "ml"),  # Rum
                9: (30, "ml"),  # Orange Juice
                11: (15, "ml")  # Grenadine
            }
        },
        {
            "Name": "Vodka Soda",
            "Ingredients": {
                1: (60, "ml"),  # Vodka
                15: (90, "ml")  # Club Soda
            }
        },
        {
            "Name": "Mojito",
            "Ingredients": {
                2: (60, "ml"),  # Rum
                7: (30, "ml"),  # Lime Juice
                12: (30, "ml"),  # Simple Syrup
                15: (90, "ml")  # Club Soda
            }
        },
        {
            "Name": "Moscow Mule",
            "Ingredients": {
                1: (60, "ml"),  # Vodka
                7: (30, "ml"),  # Lime Juice
                16: (90, "ml")  # Ginger Beer
            }
        },
        {
            "Name": "Gin Fizz",
            "Ingredients": {
                4: (60, "ml"),  # Gin
                7: (30, "ml"),  # Lemon Juice
                12: (15, "ml"),  # Simple Syrup
                15: (90, "ml")  # Club Soda
            }
        },
        {
            "Name": "Rum and Cola",
            "Ingredients": {
                2: (60, "ml"),  # Rum
                13: (90, "ml")  # Cola
            }
        }
    ]

    def get_drink_ingredients(self):
        return self.drink_ingredients

    def get_drink_types(self):
        return self.drink_types

    def get_drink(self, name):
        limited_list = [element for element in self.drink_types if element['Name'] == name]
        return limited_list[0]

    def make_drink(self, name):
        if name is None:
            return
        drink = self.get_drink(name)
        ingredients = drink['Ingredients']
        logger.info(ingredients)
        for key, value in ingredients.items():
            pump_number = key
            ml = value[0]
            self.pump_service.run_pump(pump_number, ml)

if __name__ == '__main__':
    a = DrinkService()
    a.make_drink("Gin Fizz")


