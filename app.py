# DearPyGUI Imports
from dearpygui.core import *
from dearpygui.simple import *


width_setting = 520
height_setting = 677

set_main_window_size(540, 720)
set_global_font_scale(1.25)
set_theme("White")
set_style_window_padding(30, 30)


def check_login_callback(sender, data):
    # open text file
    # get master password
    # compare to input
    print("Checking password")
    if get_value("Password") == 'password':
        print("Passwords is correct.")
        window_close("Login", data)
        open_main


def open_main():
    if does_item_exist("Main Page"):
        show_item("Main Page")
    else:
        add_window("Main Page")


def add_password_callback(sender, data):
    window_close("Main Page")

    # add input box

    # add button

    # add back button

    add_button("Main Page", callback=open_main)


def view_passwords_callback(args):
    pass


def check_strength_callback(args):
    pass


with window("Main Page", width=width_setting, height=height_setting):
    print("Welcome to the Password Manager.")
    set_window_pos("Main Page", 0, 0)
    add_drawing("logo", width=520, height=290)

    # IF THE PREVIOUS LINE OF CODE TRIGGERS AN ERROR TRY
    draw_image("logo", "Logo.png", [0, 40], [420, 260])

    # add buttons for doing stuff
    # add password
    add_button("Add Password", callback=add_password_callback)

    # view passwords
    add_button("View Passwords", callback=view_passwords_callback)

    # Check strength
    add_button("Check password strength", callback=check_strength_callback)

def window_close(sender, data):
    delete_item(sender)
    log_debug("window was deleted")


with window("Login", width=width_setting, height=height_setting):
    print("Login to Password Manager.")
    set_window_pos("Login", 0, 0)
    # add_drawing("logo", width=520, height=290)
    add_text("Enter your master password: ")
    add_spacing(count=5)

    # collect password input
    add_input_text("Password", width=250, default_value="Add Password here.")
    add_same_line()  # add button beside input
    add_button("Enter", callback=check_login_callback)


start_dearpygui()
print("Goodbye!")
