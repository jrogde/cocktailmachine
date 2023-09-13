from guizero import App, ListBox, PushButton, Text, TextBox, Box
import sys
sys.path.append("../../")

from backend.drink_service import DrinkService

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
    print(listbox.value)
    if selected_value:
        for drink in service.get_drink_types():
            if drink["Name"] == selected_value:
                print(f"Details for {drink['Name']}:")
                for key, value in drink['Ingredients'].items():
                    ingredient_name = service.get_drink_ingredients().get(key)
                    print(f"{ingredient_name}: {value[0]} {value[1]}")

app = App(title="Cocktail Maker", width=800, height=440, layout="grid")

# Left and Right boxes using Grid layout
left_box = Box(app, width=400, height=440, layout="grid", grid=[0,0], align="left")
right_box = Box(app, width=400, height=440, layout="grid", grid=[1,0], align="right")

# Title on top of left box
title = Text(left_box, text="Chose drink", size=20, grid=[0,0])

# A listbox for displaying drink names
listbox = ListBox(left_box,items=[drink["Name"] for drink in service.get_drink_types()], 
                  command=display_drink_details, width=400, height=400, grid=[0,1])

# Make Drink Button
make_button = PushButton(drinkListbox, text="Make drink", width="fill", grid=[0,1])

app.display()


# A textbox for displaying selected drink's details in the right side of the app
ingredients_textbox = TextBox(drinkListbox, width=400, height=440, multiline=True, scrollbar=True)

app.display()
