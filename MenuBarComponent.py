from tkinter import Menu


class MenuBarComponent:
    def __init__(self, master, on_open, on_exit):
        self.menubar = Menu(master)
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Open", command=on_open)
        file_menu.add_command(label="Exit", command=on_exit)
        self.menubar.add_cascade(label="File", menu=file_menu)
        master.config(menu=self.menubar)
