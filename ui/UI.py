import shutil
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

        main_frame = Frame(self, width=500, height=500)
        main_frame.place(relx=0.5, rely=0.3, anchor='center')
        # main_grid.pack(fill="both", padx=20, pady=20)

        ## Open file button stuff
        # Frame
        open_button_frame = Frame(main_frame, width=500, height=100)
        open_button_frame.grid(row=0, column=0, padx=UI.center_pad(main_frame, open_button_frame), pady=20)
        # Button
        open_button = Button(open_button_frame, text='Select File', command=self.select_file)
        open_button.grid(row=0, column=0, padx=UI.center_pad(open_button_frame, open_button), pady=5)
        # Label text under button
        if not hasattr(self, "file") or self.file == None or self.file == "":
            open_button_text = "No file selected"
        else:
            open_button_text = self.file
        self.open_button_label = Label(open_button_frame, text=open_button_text)
        self.open_button_label.grid(row=1, column=0, padx=UI.center_pad(open_button_frame, self.open_button_label), pady=5)


        # path_button = Button(main_frame, text='Select Output Folder', command=self.select_folder)
        # path_button.grid(row=1, column=0, padx=UI.center_pad(main_frame, path_button), pady=0)

        # Start button stuff
        start_button_frame = Frame(main_frame, width=500, height=100)
        start_button_frame.grid(row=1, column=0, padx=UI.center_pad(main_frame, start_button_frame), pady=20)
        start_button = Button(start_button_frame, text='Start', command=self.assign_reviewers)
        start_button.grid(row=0, column=0, padx=UI.center_pad(main_frame, start_button), pady=0)
        # Error text label under button (if exists)
        self.start_err_label = Label(start_button_frame, text="")
        self.start_err_label.grid(row=1, column=0, padx=UI.center_pad(start_button_frame, self.start_err_label), pady=5)

        # Example sheet stuff
        example_button_frame = Frame(main_frame, width=500, height=100)
        example_button_frame.grid(row=2, column=0, padx=UI.center_pad(main_frame, example_button_frame), pady=20)
        example_button = Button(example_button_frame, text='Create Example File', command=self.save_example)
        example_button.grid(row=0, column=0, padx=UI.center_pad(main_frame, example_button), pady=0)
        # Error text label under example sheet button (if exists)
        self.example_err_label = Label(example_button_frame, text="")
        self.example_err_label.grid(row=1, column=0, padx=UI.center_pad(start_button_frame, self.example_err_label), pady=5)
        return
    
    def center_pad(widget1: Widget, widget2: Widget):
        return (widget1.winfo_width() - widget2.winfo_width()) // 2
    
    """ 
    Redraws the UI screen
    """
    def draw(self):
        pass
        
    
    def select_file(self):
        self.file = fd.askopenfilename() # TODO: specify file type

        if hasattr(self, "file") and not (self.file == None or self.file == ""):
            if (len(self.file) >= 85):
                open_button_text = "..." + self.file[-75:]
            else:
                open_button_text = self.file
        else:
            open_button_text = "No file selected"
        self.open_button_label.config(text=open_button_text)
        self.update()
        return

    def assign_reviewers(self):
        # Refresh error messages
        self.errmsg = ""
        self.start_err_label.config(text=self.errmsg)
        self.update()

        # check if no file selected
        if not hasattr(self, "file") or self.file == None or self.file == "":
            self.errmsg = "No file selected"
            self.start_err_label.config(text=self.errmsg)
            self.update()
            return
        self.controller.assign_reviewers(open(self.file, mode='r'))
        return

    def start(self):
        self.mainloop()
        self.close()
        return

    def close(self):
        exit(0)

    # Adds a controller to this UI instance
    def add_controller(self, controller: ControllerInterface):
        self.controller = controller

    # Save a copy of the example file to specified location 
    # Should really be its own use case, but I'm lazy
    def save_example(self):
        example_file_path = "./datafiles/example_sheet.xlsx"
        example_file = open(example_file_path, 'rb')
        # TODO: do error if cannot open file
        # filedialogue to get save to location
        save_location = fd.asksaveasfile(mode="wb", filetypes=[("Microsoft Excel spreadsheet", "*.xlsx")], defaultextension=[("Microsoft Excel spreadsheet", "*.xlsx")])
        if (save_location == None):
            return
        # attempt to save
        shutil.copyfileobj(example_file, save_location)
        # TODO: do error if saving is unsuccessful
        return 



