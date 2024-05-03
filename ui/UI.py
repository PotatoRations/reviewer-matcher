from tkinter import *
from controllers.ControllerInterface import ControllerInterface
from ui.UIInterface import UIInterface 
from tkinter import filedialog as fd

class UI(Tk, UIInterface):
    def __init__(self) -> None:
        super().__init__()
        self.resizable(False, False)
        self.geometry("500x500")
        self.title("Reviewer Matcher")

        open_button = Button(self, text='Select File', command=self.select_file)
        open_button.pack(expand=True)

        return
    
    def select_file(self):
        f = fd.askopenfile()
        self.controller.assign_reviewers(f)

    def start(self):
        self.mainloop()
        self.close()
        return

    def close(self):
        exit(0)

    # Adds a controller to this UI instance
    def add_controller(self, controller: ControllerInterface):
        self.controller = controller



