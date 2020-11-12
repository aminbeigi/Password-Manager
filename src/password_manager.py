import tkinter as tk

# global variables
root = tk.Tk()

# generate the user interface

#class LoginPage(tk.Frame):
#    def __init__(self)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def submit(self):
        title = self.title_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        print(title, email, password)
        root.destroy()
        
        

    def create_widgets(self):
        # heading
        self.label_heading = tk.Label(root, text="Add entry", font="arial 24")
        self.label_heading.grid(row=0, column=0)
        ### input fields ###
        self.title_label = tk.Label(root, text="Title: ", font="arial 16")
        self.title_label.grid(row=1, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=1, column=1)

        self.email_label = tk.Label(root, text="Email: ", font="arial 16")
        self.email_label.grid(row=2, column=0)
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=2, column=1)

        self.password_label = tk.Label(root, text="Password: ", font="arial 16")
        self.password_label.grid(row=3, column=0)
        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.grid(row=3, column=1)       

        # submit button
        self.submit_buttom = tk.Button(root, text="Submit", font="arial 16", command=self.submit)
        self.submit_buttom.grid(row=99, column=99)

# entry to program
def main():
    root.title("Password Manager")
    app = Application(root)
    app.mainloop()
 
if __name__ == '__main__':
    main()