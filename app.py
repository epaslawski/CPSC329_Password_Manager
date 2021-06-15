""" Password Manager App for CPSC 329 Spring 2021

main for running the app and GUI interface

Resources and references:
https://youtu.be/2RocXKPPx4o
https://youtu.be/XzE-587QupY
https://hoffstadt.github.io/DearPyGui/index.html

Author: Erin Paslawski"""

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

# Function that checks that the master password is correct
# Right now it is hardcoded but it should read from the encrypted file
def check_login_callback(sender, data):
    # open text file
    # get master password
    # compare to input
    print("Checking password")
    if get_value("Password") == 'password':
        print("Passwords is correct.")
        window_close("Login")
        open_main
    # trying to implement a popup
    """else:
        print("Wrong Password!")
        add_popup(popupparent="Password", name="popup", show=True, width= 40, height=20)
        add_text("Wrong Password")
        add_button("Close", callback=close_popup("popup"))"""

# open the main page and close/hide others
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


# show the add password page
def add_password_window(sender, data):
    hide_item("Main Page")
    if does_item_exist("Add Password"):
        show_item("Add Password")
    else:
        add_window("Add Password")


# show the passwords page
def show_passwords_window(sender, data):
    pass


# show the check strength page
def check_strength_window(sender, data):
    pass


# calls the functions. add_password function to actually put the encrypted password into a text file
def add_password(sender, data):
    # code for adding the new password to the database, including encryption
    print("Adding Password")
    functions.add_password(get_value("Account"), get_value("Username"), get_value("New Password"))

    hide_item("Add Password")

    open_main
    show_item("Main Page")


# Window for Add Password page
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
    # add password button
    add_button("Add", callback=add_password)

    add_spacing(count=30)
    # back to main page button
    add_button("Return", callback=open_main)


# Main page window
with window("Main Page", width=width_setting, height=height_setting, y_pos=0, x_pos=0, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Welcome to the Password Manager.")

    add_drawing("logo", width=520, height=290)

    # Add the logo
    draw_image("logo", "Logo.png", [0, 40], [420, 260])

    # add buttons for doing stuff
    # add password
    add_button("Add a Password", callback=add_password_window)

    # view passwords
    add_button("View Passwords", callback=show_passwords_window)

    # Check strength
    add_button("Check password strength", callback=check_strength_window)


# Generic function that hides windows
def window_close(sender):
    hide_item(sender)
    log_debug("window was deleted")


# initial login window
with window("Login", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Login to Password Manager.")
    # hide the other windows and wait for the master password

    set_window_pos("Login", 0, 0)

    add_text("Enter your master password: ")
    add_spacing(count=5)

    # collect password input
    add_input_text("Password", width=250, default_value="password")
    add_same_line()  # add button beside input
    add_button("Enter", callback=check_login_callback)

## start program
start_dearpygui()
print("Goodbye!")
