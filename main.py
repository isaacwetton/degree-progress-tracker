# Import relevant modules
import os
import webbrowser
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

        self.main_courseinfo_bttn = Button(self, text="View Course Info & Stats", width=42, height=2,
                                           command=self.course_info_menu)
        self.main_createmodule_bttn = Button(self, text="Create Module", width=42, height=2,
                                             command=self.create_module_menu)
        self.main_addwork_bttn = Button(self, text="Add a Piece of Work", width=42, height=2)
        self.main_viewmodule_bttn = Button(self, text="View a Module's Info", width=42, height=2)
        self.main_about_bttn = Button(self, text="About", width=42, height=2,
                                      command=self.about_page)
        self.main_courseinfo_bttn.grid(row=3, column=4, pady=5)
        self.main_createmodule_bttn.grid(row=4, column=4, pady=5)
        self.main_addwork_bttn.grid(row=5, column=4, pady=5)
        self.main_viewmodule_bttn.grid(row=6, column=4, pady=5)
        self.main_about_bttn.grid(row=7, column=4, pady=5)

    def clear_main_menu(self):
        """Closes the main menu"""
        self.main_title_lbl.grid_forget()
        self.main_credit_lbl.grid_forget()
        self.main_courseinfo_bttn.grid_forget()
        self.main_createmodule_bttn.grid_forget()
        self.main_addwork_bttn.grid_forget()
        self.main_viewmodule_bttn.grid_forget()
        self.main_about_bttn.grid_forget()

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

    def create_module_menu(self):
        """Opens menu for adding a module"""
        self.clear_main_menu()
        self.create_module_home_bttn = Button(self,
                                           text="Home",
                                           width=10,
                                           height=2,
                                           command=self.create_module_home
                                           )
        self.create_module_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.create_module_title_lbl = Label(self,
                                      text="Create Module",
                                      font="Helvetica 30")
        self.create_module_title_lbl.grid(row=0, column=2, columnspan=7, padx=170, pady=(0,80))

        self.create_module_name_lbl = Label(self,
                                           text="Module Name",
                                           font="Helvetica 13")
        self.create_module_name_lbl.grid(row=1, column=3, sticky=W)
        self.create_module_name_entry = Entry(self, width=50)
        self.create_module_name_entry.grid(row=1, column=4)

        self.create_module_maxcredits_lbl = Label(self,
                                                  text="Maximum Available Credits",
                                                  font="Helvetica 13")
        self.create_module_maxcredits_lbl.grid(row=2, column=3, sticky=W)
        self.create_module_maxcredits_entry = Entry(self, width=50)
        self.create_module_maxcredits_entry.grid(row=2, column=4)

        self.create_module_submit_bttn = Button(self,
                                                text="Create Module",
                                                width=42)
        self.create_module_submit_bttn.grid(row=3, column=4)

    def create_module_home(self):
        """Goes back to main menu from module creation menu"""
        self.create_module_home_bttn.grid_forget()
        self.create_module_title_lbl.grid_forget()
        self.create_module_name_lbl.grid_forget()
        self.create_module_name_entry.grid_forget()
        self.create_module_maxcredits_lbl.grid_forget()
        self.create_module_maxcredits_entry.grid_forget()
        self.create_module_submit_bttn.grid_forget()
        self.main_menu()

    def about_page(self):
        """Displays information page about the application"""
        self.clear_main_menu()
        self.about_home_bttn = Button(self,
                                              text="Home",
                                              width=10,
                                              height=2,
                                              command=self.about_home
                                              )
        self.about_home_bttn.grid(row=0, column=0, padx=10, pady=5)

        self.about_text1_lbl = Label(self,
                                             text="This application was created by Isaac Wetton. " \
                                                  + "It is designed to assist with the organisation\nand tracking of " \
                                                  + "a university degree's progress. The app allows for the creation " \
                                                  + "of modules\nand worksheet which can then be assigned to those " \
                                                  + "modules. \n\nEach module and worksheet's average marks and " \
                                                  + "grades can be tracked, as well as overall\nprogress." \
                                                  + "The app makes the assumption that 40% is a third class, 50% is " \
                                                  + "a 2:2, 60% is a 2:1\nand 70% is a first class degree.\n\n" \
                                                  + "The course data for this program is stored in the directory "
                                                  + "User\Documents\DegreeTracker\.\nIf the program stops working " \
                                                  + "at any point, it can be reset by deleting this directory and " \
                                                  + "its\ncontents.\n\nThis is the first GUI program I have created " \
                                                  + "with Python so please appreciate there may be some\nissues. " \
                                                  + "Bugs and other problems can be reported on the GitHub page " \
                                                  + "below.",
                                             font="Helvetica 13",
                                             justify=LEFT)
        self.about_text1_lbl.grid(row=1, column=0, columnspan=7, pady=10, padx=50)

        self.about_github_bttn = Button(self, text="degree-progress-tracker GitHub Project",
                                        width=50, height=1, command=self.githublink)
        self.about_github_bttn.grid(row=2, column=2, padx=20)

    def about_home(self):
        """Goes back to main menu from about page"""
        self.about_home_bttn.grid_forget()
        self.about_text1_lbl.grid_forget()
        self.about_github_bttn.grid_forget()
        self.main_menu()

    def githublink(self):
        """Opens the application's Github repos"""
        webbrowser.open_new("https://github.com/isaacwetton/degree-progress-tracker/")

    def shelve_modules(self):
        """Collects all modules and stores them in the file system"""
        global modules
        global works
        f_modules = shelve.open(direct + "moduleWorkLists.dat", "n")
        for module in modules:
            f_modules[module] = module.works
        f_modules.sync()
        f_modules.close()

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
    f_courseData.close()
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
