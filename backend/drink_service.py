import  logging


logger = logging.getLogger(__name__)


class DrinkService:
    drink = {
        "recipes": {
            "Gin and Tonic (GT)": {
                "ingredients": {
                    "Gin": "50 ml",
                    "Tonic Water": "150 ml"
                }
            },
            "Sex on the Beach": {
                "ingredients": {
                    "Vodka": "50 ml",
                    "Peach Schnapps": "30 ml",
                    "Cranberry Juice": "90 ml",
                    "Orange Juice": "90 ml",
                    "Grenadine Syrup": "15 ml"
                }
            },
            "Mojito": {
                "ingredients": {
                    "White Rum": "60 ml",
                    "Fresh Lime Juice": "30 ml",
                    "Simple Syrup": "15 ml",
                    "Soda Water": "120 ml"
                }
            }
        }
    }
    #def __init__(self):

    def get_drinks(self):
        return self.drink


if __name__ == '__main__':
    a = DrinkService()
    drink = a.get_drinks()
    print(drink)


