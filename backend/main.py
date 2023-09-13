from guizero import App, ListBox, PushButton, Text, TextBox, Box, Picture, Window
from drink_service import DrinkService
from PIL import ImageTk, Image

selected_drink_name = None

service = DrinkService()
def display_drink_details(selected_value):
    global selected_drink_name  # declare it as global to modify the global variable
    
    selected_drink_name = selected_value  # update the selected drink name
    ingredients_textbox.clear()
    
    for drink in service.get_drink_types():
        if drink["Name"] == selected_value:
            drink_name_label.value = selected_value
            # Construct the image path based on the drink's name
            for key, value in drink['Ingredients'].items():
                ingredient_name = service.get_drink_ingredients().get(key)
                ingredients_textbox.append(f"{ingredient_name}: {value[0]} {value[1]}\n")


app = App(title="Cocktail Maker", width=800, height=440, layout="grid")
#app.set_full_screen()

# Left and Right boxes using Grid layout
left_box = Box(app, width=500, height=440, layout="grid", grid=[0,0], align="left")
""" drink_image = Picture(app,grid=[1,0], image="images/Tequila Sunrise.png") """
right_box = Box(app, width=300, height=440, layout="grid", grid=[1,0], align="right")

drink_name_label = Text(right_box, text="", size=20, grid=[0,0])

ingredients_textbox = TextBox(right_box, width=25, height=10, multiline=True, scrollbar=True,grid=[0,1])

def re_enable_button():
    make_button.enabled = True

def make_drink_and_disable():
    service.make_drink(selected_drink_name)
    make_button.enabled = False
    app.after(service.get_drink_max_ingredient_ms(selected_drink_name), re_enable_button)  # re-enable after 10 seconds (10000 milliseconds)
def button_action(name):
    print(name)
def goto_settings():
    # Create a new Window for the settings
    settings_window = Window(app, title="Settings", width=800, height=440, layout="grid")
    
    drink_ingredients = service.get_drink_ingredients()
    # Add some settings controls, for example:
    close_button = PushButton(settings_window,grid=[2,4], text="Close", command=settings_window.destroy)
    for index, ingredient in enumerate(drink_ingredients.values()):
        row = index // 4
        col = index % 4
        button = PushButton(settings_window, text=ingredient, grid=[col, row], width=20, 
                            command=lambda k=ingredient: service.run_ingredient(k, 5))





# Make Drink Button
make_button = PushButton(right_box, image="images/Make Cocktail Button.png", grid=[0,2], width=150, align="left", command=make_drink_and_disable)


settings_button = PushButton(right_box, image="images/settings image.png", grid=[0,2], align="right", command=goto_settings)


# A textbox for displaying selected drink's details in the right side of the app

all_drinks = service.get_drink_types()

# Create a list to hold all drink image buttons
drink_buttons = []

for index, drink in enumerate(all_drinks):
    # Calculate grid coordinates based on the index
    row = index // 5  # Using integer division to get the row number
    col = index % 5   # Using modulo to get the column number (0 or 1)
    
    image_path = f"images/{drink['Name']}.png"
    
    # Load and scale the image using PIL
    original = Image.open(image_path)
    width, height = original.size
    scaled = original.resize((int(width * 0.7), int(height * 0.7)))
    
    # Convert the PIL Image object into a format that guizero can display
    tk_scaled_image = ImageTk.PhotoImage(scaled)
    
    # Attach the scaled image to the button
    button = PushButton(left_box, image=tk_scaled_image, grid=[col, row],
                        command=display_drink_details, args=[drink['Name']])
    drink_buttons.append(button)


app.display()
