import tkinter as tk

# generate the user interface
class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def submit(self):
        print(self.input_email.get())

    def create_widgets(self):
        # heading
        self.label_heading = tk.Label(root, text="Add entry")
        self.label_heading.grid(row=0, column=0)
        # input fields
        self.label_email = tk.Label(root, text="Email: ")
        self.label_email.grid(row=1, column=0)
        self.input_email = tk.Entry(root)
        self.input_email.grid(row=1, column=1)


        # submit button
        self.submit_buttom = tk.Button(root, text="Submit", command=self.submit)
        self.submit_buttom.grid(row=99, column=99)


root = tk.Tk()
app = Application(root)
app.mainloop()