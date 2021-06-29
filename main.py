# Import relevant modules
from tkinter import *
import os, pickle

# Create application frame


class Application(Frame):
    """A GUI Application Frame to contain the primary menu navigation."""

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()

    def first_time(self):
        self.wel_lbl = Label(self,
                             text="I've noticed this is your first time using my Degree Progress Tracker.\n" +
                                  "Please input your degree information below:",
                             font="Helvetica 15"
                             )
        self.wel_lbl.grid(row=0, column=1, padx=90, pady=100, columnspan=7)

        self.course_name_entry_lbl = Label(self,
                                           text="Course Name",
                                           font="Helvetica 14"
                                           )
        self.course_name_entry_lbl.grid(row=1, column=4, sticky=W)

        self.course_name_entry = Entry(self, width=50)
        self.course_name_entry.grid(row=1, column=5, sticky=W)

        self.course_maxcreds_entry_lbl = Label(self,
                                               text="Maximum Course Credits",
                                               font="Helvetica 14"
                                               )
        self.course_maxcreds_entry_lbl.grid(row=2, column=4, sticky=W)

        self.course_maxcreds_entry = Entry(self, width=50)
        self.course_maxcreds_entry.grid(row=2, column=5, sticky=W)

        self.submit_course_info_bttn = Button(self, text="Submit", command=self.close_setup, width=42)
        self.submit_course_info_bttn.grid(row=3, column=5, sticky=W)

        self.setup_error_lbl = Label(self, font="Helvetica 12", fg="red")

    def close_setup(self):
        if len(self.course_name_entry.get()) < 41:
            try:
                courseData = (self.course_name_entry.get(), int(self.course_maxcreds_entry.get()))
                f_writeCourseData = open(direct + "courseData.dat", "wb")
                pickle.dump(courseData, f_writeCourseData)
                f_writeCourseData.close()
                self.wel_lbl.grid_remove()
                self.course_name_entry.grid_remove()
                self.course_name_entry_lbl.grid_remove()
                self.course_maxcreds_entry_lbl.grid_remove()
                self.course_maxcreds_entry.grid_remove()
                self.submit_course_info_bttn.grid_remove()
                self.setup_error_lbl.grid_remove()
            except ValueError:
                self.setup_entry_error("credits_error")
        else:
            self.setup_entry_error("name_error")

    def setup_entry_error(self, errortype):

        if errortype == "credits_error":
            self.setup_error_lbl.config(text="Maximum Credits must be an integer value")
            self.setup_error_lbl.grid(row=4, column=3, columnspan=3)
        elif errortype == "name_error":
            self.setup_error_lbl.config(text="Degree name must be 40 characters or less")
            self.setup_error_lbl.grid(row=4, column=3, columnspan=3)
# main program

# create directory


direct = ""
try:
    os.mkdir(os.environ['USERPROFILE'] + "\\Documents\\DegreeTracker\\")
    direct = os.environ['USERPROFILE'] + "\\Documents\\DegreeTracker\\"
except FileExistsError:
    direct = os.environ['USERPROFILE'] + "\\Documents\\DegreeTracker\\"

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
root.geometry("800x400")
root.resizable(False, False)
mainApp = Application(root)

# Invoke first time setup sequence

if firstTime == True:
    mainApp.first_time()

root.mainloop()
