from login import LoginView

from tkinter import Tk, ttk

class UI:
    def __init__(self, root):
        self._root = root

    def start(self):
        label = ttk.Label(master=self._root, text="Hello world!")

        label.pack()

window = Tk()

window.title("TkInter example")

ui = UI(window)

ui.start()

window.mainloop()