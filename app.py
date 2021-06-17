""" Password Manager App for CPSC 329 Spring 2021

main for running the app and GUI interface

Resources and references:
https://youtu.be/2RocXKPPx4o
https://youtu.be/XzE-587QupY
https://hoffstadt.github.io/DearPyGui/index.html

Authors: Erin Paslawski, Ryan Pang, Mohit Bhatia"""

# DearPyGUI Imports
import tkinter.filedialog
from dearpygui.core import *
from dearpygui.simple import *
from functions import *

# GLOBAL VARIABLES
cred_buf = []
edit_properties = []

chk_pswrd = ""

width_setting = 600
height_setting = 677


class SmartTable:
    # This is the smart table that will fill widgets for cells based on type
    def __init__(self, name: str, header: List[str] = None):
        self.name = name
        self.header = header
        self.row = 0
        self.column = 0

        if header is not None:
            self.add_header(self.header)

    def add_header(self, header: List[str]):
        with managed_columns(f"{self.name}_head", len(header)):
            for item in header:
                add_text(item)
            
        with managed_columns(f"{self.name}_body", len(header)):
            pass

    def add_row(self, row_content: List[Any]):
        with managed_columns(f"{self.name}_{self.row}", len(row_content)+1, before=f"{self.name}_body"):
            for item in row_content:
                if type(item) is str:
                    add_input_text(f"##{self.name}_{self.row}_{self.column}", default_value=item, width=-1)
                if type(item) is int:
                    add_input_int(f"##{self.name}_{self.row}_{self.column}", default_value=item, width=-1, step=0)
                if type(item) is float:
                    add_input_float(f"##{self.name}_{self.row}_{self.column}", default_value=item, width=-1, step=0)
                self.column += 1
            add_button(f"Edit##{self.name}_{self.row}_{self.column}", width=-1, callback_data=self.row,
                       callback=lambda sender, data: edit_button_callback(data))
        self.column = 0
        self.row += 1

    def clear_table(self):
        print(self.row)
        if (self.row > 0):
            for i in range(self.row):
                if (does_item_exist(f"{self.name}_{i}")): delete_item(f"{self.name}_{i}")
            self.row = 0


set_main_window_size(width_setting + 20, 720)
set_global_font_scale(1.25)
set_theme("Gold")
set_style_window_padding(30, 30)

def edit_button_callback(data):
    print(data)
    #look at the global credential buffer
    global cred_buf, edit_properties
    # retrieve the row
    row = cred_buf[data]
    #edit the contents
    edit_properties = [data] + row
    open_edit()

def confirm_edit_callback(index,row):
    add_password(index, row)
    open_main()

def confirm_add_callback(row):
    global cred_buf
    set_value("Account", "")
    set_value("Username", "")
    set_value("New Password", "")
    add_password(len(cred_buf), row)
    open_main()

def confirm_delete_callback(index):
    global cred_buf
    delete_password(index)
    open_main()


def edit_button_callback(data):
    print(data)
    # look at the global credential buffer
    global cred_buf, edit_properties
    # retrieve the row
    row = cred_buf[data]
    # edit the contents
    edit_properties = [data] + row
    open_edit()


def confirm_edit_callback(index, row):
    add_password(index, row)
    open_main()


def confirm_add_callback(row):
    global cred_buf
    add_password(len(cred_buf), row)
    open_main()


def confirm_mpw_callback(sender, data):
    # compare inputs
    print("Checking password")
    if get_value("Master Password") == get_value("Re-enter Master Password"):
        print("Passwords is correct.")
        # initialize passwords.txt
        init_pw_file(get_value("Master Password"))
        window_close("Register")
    else:
        print("Passwords do not match!")
        add_popup(popupparent="Re-enter Master Password", name="popup", show=True, width=40, height=20)
        add_text("Passwords do not match!")
        add_button("Close", callback=close_popup("popup"))


# Function that checks that the master password is correct
def check_login_callback(sender, data):
    # get master password
    # compare to input
    print("Checking password")
    if check_mpw(get_value("Password")):
        global cred_buf
        cred_buf = get_list()
        window_close("Login")
        open_main()

    else:
        print("Wrong Password!")
        add_popup(popupparent="Password", name="popup", show=True, width=40, height=20)
        add_text("Wrong Password")
        add_button("Close", callback=close_popup("popup"))


def open_main():
    if does_item_exist("Main Page"):
        show_item("Main Page")
        # close others to be safe
    if does_item_exist("Login"):
        window_close("Login")
    if does_item_exist("Register"):
        window_close("Register")
    if does_item_exist("Add Password"):
        hide_item("Add Password")
    populate_table()


def open_edit():
    global edit_properties
    hide_item("Main Page")
    if does_item_exist("Edit Password"):
        show_item("Edit Password")
        set_value("Account##e", edit_properties[3])
        set_value("Password##e", edit_properties[2])
        set_value("Username##e", edit_properties[1])
        print(edit_properties)
    else:
        add_window("Edit Password")


