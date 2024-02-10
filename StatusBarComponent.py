from tkinter import Label

class StatusBarComponent:
    def __init__(self, master):
        self.status_bar = Label(master, text="Ready", bd=1, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def update_status(self, message):
        self.status_bar.config(text=message)
