# Import relevant modules
import os
import webbrowser
from tkinter import *
from tkinter import ttk
import pickle

# Create application frame

class Work(object):
    """A piece of university work (Coursework or Exam)"""

    def __init__(self, name, work_type, score, percentage_module):
        global works
        self.name = name
        self.work_type = work_type
        self.score = score
        self.percentage_module = percentage_module

    def __str__(self):
        rep = self.name + "\n"
        rep += "Type: " + self.work_type + "\n"
        rep += "Score (%): " + str(self.score) + "\n"
        rep += "Percentage of module: " + str(self.percentage_module) + "\n"
        return rep


class Module(object):
    """A degree module"""

    def __init__(self, name, max_credits, exam_credits, coursework_credits):
        self.name = name
        self.max_credits = max_credits
        self.exam_credits = exam_credits
        self.coursework_credits = coursework_credits
        self.works = {}

    def __str__(self):
        rep = "Module: " + self.name + "\n"
        rep += "Max Credits: " + self.max_credits + "\n"
        rep += "Percentage exam: " + self.exam_credits + "\n"
        rep += "Percentage coursework: " + self.coursework_credits + "\n"
        return rep

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
                    courseName = self.course_name_entry.get()
                    courseCredits = int(self.course_maxcreds_entry.get())
                    if courseCredits <= 0:
                        self.setup_entry_error("negativecreds_error")
                    else:
                        courseData = (courseName, courseCredits)
                        f_writeCourseData = open(direct + "courseData.dat", "wb")
                        pickle.dump(courseData, f_writeCourseData, True)
                        f_writeCourseData.close()
                        f_modulesData = open(direct + "modulesData.dat", "wb")
                        modules = {}
                        pickle.dump(modules, f_modulesData, True)
                        f_modulesData.close()
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
        elif errortype == "negativecreds_error":
            self.setup_error_lbl.config(text="Credits must be positive and above 0")
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
        self.main_addwork_bttn = Button(self, text="Add a Piece of Work", width=42, height=2,
                                        command=self.addwork_validate_access)
        self.main_viewmodule_bttn = Button(self, text="View a Module's Info", width=42, height=2,
                                           command=self.viewmodule_validate_access)
        self.main_about_bttn = Button(self, text="About", width=42, height=2,
                                      command=self.about_page)
        self.main_courseinfo_bttn.grid(row=3, column=4, pady=5)
        self.main_createmodule_bttn.grid(row=4, column=4, pady=5)
        self.main_addwork_bttn.grid(row=5, column=4, pady=5)
        self.main_viewmodule_bttn.grid(row=6, column=4, pady=5)
        self.main_about_bttn.grid(row=7, column=4, pady=5)

        self.main_redtext = Label(self, font="Helvetica 12", fg="red")

    def main_edit_redtext(self, displaytext):
        """Edits and displays the red text on the main menu"""
        self.main_redtext.configure(text=displaytext)
        self.main_redtext.grid(row=8, column=4)

    def clear_main_menu(self):
        """Closes the main menu"""
        self.main_title_lbl.grid_forget()
        self.main_credit_lbl.grid_forget()
        self.main_courseinfo_bttn.grid_forget()
        self.main_createmodule_bttn.grid_forget()
        self.main_addwork_bttn.grid_forget()
        self.main_viewmodule_bttn.grid_forget()
        self.main_about_bttn.grid_forget()
        self.main_redtext.grid_forget()

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
                                           font="Helvetica 13 bold",
                                           width=8,
                                           height=1,
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
        self.course_name_lbl.grid(row=1, column=2, columnspan=6)

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
                                              font="Helvetica 13 bold",
                                              width=8,
                                              height=1,
                                              command=self.create_module_home
                                              )
        self.create_module_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.create_module_title_lbl = Label(self,
                                             text="Create Module",
                                             font="Helvetica 30")
        self.create_module_title_lbl.grid(row=0, column=2, columnspan=7, padx=170, pady=(0, 80))

        self.create_module_name_lbl = Label(self,
                                            text="Module Name",
                                            font="Helvetica 13")
        self.create_module_name_lbl.grid(row=1, column=3, sticky=W)
        self.create_module_name_entry = Entry(self, width=50)
        self.create_module_name_entry.grid(row=1, column=4)

        self.create_module_examcreds_lbl = Label(self,
                                                 text="Percentage Exam (%)",
                                                 font="Helvetica 13")
        self.create_module_examcreds_lbl.grid(row=2, column=3, sticky=W)
        self.create_module_examcreds_entry = Entry(self, width=50)
        self.create_module_examcreds_entry.grid(row=2, column=4)

        self.create_module_courseworkcreds_lbl = Label(self,
                                                       text="Percentage Coursework (%)",
                                                       font="Helvetica 13")
        self.create_module_courseworkcreds_lbl.grid(row=3, column=3, sticky=W)
        self.create_module_courseworkcreds_entry = Entry(self, width=50)
        self.create_module_courseworkcreds_entry.grid(row=3, column=4)

        self.create_module_maxcreds_lbl = Label(self,
                                                text="Maximum Available Credits",
                                                font="Helvetica 13")
        self.create_module_maxcreds_lbl.grid(row=4, column=3, sticky=W)
        self.create_module_maxcreds_entry = Entry(self, width=50)
        self.create_module_maxcreds_entry.grid(row=4, column=4)

        self.create_module_submit_bttn = Button(self,
                                                text="Create Module",
                                                width=42,
                                                command=self.create_module_validation)
        self.create_module_submit_bttn.grid(row=5, column=4)

        self.create_module_error_lbl = Label(self, font="Helvetica 12", fg="red")

    def create_module_home(self):
        """Goes back to main menu from module creation menu"""
        self.create_module_home_bttn.grid_forget()
        self.create_module_title_lbl.grid_forget()
        self.create_module_name_lbl.grid_forget()
        self.create_module_name_entry.grid_forget()
        self.create_module_examcreds_lbl.grid_forget()
        self.create_module_examcreds_entry.grid_forget()
        self.create_module_courseworkcreds_lbl.grid_forget()
        self.create_module_courseworkcreds_entry.grid_forget()
        self.create_module_maxcreds_lbl.grid_forget()
        self.create_module_maxcreds_entry.grid_forget()
        self.create_module_submit_bttn.grid_forget()
        self.create_module_error_lbl.grid_forget()
        self.main_menu()

    def create_module_validation(self):
        """Validates inputted information when creating a module"""
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        if self.create_module_name_entry.get() in modules:
            self.create_module_error("moduleExists")
        else:
            if self.create_module_name_entry.get() != "":
                if len(self.create_module_name_entry.get()) < 51:
                    try:
                        examPercent = float(self.create_module_examcreds_entry.get())
                        courseworkPercent = float(self.create_module_courseworkcreds_entry.get())
                        if 0 <= examPercent <= 100 and 0 <= courseworkPercent <= 100:
                            if examPercent + courseworkPercent == 100:
                                try:
                                    maxCreds = int(self.create_module_maxcreds_entry.get())
                                    if maxCreds > 0:
                                        self.create_module()
                                    else:
                                        self.create_module_error("maxCredsNegative")
                                except ValueError:
                                    self.create_module_error("maxCredsInt")
                            else:
                                self.create_module_error("%add")
                        else:
                            self.create_module_error("%range")
                    except ValueError:
                        self.create_module_error("%value")
                else:
                    self.create_module_error("namelength")
            else:
                self.create_module_error("nameblank")

    def create_module_error(self, errortype):
        """Shows an error message if module creation validation fails"""
        if errortype == "nameblank":
            self.create_module_error_lbl.configure(text="Your module name cannot be blank")
        elif errortype == "namelength":
            self.create_module_error_lbl.configure(text="Your module name cannot exceed 50 characters")
        elif errortype == "%value":
            self.create_module_error_lbl.configure(text="Percentages must be given as numbers")
        elif errortype == "%range":
            self.create_module_error_lbl.configure(text="Percentages must be between 0 and 100")
        elif errortype == "%add":
            self.create_module_error_lbl.configure(text="The two percentages must add to 100")
        elif errortype == "maxCredsInt":
            self.create_module_error_lbl.configure(text="The maximum credits must be given as an integer value")
        elif errortype == "maxCredsNegative":
            self.create_module_error_lbl.configure(text="Maximum credits cannot be negative or zero")
        elif errortype == "moduleExists":
            self.create_module_error_lbl.configure(text="A module of that name already exists")
        self.create_module_error_lbl.grid(row=6, column=3, pady=(5, 0), columnspan=2)

    def create_module(self):
        """Creates a module object using the given info and stores it in the file system"""
        moduleName = self.create_module_name_entry.get()
        examPercent = float(self.create_module_examcreds_entry.get())
        courseworkPercent = float(self.create_module_courseworkcreds_entry.get())
        maxCreds = int(self.create_module_maxcreds_entry.get())
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        f_modulesData = open(direct + "modulesData.dat", "wb")
        modules[moduleName] = Module(moduleName, maxCreds, examPercent, courseworkPercent)
        pickle.dump(modules, f_modulesData, True)
        f_modulesData.close()
        self.create_module_home()
        self.main_edit_redtext("Module " + moduleName + " created")

    def addwork_validate_access(self):
        """Check if any modules exist, and if so allow access to the addwork menu"""
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        if len(modules) == 0:
            self.main_edit_redtext("You must create a module first")
        else:
            self.addwork_menu()

    def addwork_menu(self):
        """Opens menu for adding a piece of work"""
        self.clear_main_menu()
        self.addwork_home_bttn = Button(self,
                                        text="Home",
                                        font="Helvetica 13 bold",
                                        width=8,
                                        height=1,
                                        command=self.addwork_home
                                        )
        self.addwork_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.addwork_title_lbl = Label(self,
                                       text="Add Piece of Work",
                                       font="Helvetica 25")
        self.addwork_title_lbl.grid(row=0, column=2, columnspan=7, padx=170, pady=(0, 50))

        # Create list of module names for combobox

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        moduleList = []
        for module in modules:
            moduleList.append(module)

        # Create combobox

        self.addwork_combobox_lbl = Label(self,
                                          text="Select Module",
                                          font="Helvetica 13")
        self.addwork_combobox_lbl.grid(row=1, column=3, sticky=E)
        self.addwork_combobox = ttk.Combobox(self, values=moduleList, width=47, state="readonly")
        self.addwork_combobox.grid(row=1, column=4, columnspan=4)

        # Create other entry fields

        self.addwork_name_lbl = Label(self,
                                      text="Work name",
                                      font="Helvetica 13")
        self.addwork_name_lbl.grid(row=2, column=3, sticky=E)
        self.addwork_name_entry = Entry(self, width=50)
        self.addwork_name_entry.grid(row=2, column=4, columnspan=4)

        self.addwork_type_lbl = Label(self,
                                      text="Work type",
                                      font="Helvetica 13")
        self.addwork_type_lbl.grid(row=3, column=3, sticky=E)
        self.radiovar = StringVar()
        self.radiovar.set(None)
        self.addwork_type_exambttn = Radiobutton(self,
                                                 text="Exam",
                                                 font="Helvetica 13",
                                                 variable=self.radiovar,
                                                 value="exam")
        self.addwork_type_exambttn.grid(row=3, column=4, padx=(20, 0), pady=(2, 0))
        self.addwork_type_courseworkbttn = Radiobutton(self,
                                                       text="Coursework",
                                                       font="Helvetica 13",
                                                       variable=self.radiovar,
                                                       value="coursework")
        self.addwork_type_courseworkbttn.grid(row=3, column=5, pady=(2, 0))

        self.addwork_percent_lbl = Label(self,
                                         text="Percentage of module",
                                         font="Helvetica 13")
        self.addwork_percent_lbl.grid(row=4, column=3, sticky=E)
        self.addwork_percent_entry = Entry(self, width=50)
        self.addwork_percent_entry.grid(row=4, column=4, columnspan=4)

        self.addwork_score_lbl = Label(self,
                                       text="Score (%)",
                                       font="Helvetica 13")
        self.addwork_score_lbl.grid(row=5, column=3, sticky=E)
        self.addwork_score_entry = Entry(self, width=50)
        self.addwork_score_entry.grid(row=5, column=4, columnspan=4)

        self.addwork_submit_bttn = Button(self, width=40, text="Submit", command=self.addwork_validation)
        self.addwork_submit_bttn.grid(row=6, column=3, columnspan=5, pady=(30,5), padx=(50,0))

        self.addwork_error_lbl = Label(self, font="Helvetica 12", fg="red")

    def addwork_home(self):
        """Return to the main menu from the add work menu"""
        self.addwork_home_bttn.grid_forget()
        self.addwork_title_lbl.grid_forget()
        self.addwork_combobox_lbl.grid_forget()
        self.addwork_combobox.grid_forget()
        self.addwork_name_lbl.grid_forget()
        self.addwork_name_entry.grid_forget()
        self.addwork_type_lbl.grid_forget()
        self.addwork_type_exambttn.grid_forget()
        self.addwork_type_courseworkbttn.grid_forget()
        self.addwork_percent_lbl.grid_forget()
        self.addwork_percent_entry.grid_forget()
        self.addwork_score_lbl.grid_forget()
        self.addwork_score_entry.grid_forget()
        self.addwork_submit_bttn.grid_forget()
        self.addwork_error_lbl.grid_forget()
        self.main_menu()

    def addwork_validation(self):
        """Validates the inputted info for adding work. If it fails, an error message is displayed."""
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        work_module = self.addwork_combobox.get()
        if work_module == "":
            self.addwork_error("noModule")
        elif self.addwork_name_entry.get() == "":
            self.addwork_error("nameBlank")
        elif len(self.addwork_name_entry.get()) > 50:
            self.addwork_error("nameLength")
        elif self.addwork_name_entry.get() in modules[work_module].works:
            self.addwork_error("workExists")
        else:
            try:
                percent = float(self.addwork_percent_entry.get())
                score = float(self.addwork_score_entry.get())
                if self.radiovar.get() != "exam" and self.radiovar.get() != "coursework":
                    self.addwork_error("selectType")
                elif not 0 <= percent <= 100 or not 0 <= score <= 100:
                    self.addwork_error("%range")
                else:
                    self.addwork()
            except ValueError:
                self.addwork_error("%value")

    def addwork_error(self, errortype):
        """Displays error message in redtext if validation fails"""
        if errortype == "noModule":
            self.addwork_error_lbl.configure(text="You must select a module")
        elif errortype == "nameBlank":
            self.addwork_error_lbl.configure(text="The name of the piece of work cannot be blank")
        elif errortype == "workExists":
            self.addwork_error_lbl.configure(text="That piece of work already exists")
        elif errortype == "selectType":
            self.addwork_error_lbl.configure(text="You must select a type of work")
        elif errortype == "nameLength":
            self.addwork_error_lbl.configure(text="Work name cannot exceed 50 characters")
        elif errortype == "%range":
            self.addwork_error_lbl.configure(text="Percentages must be between 0 and 100")
        elif errortype == "%value":
            self.addwork_error_lbl.configure(text="Percentages must be given as numbers")
        self.addwork_error_lbl.grid(row=7, column=3, columnspan=4)

    def addwork(self):
        """Creates a piece of work object using the info inputted into the addwork menu"""
        workName = self.addwork_name_entry.get()
        workModule = self.addwork_combobox.get()
        workType = self.radiovar.get()
        workPercent = float(self.addwork_percent_entry.get())
        workScore = float(self.addwork_score_entry.get())
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        f_modulesData = open(direct + "modulesData.dat", "wb")
        modules[workModule].works[workName] = Work(workName, workType, workScore, workPercent)
        pickle.dump(modules, f_modulesData, True)
        f_modulesData.close()
        self.addwork_home()
        self.main_edit_redtext(workName + " in module " + workModule + " created")

    def viewmodule_validate_access(self):
        """Check if any modules exist, and if so allow access to the view modules menu"""
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        if len(modules) == 0:
            self.main_edit_redtext("There are currently no modules to view")
        else:
            self.viewmodule_menu()

    def viewmodule_menu(self):
        """Opens the menu for viewing an existing module's information"""
        self.clear_main_menu()
        self.viewmodule_home_bttn = Button(self,
                                        text="Home",
                                        font="Helvetica 13 bold",
                                        width=8,
                                        height=1,
                                        command=self.viewmodule_home
                                        )
        self.viewmodule_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.viewmodule_title_lbl = Label(self,
                                       text="View a module",
                                       font="Helvetica 30")
        self.viewmodule_title_lbl.grid(row=0, column=2, columnspan=7, padx=170, pady=(0, 20))

        # Create list of module names for combobox

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        moduleList = []
        for module in modules:
            moduleList.append(module)

        # Create combobox

        self.viewmodule_combobox_lbl = Label(self,
                                          text="Select Module",
                                          font="Helvetica 13")
        self.viewmodule_combobox_lbl.grid(row=1, column=2, sticky=E, padx=(50,5))
        self.viewmodule_combobox = ttk.Combobox(self, values=moduleList, width=47, state="readonly")
        self.viewmodule_combobox.grid(row=1, column=3, columnspan=4)
        self.viewmodule_combobox.bind("<<ComboboxSelected>>", self.viewmodule_loadData)

        # Create frame to contain textbox and scrollbar

        self.viewmodule_work_frame = Frame(self, width=80, height=10)
        self.viewmodule_work_frame.grid(row=2, column=2, columnspan=6)

        # Create scrollbar

        self.viewmodule_work_scroll = Scrollbar(self.viewmodule_work_frame, width=20)
        self.viewmodule_work_scroll.pack(side=RIGHT, fill=Y)

        # Create textbox for work display

        self.viewmodule_work_txt = Text(self.viewmodule_work_frame, width=70, height=10, state=DISABLED,
                                        yscrollcommand=self.viewmodule_work_scroll.set)
        self.viewmodule_work_txt.pack(side=LEFT, fill=BOTH)

    def viewmodule_loadData(self, event):
        """Loads work data into the viewmodule textbox when a module is selected"""
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        module = self.viewmodule_combobox.get()
        textbox_content = ""
        workNumber = 1
        moduleWorks = modules[module].works
        for work in moduleWorks:
            textbox_content += str(workNumber) + ") " + moduleWorks[work].name + " - " + moduleWorks[work].work_type \
                               + " - " + str(moduleWorks[work].score) + "%\n"
            workNumber += 1
        self.viewmodule_work_txt.configure(state=NORMAL)
        self.viewmodule_work_txt.delete(0.0, END)
        self.viewmodule_work_txt.insert(0.0, textbox_content)
        self.viewmodule_work_txt.configure(state=DISABLED)

    def viewmodule_home(self):
        """Returns to the main menu from the module viewing menu"""
        self.viewmodule_home_bttn.grid_forget()
        self.viewmodule_title_lbl.grid_forget()
        self.viewmodule_combobox_lbl.grid_forget()
        self.viewmodule_combobox.grid_forget()
        self.viewmodule_work_txt.pack_forget()
        self.viewmodule_work_scroll.pack_forget()
        self.viewmodule_work_frame.grid_forget()
        self.main_menu()

    def about_page(self):
        """Displays information page about the application"""
        self.clear_main_menu()
        self.about_home_bttn = Button(self,
                                      text="Home",
                                      font="Helvetica 13 bold",
                                      width=8,
                                      height=1,
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

        self.about_contact_lbl = Label(self,
                                       text="Contact: isaac@wetton.net",
                                       font="Helvetica 12")
        self.about_contact_lbl.grid(row=3, column=2, pady=(5, 0))

    def about_home(self):
        """Goes back to main menu from about page"""
        self.about_home_bttn.grid_forget()
        self.about_text1_lbl.grid_forget()
        self.about_github_bttn.grid_forget()
        self.about_contact_lbl.grid_forget()
        self.main_menu()

    def githublink(self):
        """Opens the application's Github repos"""
        webbrowser.open_new("https://github.com/isaacwetton/degree-progress-tracker/")


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
