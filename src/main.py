import tkinter as tk
from tkinter import font as tkfont 
import configparser
import pyperclip
# local files
import database

"""Simple Password manager.

A simple password manager with two frames - login page and the main page.
Requires input in config.ini. 
The two frames are stacked on top of each other, once the correct password is inputted
the main page is raised above the login page. The frame on top will be the frame that is visible.
"""

### globals variables ###
CONFIG_FILE_PATH = 'config.ini'
config = configparser.ConfigParser() # TO-DO: TRY CATCH error here to see if found config
config.read(CONFIG_FILE_PATH)
MASTER_PASSWORD = config.get('LOGIN', 'master_password')

DB = database.Database() # initialise database

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold', slant='italic')

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
        
        ### input fields ###
        self.login_label = tk.Label(self, text="Key Password: ", font=controller.title_font)
        self.login_entry = tk.Entry(self, show='*')
        self.login_label.grid(row=0, column=0)
        self.login_entry.grid(row=0, column=1)

        # submit button
        self.on_submit_btn = tk.Button(self, text="Submit",
                            command=self.on_submit)

        self.on_submit_btn.grid(row=1, column=2)
    
    def on_submit(self):
        password = self.login_entry.get()
        if (password == MASTER_PASSWORD):
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

    def on_submit(self):
        title = self.title_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        # correct input
        if (title != "" and email != "" and password != ""):
            DB.insert(title, username, password, email)

            self.title_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.incorrect_input_label.grid_forget()
        # missing input
        else:
            self.incorrect_input_label.grid(row=5, column=0, columnspan=2, sticky='w')
        
    def show_account(self, value):
        data = DB.get_entry(entry_no=str(value[0]))
        title = data[0][1]
        username = data[0][2]
        email = data[0][4]

        # change labels
        self.show_title_label.config(text=title, font="arial 16")
        self.show_username_label.config(text=username, font="arial 16")
        self.show_email_label.config(text=email, font="arial 16")

 

        self.show_title_label.grid(row=2, column=3)   
        self.show_username_label.grid(row=3, column=3)   
        self.show_email_label.grid(row=4, column=3)        

    def create_widgets(self):
        # heading
        self.label_heading = tk.Label(self, text="Add entry", font='arial 24')
        self.label_heading.grid(row=0, column=0, columnspan=2)
        ### input fields ###
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
        self.on_submit_btn = tk.Button(self, text="Submit", font='arial 16', command=self.on_submit)
        self.on_submit_btn.grid(row=5, column=1, sticky='e')   
        self.incorrect_input_label = tk.Label(self, text=f"empty input box/boxes.", fg='red')

        ### empty seperator coloumn
        self.empty_column = tk.Label(self, text="----------")
        self.empty_column.grid(row=0, column=2)       

        ### stuff on the right ###
        # initial values
        self.show_title_label = tk.Label(self, text="*", font="arial 16")
        self.show_username_label = tk.Label(self, text="*", font="arial 16") 
        self.show_email_label = tk.Label(self, text="*", font="arial 16")  

        self.show_title_label.grid(row=2, column=3)   
        self.show_username_label.grid(row=3, column=3)   
        self.show_email_label.grid(row=4, column=3)   

        # title
        self.label_heading2 = tk.Label(self, text="Accounts:", font='arial 24')
        self.label_heading2.grid(row=0, column=3, columnspan=2)
        # dropdown menu
        DB.select_entries()
        self.options = DB.select_entries()

        drop_var = tk.StringVar()
        drop_var.set(self.options[0])

        drop = tk.OptionMenu(self, drop_var, *self.options, command=self.show_account)
        drop.grid(row=1, column=3)   

        # get password
        self.on_get_password_btn = tk.Button(self, text="get password", font='arial 16')
        self.on_get_password_btn.grid(row=5, column=3, sticky='w')   
     
# entry to program
def main():
    # add an icon
    app = Application()
    app.title("Password Manager")
    app.mainloop()

if __name__ == '__main__':
    main()