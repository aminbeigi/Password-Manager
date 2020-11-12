import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        
        super().__init__(master)
        
        self.create_widgets()
        print("I've been made")
    
    def create_widgets(self):
        # heading
        self.label = tk.Label(root, text="Add entry")
        self.label.pack()
        # submit button
        self.my_button = tk.Button(root, text="Submit")
        self.my_button.pack()


root = tk.Tk()
app = Application(root)
app.mainloop()