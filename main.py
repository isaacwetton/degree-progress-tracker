
# Import relevant modules
from tkinter import *

# Create application frame

class Application(Frame):
    """A GUI Application Frame to contain the primary menu navigation."""
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()

# main program

root = Tk()
root.title("Degree Progress Tracker")
root.geometry("800x600")
mainapp = Application(root)
root.mainloop()