def add_password_callback(sender, data):
    hide_item("Main Page")
    if does_item_exist("Add Password"):
        show_item("Add Password")
    else:
        add_window("Add Password")


def backup_password_callback(sender, data):
    global cred_buf
    root = tkinter.Tk()
    dir = tkinter.filedialog.asksaveasfilename()
    root.withdraw()
    save_password_file(cred_buf, dir)


#Adds the rows to the global credential buffer to the table
def populate_table():
    global cred_buf, tbl
    
    tbl.clear_table()

    for cred in cred_buf:
        tbl.add_row([cred[0],cred[1],cred[2]])


def check_strength_callback(sender, data):
    set_value("Strength", check_strength(get_value("Check")))
    set_value("Suggestion", return_leet(get_value("Check")))


def check_strength_add_callback(sender, data):
    set_value("Password Strength", check_strength(get_value("Check Pswrd")))
    set_value("New Suggestion", return_leet(get_value("Check Pswrd")))


def check_strength_edit_callback(sender, data):
    set_value("Password Strength Test", check_strength(get_value("Check Old Password")))
    set_value("New Password Suggestion", return_leet(get_value("Check Old Password")))


# calls the functions. add_password function to actually put the encrypted password into a text file
def add_password(index, row):
    # code for adding the new password to the database, including encryption
    global cred_buf
    size = len(cred_buf)-1
    if(size< index):
        cred_buf.append(row)
    else:
        cred_buf[index] = row
    print("resaving file")
    cred_buffer_to_file(cred_buf)
    open_main()


# calls the functions. add_password function to actually put the encrypted password into a text file
def delete_password(index):
    # code for adding the new password to the database, including encryption
    global cred_buf
    cred_buf.pop(index)
    print("resaving file")
    cred_buffer_to_file(cred_buf)
    open_main()


with window("Edit Password", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Edit password.")
    set_window_pos("Edit Password", 0, 0)

    add_text("Enter the credentials to be changed:")
    add_spacing(count=5)

    # collect password input
    add_input_text("Account##e", width=250)
    add_input_text("Username##e", width=250)
    add_input_text("Password##e", width=250)
    add_button("Confirm Changes", callback=lambda sender, data: confirm_edit_callback(edit_properties[0],
                                                                                      [get_value("Username##e"),
                                                                                       get_value("Password##e"),
                                                                                       get_value("Account##e")]))

    add_spacing(count=20)
    # Check strength
    add_input_text("Check Old Password", width=250)
    add_button("Check old strength", callback=check_strength_edit_callback)

    add_input_text("Password Strength Test")
    add_input_text("New Password Suggestion")

    add_spacing(count=30)

    add_button("Cancel##e", callback=lambda x, y: open_main())


with window("Add Password", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
    print("Add password.")
    set_window_pos("Add Password", 0, 0)

    add_text("Enter the credentials to be added:")
    add_spacing(count=5)

    # collect password input
    add_input_text("Account", width=250, hint="URL")
    add_input_text("Username", width=250, hint="Username")
    add_input_text("New Password", width=250, hint="Password")

    add_button("Add", callback=lambda sender, data: confirm_add_callback(
        [get_value("Username"), get_value("New Password"), get_value("Account")]))

    add_spacing(count=20)
    # Check strength
    add_input_text("Check Pswrd", width=250)
    add_button("Check strength", callback=check_strength_add_callback)

    add_input_text("Password Strength")
    add_input_text("New Suggestion")

    add_spacing(count=30)

    add_button("Cancel", callback=lambda x, y: open_main())


with window("Main Page", width=width_setting, height=height_setting, y_pos=0, x_pos=0, no_collapse=True, no_resize=True,
            no_close=True,
            no_move=True, no_background=False):
    # add buttons for doing stuff
    # add password
    draw_image("logo", "Logo.png", [0, 40], [420, 260])

    add_button("Add a Password", callback=add_password_callback)
   
    #Table
    global tbl
    tbl = SmartTable(name="table")
    tbl.add_header(["Login ID:", "Passphrase:", "Website:", "Edit"])

    add_button("Backup Password File", callback=backup_password_callback)


    # Add the logo
    draw_image("logo", "Logo.png", [0, 40], [420, 260])
    add_spacing(count=10)
    # Check strength
    add_text("Check the strength of a password:")

    add_input_text("Check", width=250)
    add_same_line()
    add_button("Check password strength", callback=check_strength_callback)

    add_spacing(count=10)

    # Backup Passwords
    add_label_text("Strength")
    add_input_text("Suggestion")

    


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
    add_input_text("Password", width=250, hint="Master Password", on_enter=True, callback=check_login_callback)
    add_same_line()  # add button beside input
    add_button("Enter", callback=check_login_callback)

with window("Register", width=width_setting, height=height_setting, no_collapse=True, no_resize=True, no_close=True,
            no_move=True, no_background=False):
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
        f = open("passwords.txt", "r")
        print("passwords.txt exists")
        window_close("Register")
    except:
        print("No password file exists")


# start program
start_dearpygui()
print("Goodbye!")
