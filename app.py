# DearPyGUI Imports
from dearpygui.core import *
from dearpygui.simple import *

import functions

width_setting = 520
height_setting = 677

set_main_window_size(540, 720)
set_global_font_scale(1.25)
set_theme("Gold")
set_style_window_padding(30, 30)


def check_login_callback(sender, data):
    # open text file
    # get master password
    # compare to input
    print("Checking password")
    if get_value("Password") == 'password':
        print("Passwords is correct.")
        window_close("Login")
        open_main
    """else:
        print("Wrong Password!")
        add_popup(popupparent="Password", name="popup", show=True, width= 40, height=20)
        add_text("Wrong Password")
        add_button("Close", callback=close_popup("popup"))"""


def open_main(sender, data):
    if does_item_exist("Main Page"):
        show_item("Main Page")
    else:
        add_window("Main Page")
    # close others to be safe
    if does_item_exist("Login"):
        window_close("Login")
    if does_item_exist("Add Password"):
        hide_item("Add Password")


def add_password_callback(sender, data):
    hide_item("Main Page")
    if does_item_exist("Add Password"):
        show_item("Add Password")
    else:
        add_window("Add Password")


def view_passwords_callback(sender, data):
    pass


def check_strength_callback(sender, data):
    pass


def add_password(sender, data):
    # code for adding the new password to the database, including encryption
    print("Adding Password")
    functions.add_password(get_value("Account"), get_value("Username"), get_value("New Password"))
    # window_close("Add Password")
    hide_item("Add Password")

    open_main
    show_item("Main Page")


with window("Add Password", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Add a new password.")
    set_window_pos("Add Password", 0, 0)

    add_text("Enter the credentials to be added:")
    add_spacing(count=5)

    # collect password input
    add_input_text("Account", width=250, default_value="Website")
    add_input_text("Username", width=250, default_value="Username")
    add_input_text("New Password", width=250, default_value="New password")
    add_button("Add", callback=add_password)

    add_spacing(count=30)

    add_button("Return", callback=open_main)


with window("Main Page", width=width_setting, height=height_setting, y_pos=0, x_pos=0, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Welcome to the Password Manager.")

    add_drawing("logo", width=520, height=290)

    # Add the logo
    draw_image("logo", "Logo.png", [0, 40], [420, 260])

    # add buttons for doing stuff
    # add password
    add_button("Add a Password", callback=add_password_callback)

    # view passwords
    add_button("View Passwords", callback=view_passwords_callback)

    # Check strength
    add_button("Check password strength", callback=check_strength_callback)


def window_close(sender):
    delete_item(sender)
    log_debug("window was deleted")


with window("Login", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Login to Password Manager.")
    # hide the other windows and wait for the master password

    set_window_pos("Login", 0, 0)
    # add_drawing("logo", width=520, height=290)
    add_text("Enter your master password: ")
    add_spacing(count=5)

    # collect password input
    add_input_text("Password", width=250, default_value="password")
    add_same_line()  # add button beside input
    add_button("Enter", callback=check_login_callback)

start_dearpygui()
print("Goodbye!")
