import tkinter as tk
from tkinter import font as tkfont 
import os 
import sys
import pyperclip
from .static_config_parser import StaticConfigParser
from .database import Database

"""A password manager, GUI created in tktinker.

Password-Manager is a password manager. Passwords are encrypted then stored in
a mySQL database, which is locked with a master key via the login page.
The login page and the main page are stacked on top of each other, once the correct master password is inputted
the main page is raised above the login page. The frame on top will be the frame that is visible.
"""
# Set CWD to script directory
os.chdir(sys.path[0])

### globals ###
DB = Database()

# classes
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight='bold', slant='italic')

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('LoginPage')

    def show_frame(self, page_name):
        # show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.attempt_count = 1
        
        config = StaticConfigParser()
        self.master_password = config.get('LOGIN', 'master_password')
        
        # input fields
        self.login_label = tk.Label(self, text="Master Password: ", font='arial 24')
        self.login_entry = tk.Entry(self, show='*')
        self.login_label.grid(row=0, column=0)
        self.login_entry.grid(row=0, column=1)

        # login button
        self.login_btn = tk.Button(self, text="Login",command=self.login_btn_clicked)
        self.login_btn.grid(row=1, column=2)
    
    def login_btn_clicked(self):
        password = self.login_entry.get()
        if (password == self.master_password):
            self.controller.show_frame('MainPage')
        # incorrect password
        self.incorrect_password_label = tk.Label(self, text=f"Incorrect password({self.attempt_count})", fg='red')
        self.attempt_count += 1
        self.incorrect_password_label.grid(row=1, column=0)
        self.login_entry.delete(0, 'end')

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def submit_btn_clicked(self):
        title = self.title_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        # missing input
        if (title == "" or email == "" or password == ""):
            self.reset_labels()
            self.incorrect_input_label.grid(row=5, column=0, columnspan=2, sticky='w')
        # correct input
        else:
            DB.insert(title, username, password, email)

            self.options = DB.select_all_entry_no_and_title()
            self.display_RHS(DB.get_highest_id()) # get most recent entry_no

            pretty_output = DB.get_highest_id() + ". " + DB.get_title(DB.get_highest_id())
            self.variable.set(pretty_output) # display most recent entry

            self.update_options_menu()

            self.title_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            
            self.reset_labels()
        
    def display_RHS(self, value):
        entry_no = value[0]
        username = DB.get_username(entry_no)
        email = DB.get_email(entry_no)

        # update labels
        self.RHS_username_label.config(text=username, font="arial 16")
        self.RHS_email_label.config(text=email, font="arial 16")
        self.RHS_username_label.grid(row=2, column=3)   
        self.RHS_email_label.grid(row=3, column=3)    

    def password_btn_clicked(self):
        if not(DB.is_empty()):
            entry_no = self.variable.get()[0] # e.g. '1. Runescape'
            password = DB.get_password(entry_no)
            pyperclip.copy(password)

            # text
            self.reset_labels()
            self.clipboard_label.grid(row=5, column=0, columnspan=2, sticky='w')
    
    def reset_RHS_conent(self):
        self.variable.set('...')
        drop = tk.OptionMenu(self, self.variable, '...')
        drop.grid(row=1, column=3) 
        self.RHS_username_label.config(text='*', font="arial 16")
        self.RHS_email_label.config(text='*', font="arial 16")
        self.RHS_username_label.grid(row=2, column=3)   
        self.RHS_email_label.grid(row=3, column=3)

    def reset_btn_clicked(self):
        self.confirmation_popup()

    def confirmation_popup(self):
        win = tk.Toplevel()
        win.wm_title("Confirmation Window")

        disclaimer = "Are you sure you want to delete ALL entries?"
        self.disclaimer_label = tk.Label(win, text=disclaimer)  
        
        self.yes_btn = tk.Button(win, text="YES", command=self.yes_btn_clicked and win.destroy )
        self.no_btn = tk.Button(win, text="NO", command=self.no_btn_clicked and win.destroy ) 

        if not(False):
            self.disclaimer_label.grid(row=0, column=0)
            self.yes_btn.grid(row=1, column=0)
            self.no_btn.grid(row=1, column=1)
    # confirmation popup button
    def yes_btn_clicked(self):
        if not(DB.is_empty()):
            DB.clear_table()
            self.reset_RHS_conent()
    def no_btn_clicked(self):
        print("yay")

    def reset_labels(self):
        self.incorrect_input_label.grid_forget()
        self.clipboard_label.grid_forget()
    
    def update_options_menu(self):
        pretty_options = []
        for entry in self.options:
            formatted_string = entry[0] + ". " + entry[1]
            pretty_options.append(formatted_string)

        drop = tk.OptionMenu(self, self.variable, *pretty_options, command=self.display_RHS)
        drop.grid(row=1, column=3)

    def create_widgets(self):
        ### left hand side (LHS) widgets ###
        # heading
        self.label_heading = tk.Label(self, text="Add entry", font='arial 24')
        self.label_heading.grid(row=0, column=0, sticky='w')
        # input fields
        self.title_label = tk.Label(self, text="Title: ", font='arial 16')
        self.title_entry = tk.Entry(self)
        self.title_label.grid(row=1, column=0)
        self.title_entry.grid(row=1, column=1)

        self.username_label = tk.Label(self, text="Username(opt): ", font="arial 16")
        self.username_entry = tk.Entry(self)
        self.username_label.grid(row=2, column=0)
        self.username_entry.grid(row=2, column=1)

        self.password_label = tk.Label(self, text="Password: ", font='arial 16')
        self.password_entry = tk.Entry(self, show='*')
        self.password_label.grid(row=3, column=0)
        self.password_entry.grid(row=3, column=1)   

        self.email_label = tk.Label(self, text="Email: ", font="arial 16")
        self.email_entry = tk.Entry(self)
        self.email_label.grid(row=4, column=0)
        self.email_entry.grid(row=4, column=1)    

        # submit button
        self.submit_btn = tk.Button(self, text="Submit", font='arial 16', command=self.submit_btn_clicked)
        self.submit_btn.grid(row=5, column=1, sticky='e') 

        # initialise clipboard and incorrect input label
        self.clipboard_label = tk.Label(self, text=f"copied to clipboard!", fg='green')
        self.incorrect_input_label = tk.Label(self, text=f"missing input", fg='red')   
             
        ### right hand side (RHS) widgets ###
        # heading
        self.label_heading2 = tk.Label(self, text="Accounts:", font='arial 24')
        self.label_heading2.grid(row=0, column=3, columnspan=2)

        # initialise labels
        self.RHS_username_label = tk.Label(self, text="*", font="arial 16") 
        self.RHS_email_label = tk.Label(self, text="*", font="arial 16")  
        self.RHS_username_label.grid(row=2, column=3)   
        self.RHS_email_label.grid(row=3, column=3)  

        # initialise option menu values
        self.options = DB.select_all_entry_no_and_title()
        self.variable = tk.StringVar()

        if not(DB.is_empty()):
            self.display_RHS(self.options[0]) # show the first username and email

            pretty_options = []
            for i in self.options:
                formatted_string = i[0] + ". " + i[1]
                pretty_options.append(formatted_string)

            self.variable.set(pretty_options[0]) # show first entry_no and title
            drop = tk.OptionMenu(self, self.variable, *pretty_options, command=self.display_RHS)
        else:
            self.variable.set('...')
            drop = tk.OptionMenu(self, self.variable, '...')

        drop.grid(row=1, column=3)

        # get password button
        self.password_btn = tk.Button(self, text="password", font='arial 16', command=self.password_btn_clicked)
        self.password_btn.grid(row=4, column=3)

        # reset database button
        self.reset_btn = tk.Button(self, text="reset", font='arial 12', command=self.reset_btn_clicked)
        self.reset_btn.grid(row=5, column=3)

        ### empty seperator coloumn ###
        self.empty_column = tk.Label(self, text=' '*10)
        self.empty_column.grid(row=0, column=2)
     
# entry to program
app = Application()
app.title("Password Manager")
app.iconbitmap('./images/icon.ico')
app.mainloop()