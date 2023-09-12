from guizero import App, PushButton, Text, ListBox, Window, TextBox
import smbus2 as smbus

def run_pump():
    try:
        bus = smbus.SMBus(1)  # This might be 0 or 1 depending on your system
        bus.write_byte(0x04, 0x01)
    except Exception as e:
        print(f"Error communicating with Arduino: {e}")

def show_ingredients(selected_cocktail):
    if selected_cocktail == "Mojito":
        ingredient_box.value = "Rum, Mint, Sugar, Lime, Soda"
    elif selected_cocktail == "Margarita":
        ingredient_box.value = "Tequila, Triple Sec, Lime"
    elif selected_cocktail == "Pina Colada":
        ingredient_box.value = "Rum, Pineapple Juice, Coconut Cream"
    mix_button.enabled = True  # Enable the "Mix" button

def mix_cocktail():
    ingredient_box.append("\n\nMixing your " + cocktail_listbox.value + "!")


def add_new_drink():
    # Create a new window for the popup
    new_drink_window = Window(app, title="Add New Drink", width=400, height=200)
    Text(new_drink_window, "Drink Name:")
    
    # TextBox for drink name
    drink_name = TextBox(new_drink_window, width="fill")
    
    Text(new_drink_window, "Ingredients (comma separated):")
    
    # TextBox for ingredients
    ingredients = TextBox(new_drink_window, width="fill")
    
    # Button to save the new drink to the list
    def save_drink():
        cocktail_name = drink_name.value
        cocktail_ingredients = ingredients.value
        if cocktail_name and cocktail_ingredients:
            cocktails.append(cocktail_name)
            cocktail_listbox.append(cocktail_name)
            cocktail_ingredients_dict[cocktail_name] = cocktail_ingredients
        new_drink_window.destroy()

    PushButton(new_drink_window, text="Save", command=save_drink, width="fill")

cocktail_ingredients_dict = {
    "Mojito": "Rum, Mint, Sugar, Lime, Soda",
    "Margarita": "Tequila, Triple Sec, Lime",
    "Pina Colada": "Rum, Pineapple Juice, Coconut Cream"
}

def show_ingredients(selected_cocktail):
    ingredients = cocktail_ingredients_dict.get(selected_cocktail, "")
    ingredient_box.value = ingredients
    if ingredients:
        mix_button.enabled = True
    else:
        mix_button.enabled = False


app = App(title="Cocktail Maker", width=780, height=420)  # Adjusted dimensions

new_drink_button = PushButton(app, text="New", command=add_new_drink, width="fill", align="bottom")



# Position and size adjustments for better display
cocktails = ["Mojito", "Margarita", "Pina Colada"]
cocktail_listbox = ListBox(app, items=cocktails, command=show_ingredients, width="fill", height="fill", align="left")

ingredient_box = Text(app, width="fill", height="fill", align="right")

pump_button = PushButton(app, text="Run Pump", command=run_pump, width="fill", align="bottom")

mix_button = PushButton(app, text="Mix", command=mix_cocktail, width="fill", align="bottom", enabled=False)

app.display()
