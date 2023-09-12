from guizero import App, ListBox, PushButton, Text, TextBox, Box
from drink_service import DrinkService

service = DrinkService()


def display_drink_details(selected_value):
    ingredients_textbox.clear()

    for drink in service.get_drink_types():
        if drink["Name"] == selected_value:
            for key, value in drink['Ingredients'].items():
                ingredient_name = service.get_drink_ingredients().get(key)
                ingredients_textbox.append(f"{ingredient_name}: {value[0]} {value[1]}\n")


def print_drink_details():
    selected_value = listbox.value
    if selected_value:
        for drink in service.get_drink_types():
            if drink["Name"] == selected_value:
                print(f"Details for {drink['Name']}:")
                for key, value in drink['Ingredients'].items():
                    ingredient_name = service.get_drink_ingredients().get(key)
                    print(f"{ingredient_name}: {value[0]} {value[1]}")


app = App(title="Cocktail Maker", width=800, height=440)

# Create a Box to hold the listbox and the print button, set the width to half of app's width
left_box = Box(app, width=400, height=440, align="left")
right_box = Box(app, width=400, height=440, align="right")

# A listbox for displaying drink names
listbox = ListBox(left_box, items=[drink["Name"] for drink in service.get_drink_types()],
                  command=display_drink_details, width=400, height=400)

# A button to print the details of the selected drink
print_button = PushButton(left_box, text="Print Drink Details", command=print_drink_details, width=400)

# A textbox for displaying selected drink's details in the right side of the app
ingredients_textbox = TextBox(right_box, width=400, height=440, multiline=True, scrollbar=True)

app.display()
