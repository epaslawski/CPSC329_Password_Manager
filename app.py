# DearPyGUI Imports
from dearpygui.core import *
from dearpygui.simple import *


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



def on_window_close(sender, data):
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
