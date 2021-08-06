# Import relevant modules
import os
from degreeobjects import *
from tkinter import *


# Create application frame


class Application(Frame):
    """A GUI Application Frame to contain the primary menu navigation."""

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()

    def first_time(self):
        """Initiates first time setup menu"""

        self.wel_lbl = Label(self,
                             text="I've noticed this is your first time using my Degree Progress Tracker.\n" +
                                  "Please input your degree information below:",
                             font="Helvetica 15"
                             )
        self.wel_lbl.grid(row=0, column=1, padx=90, pady=100, columnspan=7)

        self.course_name_entry_lbl = Label(self,
                                           text="Course Name",
                                           font="Helvetica 13")
        self.course_name_entry_lbl.grid(row=1, column=4, sticky=W)

        self.course_name_entry = Entry(self, width=50)
        self.course_name_entry.grid(row=1, column=5, sticky=W)

        self.course_maxcreds_entry_lbl = Label(self,
                                               text="Maximum Course Credits",
                                               font="Helvetica 13"
                                               )
        self.course_maxcreds_entry_lbl.grid(row=2, column=4, sticky=W)

        self.course_maxcreds_entry = Entry(self, width=50)
        self.course_maxcreds_entry.grid(row=2, column=5, sticky=W)

        self.submit_course_info_bttn = Button(self, text="Submit", command=self.close_setup, width=42)
        self.submit_course_info_bttn.grid(row=3, column=5, sticky=W)

        self.setup_error_lbl = Label(self, font="Helvetica 12", fg="red")

    def close_setup(self):
        """Validates inputs, saves data and closes setup menu"""
        if len(self.course_name_entry.get()) < 41:
            if self.course_name_entry.get() == "":
                self.setup_entry_error("nameblank_error")
            else:
                try:
                    courseData = (self.course_name_entry.get(), int(self.course_maxcreds_entry.get()))
                    f_writeCourseData = open(direct + "courseData.dat", "wb")
                    pickle.dump(courseData, f_writeCourseData, True)
                    f_writeCourseData.close()
                    f_moduleWorkLists = open(direct + "moduleWorkLists.dat", "wb")
                    f_moduleWorkLists.close()
                    self.wel_lbl.grid_remove()
                    self.course_name_entry.grid_remove()
                    self.course_name_entry_lbl.grid_remove()
                    self.course_maxcreds_entry_lbl.grid_remove()
                    self.course_maxcreds_entry.grid_remove()
                    self.submit_course_info_bttn.grid_remove()
                    self.setup_error_lbl.grid_remove()
                    self.main_menu()
                except ValueError:
                    self.setup_entry_error("credits_error")
        else:
            self.setup_entry_error("namelength_error")

    def setup_entry_error(self, errortype):
        """Responds to setup menu validation error"""
        if errortype == "credits_error":
            self.setup_error_lbl.config(text="Maximum Credits must be an integer value")
        elif errortype == "namelength_error":
            self.setup_error_lbl.config(text="Degree name must be 40 characters or less")
        elif errortype == "nameblank_error":
            self.setup_error_lbl.config(text="You must enter a degree name")
        self.setup_error_lbl.grid(row=4, column=3, columnspan=3)

    def main_menu(self):
        """Opens the main menu of the application"""

        self.main_title_lbl = Label(self,
                                    text="Degree Progress Tracker",
                                    font="Helvetica 25")
        self.main_title_lbl.grid(row=0, column=1, columnspan=7, padx=220)

        self.main_credit_lbl = Label(self,
                                     text="by Isaac Wetton",
                                     font="Helvetica 12")
        self.main_credit_lbl.grid(row=1, column=3, columnspan=4, pady=5)

        self.main_courseinfo_bttn = Button(self, text="View Course Info & Stats", width=42, height=3,
                                           command=self.course_info_menu)
        self.main_createmodule_bttn = Button(self, text="Create Module", width=42, height=3)
        self.main_addwork_bttn = Button(self, text="Add a Piece of Work", width=42, height=3)
        self.main_viewmodule_bttn = Button(self, text="View a Module's Info", width=42, height=3)
        self.main_courseinfo_bttn.grid(row=3, column=4, pady=5)
        self.main_createmodule_bttn.grid(row=4, column=4, pady=5)
        self.main_addwork_bttn.grid(row=5, column=4, pady=5)
        self.main_viewmodule_bttn.grid(row=6, column=4, pady=5)

    def clear_main_menu(self):
        """Closes the main menu"""
        self.main_title_lbl.grid_forget()
        self.main_credit_lbl.grid_forget()
        self.main_courseinfo_bttn.grid_forget()
        self.main_createmodule_bttn.grid_forget()
        self.main_addwork_bttn.grid_forget()
        self.main_viewmodule_bttn.grid_forget()

    def course_info_menu(self):
        """Opens course info menu"""
        self.clear_main_menu()
        # Open relevant files
        f_readCourseData = open(direct + "courseData.dat", "rb")
        courseData = pickle.load(f_readCourseData)
        f_readCourseData.close()

        # Create course info menu

        self.courseinfo_home_bttn = Button(self,
                                          text="Home",
                                          width=10,
                                          height=2,
                                          command=self.courseinfo_home
        )
        self.courseinfo_home_bttn.grid(row=0, column=0, padx=10)

        self.course_title_lbl = Label(self,
                                      text="Course Info",
                                      font="Helvetica 30")
        self.course_title_lbl.grid(row=0, column=2, columnspan=7, padx=200)

        self.course_name_lbl = Label(self,
                                     text="Course name: " + courseData[0],
                                     font="Helvetica 12")
        self.course_name_lbl.grid(row=1, column=3, columnspan=2)

    def courseinfo_home(self):
        """Goes back to main menu from course info page"""
        self.courseinfo_home_bttn.grid_forget()
        self.course_title_lbl.grid_forget()
        self.course_name_lbl.grid_forget()
        self.main_menu()

# main program

# create module and work lists
modules = []
works = []

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

# Invoke first time setup sequence if required

if firstTime == True:
    mainApp.first_time()
else:
    mainApp.main_menu()
root.mainloop()
