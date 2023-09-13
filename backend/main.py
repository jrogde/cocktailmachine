from guizero import App, ListBox, PushButton, Text, TextBox, Box, Picture
from drink_service import DrinkService

service = DrinkService()
def display_drink_details(selected_value):
    ingredients_textbox.clear()
    
    for drink in service.get_drink_types():
        if drink["Name"] == selected_value:
            # Construct the image path based on the drink's name
            image_path = f"{drink['Name']}.png"
            
            # Update the Picture widget's image attribute
            try:
                drink_image.image = image_path
            except:
                print(f"Error loading image {image_path}. Please ensure the image exists.")
            
            for key, value in drink['Ingredients'].items():
                ingredient_name = service.get_drink_ingredients().get(key)
                ingredients_textbox.append(f"{ingredient_name}: {value[0]} {value[1]}\n")

""" def display_drink_details(selected_value):
    ingredients_textbox.clear()
    
    for drink in service.get_drink_types():
        if drink["Name"] == selected_value:
            for key, value in drink['Ingredients'].items():
                ingredient_name = service.get_drink_ingredients().get(key)
                ingredients_textbox.append(f"{ingredient_name}: {value[0]} {value[1]}\n") """

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
left_box = Box(app, width=300, height=440, layout="grid", grid=[0,0], align="left")
drink_image = Picture(app,grid=[1,0], image="Tequila Sunrise.png")
right_box = Box(app, width=300, height=440, layout="grid", grid=[2,0], align="right")

# Title on top of left box
title = Text(left_box, text="Chose drink", size=20, grid=[0,0])

# A listbox for displaying drink names
listbox = ListBox(left_box,items=[drink["Name"] for drink in service.get_drink_types()], 
                  command=display_drink_details, width=300, height=360, grid=[0,1])

# Make Drink Button
make_button = PushButton(left_box, text="Make drink", grid=[0,2],  command=lambda: service.make_drink(listbox.value))

# Title on top of left box
title = Text(right_box, text="Ingredients", size=20, grid=[0,0])

# A textbox for displaying selected drink's details in the right side of the app
ingredients_textbox = TextBox(right_box, width=50, height=360, multiline=True, scrollbar=True,grid=[0,1])


app.display()
