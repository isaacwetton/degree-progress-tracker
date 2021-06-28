# Import relevant modules
from tkinter import *
import os


# Create application frame


class Application(Frame):
    """A GUI Application Frame to contain the primary menu navigation."""

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()

    def first_time(self):
        self.wel_lbl = Label(self,
                             text="We've noticed this is your first time using our Degree Progress Tracker.\n" +
                                  "Please input your degree information below:",
                             font="Helvetica 15 bold"
                             )
        self.wel_lbl.grid(row=0, column=1, columnspan=3, sticky=S)
        self.wel_lbl.config(anchor=CENTER)
        self.wel_lbl.pack()

# main program

# create directory


direct = ""
try:
    os.mkdir(os.environ['USERPROFILE'] + "\\Documents\\PythonTest\\")
    direct = os.environ['USERPROFILE'] + "\\Documents\\PythonTest\\"
except FileExistsError:
    direct = os.environ['USERPROFILE'] + "\\Documents\\PythonTest\\"

# Determine if first-time use
try:
    f_courseData = open(direct + "courseData.dat", "rb+")
    firstTime = False
except IOError:
    # os.remove(direct + "courseData.dat")
    firstTime = True

# Create root and main application window
root = Tk()
root.title("Degree Progress Tracker")
root.geometry("800x600")
mainApp = Application(root)

# Invoke first time setup sequence

if firstTime == True:
    mainApp.first_time()

root.mainloop()
