import tkinter as tk
from tkinter import font as tkfont 

import os
import configparser

"""Simple Password manager.

A simple password manager with two frames - login page and the password manager page.
Requires input in config.ini.
"""

### globals variables ###
CONFIG_FILE_PATH = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
MASTER_PASSWORD = config.get('LOGIN', 'master_password')

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
        self.on_submit_button = tk.Button(self, text="Submit",
                            command=self.on_submit)

        self.on_submit_button.grid(row=1, column=2)
    
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
        email = self.email_entry.get()
        password = self.password_entry.get()

        if (title == "" or email == "" or password == ""):
            self.incorrect_input_label.grid(row=4, column=0, columnspan=2, sticky='w')
        else:
            with open('passwords.txt', 'a') as f:
                f.write(f"{title}:\n {email}\n {password}\n\n")
            self.title_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.incorrect_input_label.grid_forget()

    def create_widgets(self):
        # heading
        self.label_heading = tk.Label(self, text="Add entry", font='arial 24')
        self.label_heading.grid(row=0, column=0, columnspan=2)
        ### input fields ###
        self.title_label = tk.Label(self, text="Title: ", font='arial 16')
        self.title_entry = tk.Entry(self)
        self.title_label.grid(row=1, column=0)
        self.title_entry.grid(row=1, column=1)

        self.email_label = tk.Label(self, text="Email: ", font="arial 16")
        self.email_entry = tk.Entry(self)
        self.email_label.grid(row=2, column=0)
        self.email_entry.grid(row=2, column=1)

        self.password_label = tk.Label(self, text="Password: ", font='arial 16')
        self.password_entry = tk.Entry(self, show='*')
        self.password_label.grid(row=3, column=0)
        self.password_entry.grid(row=3, column=1)       

        # submit button
        self.on_submit_buttom = tk.Button(self, text="Submit", font='arial 16', command=self.on_submit)
        self.on_submit_buttom.grid(row=4, column=1, sticky='e')   
        self.incorrect_input_label = tk.Label(self, text=f"empty input box/boxes.", fg='red')
     

# entry to program
def main():
    app = Application()
    app.title("Password Manager")
    app.mainloop()

if __name__ == '__main__':
    main()