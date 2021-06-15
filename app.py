# DearPyGUI Imports
from dearpygui.core import *
from dearpygui.simple import *
import functions

cred_buf = []
enc_key = b''
tbl = None


width_setting = 520
height_setting = 677

set_main_window_size(540, 720)
set_global_font_scale(1.25)
set_theme("Gold")
set_style_window_padding(30, 30)

def confirm_mpw_callback(sender, data):
    # compare inputs
    print("Checking password")
    if get_value("Master Password") == get_value("Re-enter Master Password"):
        print("Passwords is correct.")
        #initialize passwords.txt
        functions.initPWFile(bytes(get_value("Master Password"), "utf-8"))
        window_close("Register")
    else:
        print("Passwords do not match!")
        add_popup(popupparent="Re-enter Master Password", name="popup", show=True, width= 40, height=20)
        add_text("Passwords do not match!")
        add_button("Close", callback=close_popup("popup"))

def check_login_callback(sender, data):
    # get master password
    # compare to input
    print("Checking password")
    if functions.check_mpw(get_value("Password")):
        print("Passwords is correct.")
        functions.get_list(get_value("Password"))
        global enc_key, cred_buf, tbl
        enc_key = functions.get_key()
        cred_buf = functions.get_list(get_value("Password"))
        window_close("Login")
        open_main()
        
    else:
        print("Wrong Password!")
        add_popup(popupparent="Password", name="popup", show=True, width= 40, height=20)
        add_text("Wrong Password")
        add_button("Close", callback=close_popup("popup"))


def open_main():
    if does_item_exist("Main Page"):
        show_item("Main Page")
    else:
        add_window("Main Page")
        
    # close others to be safe
    if does_item_exist("Login"):
        window_close("Login")
    if does_item_exist("Register"):
        window_close("Register")
    if does_item_exist("Add Password"):
        hide_item("Add Password")
    populate_table()


def open_register(sender, data):
    if does_item_exist("Login"):
        window_close("Login")
    add_window("Register")


def add_password_callback(sender, data):
    hide_item("Main Page")
    if does_item_exist("Add Password"):
        show_item("Add Password")
    else:
        add_window("Add Password")

def populate_table():
    global cred_buf, tbl
    #add_table(parent="Main Page", name="table", headers=["Username","Password","Website"])
    print(cred_buf)
    for cred in cred_buf:
        add_row("table",[cred[1],cred[2],cred[0]])
        

def view_passwords_callback(sender, data):
    pass


def check_strength_callback(sender, data):
    pass


def add_password(row=[]):
    # code for adding the new password to the database, including encryption
    global cred_buf, enc_key
    cred_buf.append(row)
    print("Adding Password")
    functions.add_password(row, enc_key)
    add_row("table",[row[1],row[2],row[0]])
    # window_close("Add Password")
    hide_item("Add Password")
    show_item("Main Page")


with window("Add Password", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Add a new password.")
    set_window_pos("Add Password", 0, 0)

    add_text("Enter the credentials to be added:")
    add_spacing(count=5)

    # collect password input
    add_input_text("Account", width=250, default_value="")
    add_input_text("Username", width=250, default_value="")
    add_input_text("New Password", width=250, default_value="")
    add_button("Add", callback=lambda x,y:add_password(row=[get_value("Account"), get_value("Username"), get_value("New Password")]))

    add_spacing(count=30)

    add_button("Cancel", callback=open_main)


with window("Main Page", width=width_setting, height=height_setting, y_pos=0, x_pos=0, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    # add buttons for doing stuff
    # add password
    add_button("Add a Password", callback=add_password_callback)
    add_same_line()  # add button beside input
    # view passwords
    add_button("View Passwords", callback=view_passwords_callback)
    print("Welcome to the Password Manager.")

    add_table(parent="Main Page", name="table", headers=["Username","Password","Website"])

    # Add the logo
    draw_image("logo", "Logo.png", [0, 40], [420, 260])

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


with window("Register", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Register Password")
    
    # hide the other windows and wait for the master password

    set_window_pos("Register", 0, 0)
    # add_drawing("logo", width=520, height=290)
    add_text("Create your master password: ")
    add_spacing(count=5)

    # collect password input
    add_input_text("Master Password", width=250)
    add_input_text("Re-enter Master Password", width=250)
    add_button("Confirm", callback=confirm_mpw_callback)
    try:
        f = open("passwords.txt","x")
    except:
        print("passwords.txt exists")
        window_close("Register")


start_dearpygui()
show_debug()
print("Goodbye!")
