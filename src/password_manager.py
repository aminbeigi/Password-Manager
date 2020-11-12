import tkinter as tk

# generate the user interface
class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def submit(self):
        print("The submit button has been pressed.")

    def create_widgets(self):
        # heading
        self.heading = tk.Label(root, text="Add entry")
        self.heading.pack()
        # input fields
        self.email = tk.Label(root, text="Email: ")
        self.email.pack()
        # submit button
        self.submit_buttom = tk.Button(root, text="Submit", command=self.submit)
        self.submit_buttom.pack()


root = tk.Tk()
app = Application(root)
app.mainloop()