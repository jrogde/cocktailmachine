from guizero import App, PushButton, Box

import smbus2 as smbus

def run_pump(pump_number):
    try:
        bus = smbus.SMBus(1)
        bus.write_byte(0x04, pump_number)
    except Exception as e:
        print(f"Error communicating with Arduino: {e}")

def show_home():
    setup_box.hide()
    home_box.show()

def show_setup():
    home_box.hide()
    setup_box.show()

app = App(title="Cocktail Maker", width=800, height=440, layout="grid")

# Home Screen
home_box = Box(app, layout="grid", grid=[0,0])
PushButton(home_box, text="Setup", grid=[0,0], width="fill", command=show_setup)
for i in range(6):
    PushButton(home_box, text=f"Cocktail {i+1}", grid=[0, i+1], width="fill")

# Setup Screen
setup_box = Box(app, layout="grid", grid=[0,0], visible=False)
PushButton(setup_box, text="Back", grid=[0,0], width="fill", command=show_home)
for i in range(6):
    PushButton(setup_box, text=f"Test Pump {i+1}", grid=[0, i+1], width="fill", command=lambda i=i: run_pump(i+1))

app.display()
