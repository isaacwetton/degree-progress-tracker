#     A Windows application developed with python which is designed to assist in tracking university degree progress. 
#     Copyright (C) 2021  Isaac Wetton

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see https://www.gnu.org/licenses/.

# Import modules
import os
import tkinter.messagebox
import webbrowser
from tkinter import *
from tkinter import ttk
import pickle
from platform import system


class Work(object):
    """A piece of university work (Coursework or Exam)"""

    def __init__(self, name, work_type, score, percentage_module):
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

    def __init__(self, name, max_credits, exam_percent, coursework_percent):
        self.name = name
        self.max_credits = max_credits
        self.exam_percent = exam_percent
        self.coursework_percent = coursework_percent
        self.works = {}

    def __str__(self):
        rep = "Module: " + self.name + "\n"
        rep += "Max Credits: " + self.max_credits + "\n"
        rep += "Percentage exam: " + self.exam_percent + "\n"
        rep += "Percentage coursework: " + self.coursework_percent + "\n"
        return rep

    def get_completed_creds(self):
        """Calculates the number of completed credits in the module"""
        completed_percent = 0.0
        for work in self.works:
            completed_percent += self.works[work].percentage_module
        completed_creds = completed_percent * 0.01 * self.max_credits
        completed_creds = round(completed_creds)
        return completed_creds


# Create application frame

class Application(Frame):
    """A GUI Application Frame to contain the primary menu navigation."""

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()

    def first_time(self):
        """Initiates first time setup menu. Menu asks for course name, maximum credits, and target grade"""

        self.wel_lbl = Label(self,
                             text="I've noticed this is your first time using my Degree Progress Tracker.\n" +
                                  "Please input your degree information below:",
                             font="Helvetica 15"
                             )
        self.wel_lbl.grid(row=0, column=1, padx=90, pady=(100, 60), columnspan=7)

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

        self.course_target_combobox_lbl = Label(self,
                                                text="Select Target Grade",
                                                font="Helvetica 13")
        self.course_target_combobox_lbl.grid(row=3, column=4, sticky=W)
        self.course_target_combobox = ttk.Combobox(self,
                                                   values=["Third",
                                                           "2:2",
                                                           "2:1",
                                                           "First"],
                                                   width=47,
                                                   state="readonly")
        self.course_target_combobox.current(2)
        self.course_target_combobox.grid(row=3, column=5, sticky=W)

        self.submit_course_info_bttn = Button(self, text="Submit", command=self.close_setup, width=42,
                                              font="Helvetica 9", cursor="hand2")
        self.submit_course_info_bttn.grid(row=4, column=5, sticky=W)

        self.setup_error_lbl = Label(self, font="Helvetica 12", fg="brown")

    def close_setup(self):
        """Validates inputs, saves data and closes setup menu"""
        # Check coursename length is 40 character or less
        if len(self.course_name_entry.get()) < 41:
            # Check that coursename isn't blank
            if self.course_name_entry.get() == "":
                self.setup_entry_error("nameblank_error")
            else:
                # Ensure that credits are inputted as an integer
                try:
                    courseName = self.course_name_entry.get()
                    courseCredits = int(self.course_maxcreds_entry.get())
                    courseTarget = self.course_target_combobox.get()
                    # Check that credits aren't negative
                    if courseCredits <= 0:
                        self.setup_entry_error("negativecreds_error")
                    else:

                        # Write inputted course data to file

                        courseData = [courseName, courseCredits, courseTarget]
                        f_writeCourseData = open(direct + "courseData.dat", "wb")
                        pickle.dump(courseData, f_writeCourseData, True)
                        f_writeCourseData.close()

                        # Initiate modulesData.dat with an empty dict

                        f_modulesData = open(direct + "modulesData.dat", "wb")
                        modules = {}
                        pickle.dump(modules, f_modulesData, True)
                        f_modulesData.close()

                        # Remove all initial setup tkinter elements and open main menu

                        self.wel_lbl.grid_remove()
                        self.course_name_entry.grid_remove()
                        self.course_name_entry_lbl.grid_remove()
                        self.course_maxcreds_entry_lbl.grid_remove()
                        self.course_maxcreds_entry.grid_remove()
                        self.submit_course_info_bttn.grid_remove()
                        self.setup_error_lbl.grid_remove()
                        self.course_target_combobox_lbl.grid_remove()
                        self.course_target_combobox.grid_remove()
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
        self.setup_error_lbl.grid(row=5, column=3, columnspan=3)

    def main_menu(self):
        """Opens the main menu of the application"""

        self.main_title_lbl = Label(self,
                                    text="Degree Progress Tracker",
                                    font="Helvetica 25")
        self.main_title_lbl.grid(row=0, column=1, columnspan=7, padx=220)

        self.main_credit_lbl = Label(self,
                                     text="by Isaac Wetton",
                                     font="Helvetica 12")
        self.main_credit_lbl.grid(row=1, column=3, columnspan=4, pady=(0, 5))

        # Create main menu buttons

        self.main_courseinfo_bttn = Button(self, text="View Course Stats", font="Helvetica 9", width=42, height=2,
                                           command=self.course_info_validate, cursor="hand2")
        self.main_createmodule_bttn = Button(self, text="Create/Delete Module", font="Helvetica 9", width=42, height=2,
                                             command=self.create_module_menu, cursor="hand2")
        self.main_addwork_bttn = Button(self, text="Add a Piece of Work", font="Helvetica 9", width=42, height=2,
                                        command=self.addwork_validate_access, cursor="hand2")
        self.main_viewmodule_bttn = Button(self, text="View a Module's Stats", font="Helvetica 9", width=42, height=2,
                                           command=self.viewmodule_validate_access, cursor="hand2")
        self.main_about_bttn = Button(self, text="About this Application", font="Helvetica 9", width=42, height=2,
                                      command=self.about_page, cursor="hand2")
        self.main_reset_bttn = Button(self, text="Edit Course Info / Reset Application", font="Helvetica 9",
                                      width=42, height=2,
                                      command=self.reset_page,
                                      cursor="hand2")
        self.main_deletework_bttn = Button(self, text="Delete a Piece of Work", font="Helvetica 9", width=42,
                                           height=2, cursor="hand2", command=self.deletework_validate_access)
        self.main_save_bttn = Button(self, text="Save/Load Profiles", font="Helvetica 9", width=42,
                                     height=2, cursor="hand2", command=self.save_page)

        # Position main menu buttons on the menu

        self.main_courseinfo_bttn.grid(row=6, column=4, pady=1)
        self.main_createmodule_bttn.grid(row=2, column=4, pady=1)
        self.main_addwork_bttn.grid(row=3, column=4, pady=1)
        self.main_viewmodule_bttn.grid(row=5, column=4, pady=1)
        self.main_about_bttn.grid(row=9, column=4, pady=1)
        self.main_reset_bttn.grid(row=7, column=4, pady=1)
        self.main_deletework_bttn.grid(row=4, column=4, pady=1)
        self.main_save_bttn.grid(row=8, column=4, pady=1)

        self.main_redtext = Label(self, font="Helvetica 12", fg="brown", text="")
        self.main_redtext.grid(row=10, column=4)

        self.main_ver_lbl = Label(self,
                                  text="v1.1.1",
                                  font="Helvetica 10")
        self.main_ver_lbl.grid(row=10, column=4, pady=(25, 0), padx=(750, 0))

    def main_edit_redtext(self, displaytext):
        """Edits and displays the red text on the main menu"""
        self.main_redtext.configure(text=displaytext)

    def clear_main_menu(self):
        """Closes the main menu"""
        self.main_title_lbl.grid_forget()
        self.main_credit_lbl.grid_forget()
        self.main_ver_lbl.grid_forget()
        self.main_courseinfo_bttn.grid_forget()
        self.main_createmodule_bttn.grid_forget()
        self.main_addwork_bttn.grid_forget()
        self.main_viewmodule_bttn.grid_forget()
        self.main_about_bttn.grid_forget()
        self.main_reset_bttn.grid_forget()
        self.main_deletework_bttn.grid_forget()
        self.main_save_bttn.grid_forget()
        self.main_redtext.grid_forget()

    def course_info_validate(self):
        """Checks to see if there is any completed work before accessing course_info menu"""
        validated = False

        # Load modules data

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()

        # Return an error if no modules exist

        if len(modules) == 0:
            self.main_edit_redtext("You must create a module and add completed work first")
        else:
            # Check that at least one module has completed work, otherwise return an error
            for module in modules:
                if modules[module].works != {}:
                    validated = True
                    break
            if validated is True:
                self.course_info_menu()
            elif validated is False:
                self.main_edit_redtext("You must add completed work first")

    def course_info_menu(self):
        """Opens course info menu"""
        self.clear_main_menu()
        # Open relevant files
        f_readCourseData = open(direct + "courseData.dat", "rb")
        courseData = pickle.load(f_readCourseData)
        f_readCourseData.close()
        target = courseData[2]

        # Create course info menu

        self.courseinfo_home_bttn = Button(self,
                                           text="Home",
                                           font="Helvetica 13 bold",
                                           width=8,
                                           height=1,
                                           command=self.courseinfo_home,
                                           cursor="hand2"
                                           )
        self.courseinfo_home_bttn.grid(row=0, column=0, padx=10)

        self.course_title_lbl = Label(self,
                                      text="Course Info",
                                      font="Helvetica 30")
        self.course_title_lbl.grid(row=0, column=2, columnspan=7, padx=200)

        self.course_name_lbl = Label(self,
                                     text="Course name: " + courseData[0],
                                     font="Helvetica 13")
        self.course_name_lbl.grid(row=1, column=1, columnspan=6, sticky=W)

        # Calculate total completed course credits

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        completedCreds = int(0)
        for module in modules:
            completedCreds += modules[module].get_completed_creds()

        # Calculate percentage of course complete

        percentageComplete = round(completedCreds / courseData[1] * 100, 2)

        # Display number of completed credits out of maximum

        self.course_creds_lbl = Label(self,
                                      text="Completed Credits: " + str(completedCreds) + " out of "
                                           + str(courseData[1]) + " (" + str(percentageComplete) + "%)",
                                      font="Helvetica 13")
        self.course_creds_lbl.grid(row=2, column=1, columnspan=6, sticky=W)

        # Add information label describing the textbox content

        self.course_modulelistinfo_lbl = Label(self,
                                               text="The displayed module scores are calculated using completed work "
                                                    "only",
                                               font="Helvetica 12",
                                               fg="brown")
        self.course_modulelistinfo_lbl.grid(row=3, column=1, columnspan=6, sticky=W)

        # Create frame to contain textbox and scrollbar

        self.course_modules_frame = Frame(self, width=80, height=10)
        self.course_modules_frame.grid(row=4, column=2, columnspan=6)

        # Create scrollbar

        self.course_modules_scroll = Scrollbar(self.course_modules_frame, width=20)
        self.course_modules_scroll.pack(side=RIGHT, fill=Y)

        # Create textbox for work display

        self.course_modules_txt = Text(self.course_modules_frame, width=70, height=8, state=DISABLED,
                                       yscrollcommand=self.course_modules_scroll.set, font="Helvetica 11")
        self.course_modules_txt.pack(side=LEFT, fill=BOTH)
        self.course_modules_scroll.configure(command=self.course_modules_txt.yview)

        # Initialise variables used for loading modules into textbox

        textbox_content = ""
        toDateCompletedScore = 0.0
        toDateCompletedTotal = 0.0
        moduleNumber = 1
        moduleScores = {}
        moduleEmpty = {}

        # Create dictionary of modules and their respective scores

        for module in modules:
            completedScore = 0.0
            completedTotal = 0.0
            if modules[module].works != {}:
                for work in modules[module].works:
                    completedScore += modules[module].works[work].score * \
                                      modules[module].works[work].percentage_module * 0.01
                    completedTotal += modules[module].works[work].percentage_module
                overallScore = round((completedScore / completedTotal) * 100, 2)
                moduleEmpty[module] = False
            else:
                overallScore = 0.0
                moduleEmpty[module] = True
            toDateCompletedScore += completedScore * 0.01 * modules[module].max_credits
            toDateCompletedTotal += completedTotal * 0.01 * modules[module].max_credits
            moduleScores[module] = overallScore

        # Sort moduleScores dictionary into list from highest to lowest score

        moduleScores = sorted(moduleScores.items(), key=self.modulesSortFunc, reverse=True)

        # Create textbox content

        for module in moduleScores:
            if moduleEmpty[module[0]] == False:
                textbox_content += str(moduleNumber) + ") " + module[0] + " - " + str(module[1]) + "%\n"
                moduleNumber += 1
        for module in moduleScores:
            if moduleEmpty[module[0]] == True and module[1] == 0.0:
                textbox_content += str(moduleNumber) + ") " + module[0] + " - " + "No Work Completed\n"
                moduleNumber += 1

        # Calculate overall score of all completed work

        toDateOverallScore = round((toDateCompletedScore / toDateCompletedTotal) * 100, 2)

        # Insert textbox content

        self.course_modules_txt.configure(state=NORMAL)
        self.course_modules_txt.insert(0.0, textbox_content)
        self.course_modules_txt.configure(state=DISABLED)

        self.course_overallcomplete_score_lbl = Label(self,
                                                      font="Helvetica 13",
                                                      text="From your completed work, your current overall score is "
                                                           + str(toDateOverallScore) + "%")
        self.course_overallcomplete_score_lbl.grid(row=5, column=1, columnspan=6, sticky=W)

        # Determine target score based on inputted target

        if target == "First":
            targetScore = 70.0
        elif target == "2:1":
            targetScore = 60.0
        elif target == "2:2":
            targetScore = 50.0
        else:
            targetScore = 40.0

        # Determine if target is being hit

        if toDateOverallScore >= targetScore:
            targetHit = True
        else:
            targetHit = False

        # Display label describing target info

        self.course_targetinfo_lbl = Label(self,
                                           font="Helvetica 13",
                                           text="",
                                           justify=LEFT)
        self.course_targetinfo_lbl.grid(row=6, column=1, columnspan=6, sticky=W)

        if targetHit is True:
            # Determine the score required in remaining work to remain on target
            percentageIncomplete = 100 - percentageComplete
            requiredScore = ((targetScore * 100) - (toDateOverallScore * percentageComplete)) / percentageIncomplete
            requiredScore = round(requiredScore, 2)
            self.course_targetinfo_lbl.configure(text="This score exceeds your target of a " + target.lower()
                                                      + ". Well done! To remain above your target,\nyou must score "
                                                      + "an average of "
                                                      + str(requiredScore) + "% in the remaining "
                                                      + str(percentageIncomplete) + "% of the course.")

        elif targetHit is False and percentageComplete != 100.0:
            # Determine the score required on remaining work to hit target grade
            percentageIncomplete = 100 - percentageComplete
            requiredScore = ((targetScore * 100) - (toDateOverallScore * percentageComplete)) / percentageIncomplete
            requiredScore = round(requiredScore, 2)
            self.course_targetinfo_lbl.configure(text="This score is currently below your target of a " + target.lower()
                                                      + ". To hit your target, you must score\nan average of "
                                                      + str(requiredScore) + "% in the remaining "
                                                      + str(percentageIncomplete) + "% of the course.")

    def modulesSortFunc(self, module):
        """Returns the score of each module for sorting"""
        return module[1]

    def courseinfo_home(self):
        """Goes back to main menu from course info page"""
        self.courseinfo_home_bttn.grid_forget()
        self.course_title_lbl.grid_forget()
        self.course_name_lbl.grid_forget()
        self.course_creds_lbl.grid_forget()
        self.course_modules_frame.grid_forget()
        self.course_modules_scroll.pack_forget()
        self.course_modules_txt.pack_forget()
        self.course_overallcomplete_score_lbl.grid_forget()
        self.course_targetinfo_lbl.grid_forget()
        self.course_modulelistinfo_lbl.grid_forget()
        self.main_menu()

    def create_module_menu(self):
        """Opens menu for adding a module"""
        self.clear_main_menu()
        self.create_module_home_bttn = Button(self,
                                              text="Home",
                                              font="Helvetica 13 bold",
                                              width=8,
                                              height=1,
                                              command=self.create_module_home,
                                              cursor="hand2"
                                              )
        self.create_module_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.create_module_title_lbl = Label(self,
                                             text="Create Module",
                                             font="Helvetica 30")
        self.create_module_title_lbl.grid(row=0, column=2, columnspan=7, padx=170, pady=(0, 20))

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
                                                command=self.create_module_validation,
                                                font="Helvetica 9",
                                                cursor="hand2")
        self.create_module_submit_bttn.grid(row=5, column=4)

        self.create_module_error_lbl = Label(self, font="Helvetica 12", fg="brown", text="")
        self.create_module_error_lbl.grid(row=6, column=3, pady=(5, 0), columnspan=2)

        self.create_module_delete_title_lbl = Label(self, font="Helvetica 30", text="Delete Module")
        self.create_module_delete_title_lbl.grid(row=7, column=2, columnspan=7, padx=170, pady=(0, 20))

        self.create_module_delete_select_lbl = Label(self, font="Helvetica 13", text="Select Module")
        self.create_module_delete_select_lbl.grid(row=8, column=3, sticky=E)

        # Create list of module names for combobox

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        moduleList = []
        for module in modules:
            moduleList.append(module)

        # Sort moduleList alphabetically

        moduleList = sorted(moduleList, key=self.moduleListSortFunc)

        # Create combobox

        self.create_module_delete_combobox = ttk.Combobox(self, values=moduleList, width=47, state="readonly")
        self.create_module_delete_combobox.grid(row=8, column=4)

        self.create_module_delete_bttn = Button(self, font="Helvetica 9", text="Delete Module", width=42,
                                                command=self.delete_module_validation, cursor="hand2")
        self.create_module_delete_bttn.grid(row=9, column=4)

        self.delete_module_error_lbl = Label(self, font="Helvetica 12", fg="brown", text="")
        self.delete_module_error_lbl.grid(row=10, column=3, pady=(5, 0), columnspan=2)

    def moduleListSortFunc(self, module):
        """Returns an uppercase name to the sorted function, for alphabetical sorting"""
        return module.upper()

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
        self.create_module_delete_title_lbl.grid_forget()
        self.create_module_delete_select_lbl.grid_forget()
        self.create_module_delete_combobox.grid_forget()
        self.create_module_delete_bttn.grid_forget()
        self.delete_module_error_lbl.grid_forget()
        self.main_menu()

    def create_module_validation(self):
        """Validates inputted information when creating a module"""

        # Load module and course data
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        f_readCourseData = open(direct + "courseData.dat", "rb")
        courseData = pickle.load(f_readCourseData)
        f_readCourseData.close()

        # Calculate unassigned credits
        unassignedCreds = courseData[1]
        for module in modules:
            unassignedCreds -= modules[module].max_credits

        # Validate inputs
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
                                        if maxCreds <= unassignedCreds:
                                            self.create_module()
                                        else:
                                            self.create_module_error("tooManyCreds", unassigned=unassignedCreds)
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

    def create_module_error(self, errortype, unassigned=0):
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
        elif errortype == "tooManyCreds" and unassigned != 0:
            self.create_module_error_lbl.configure(text="There are only " + str(unassigned)
                                                        + " unassigned credits remaining")
        elif errortype == "tooManyCreds" and unassigned == 0:
            self.create_module_error_lbl.configure(text="There are no unassigned credits remaining")
        self.create_module_error_lbl.grid(row=6, column=3, pady=(5, 0), columnspan=2)

    def create_module(self):
        """Creates a module object using the given info and stores it in the file system"""
        # Get relevant inputs for creating module
        moduleName = self.create_module_name_entry.get()
        examPercent = round(float(self.create_module_examcreds_entry.get()), 1)
        courseworkPercent = round(float(self.create_module_courseworkcreds_entry.get()), 1)
        maxCreds = int(self.create_module_maxcreds_entry.get())

        # Load module data
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()

        # Write new module object into file
        f_modulesData = open(direct + "modulesData.dat", "wb")
        modules[moduleName] = Module(moduleName, maxCreds, examPercent, courseworkPercent)
        pickle.dump(modules, f_modulesData, True)
        f_modulesData.close()

        # Return to main menu with confirmation message
        self.create_module_home()
        self.main_edit_redtext("Module " + moduleName + " created")

    def delete_module_validation(self):
        """Ensures that a module has been selected for deletion before attempting to delete it"""
        module = self.create_module_delete_combobox.get()
        if module == "":
            self.delete_module_error()
        else:
            self.delete_module(module)

    def delete_module_error(self):
        """Displays error message if a module is not selected when attempting to delete a module"""
        self.delete_module_error_lbl.configure(text="You must select a module")

    def delete_module(self, module):
        """Deletes the selected module, then invokes self.create_module_home() to return to main menu"""
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        del modules[module]
        f_modulesData = open(direct + "modulesData.dat", "wb")
        pickle.dump(modules, f_modulesData, True)
        f_modulesData.close()
        self.create_module_home()
        self.main_edit_redtext("Module " + module + " deleted successfully")

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
                                        command=self.addwork_home,
                                        cursor="hand2"
                                        )
        self.addwork_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.addwork_title_lbl = Label(self,
                                       text="Add Piece of Work",
                                       font="Helvetica 25")
        self.addwork_title_lbl.grid(row=0, column=2, columnspan=7, padx=170)

        self.addwork_guide_lbl = Label(self,
                                       text="Add exams and pieces of coursework after they have been completed "
                                            + "and marked",
                                       font="Helvetica 12",
                                       fg="brown")
        self.addwork_guide_lbl.grid(row=1, column=1, columnspan=7, pady=(50, 20))

        # Create list of module names for combobox

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        moduleList = []
        for module in modules:
            moduleList.append(module)

        # Sort list of modules alphabetically

        moduleList = sorted(moduleList, key=self.moduleListSortFunc)

        # Create combobox

        self.addwork_combobox_lbl = Label(self,
                                          text="Select Module",
                                          font="Helvetica 13")
        self.addwork_combobox_lbl.grid(row=2, column=3, sticky=E)
        self.addwork_combobox = ttk.Combobox(self, values=moduleList, width=47, state="readonly")
        self.addwork_combobox.grid(row=2, column=4, columnspan=4)

        # Create other entry fields

        self.addwork_name_lbl = Label(self,
                                      text="Work name",
                                      font="Helvetica 13")
        self.addwork_name_lbl.grid(row=3, column=3, sticky=E)
        self.addwork_name_entry = Entry(self, width=50)
        self.addwork_name_entry.grid(row=3, column=4, columnspan=4)

        self.addwork_type_lbl = Label(self,
                                      text="Work type",
                                      font="Helvetica 13")
        self.addwork_type_lbl.grid(row=4, column=3, sticky=E)
        self.radiovar = StringVar()
        self.radiovar.set(None)
        self.addwork_type_exambttn = Radiobutton(self,
                                                 text="Exam",
                                                 font="Helvetica 13",
                                                 variable=self.radiovar,
                                                 value="exam")
        self.addwork_type_exambttn.grid(row=4, column=4, padx=(20, 0), pady=(2, 0))
        self.addwork_type_courseworkbttn = Radiobutton(self,
                                                       text="Coursework",
                                                       font="Helvetica 13",
                                                       variable=self.radiovar,
                                                       value="coursework")
        self.addwork_type_courseworkbttn.grid(row=4, column=5, pady=(2, 0))

        self.addwork_percent_lbl = Label(self,
                                         text="Percentage of module (%)",
                                         font="Helvetica 13")
        self.addwork_percent_lbl.grid(row=5, column=3, sticky=E)
        self.addwork_percent_entry = Entry(self, width=50)
        self.addwork_percent_entry.grid(row=5, column=4, columnspan=4)

        self.addwork_score_lbl = Label(self,
                                       text="Score (%)",
                                       font="Helvetica 13")
        self.addwork_score_lbl.grid(row=6, column=3, sticky=E)
        self.addwork_score_entry = Entry(self, width=50)
        self.addwork_score_entry.grid(row=6, column=4, columnspan=4)

        self.addwork_submit_bttn = Button(self, width=40, text="Submit", command=self.addwork_validation,
                                          font="Helvetica 9", cursor="hand2")
        self.addwork_submit_bttn.grid(row=7, column=3, columnspan=5, pady=(30, 5), padx=(50, 0))

        self.addwork_error_lbl = Label(self, font="Helvetica 12", fg="brown")

    def addwork_home(self):
        """Return to the main menu from the add work menu"""
        self.addwork_home_bttn.grid_forget()
        self.addwork_title_lbl.grid_forget()
        self.addwork_guide_lbl.grid_forget()
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

        # Determine completed  and remaining work and exam percentages

        if work_module == "":
            self.addwork_error("noModule")
        else:
            completedExam = 0.0
            completedCoursework = 0.0
            for work in modules[work_module].works:
                if modules[work_module].works[work].work_type == "exam":
                    completedExam += modules[work_module].works[work].percentage_module
                elif modules[work_module].works[work].work_type == "coursework":
                    completedCoursework += modules[work_module].works[work].percentage_module
            remainingExam = modules[work_module].exam_percent - completedExam
            remainingCoursework = modules[work_module].coursework_percent - completedCoursework
            if self.addwork_name_entry.get() == "":
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
                    elif percent <= 0:
                        self.addwork_error("negativePercent")
                    elif not 0 < percent <= 100 or not 0 <= score <= 100:
                        self.addwork_error("%range")
                    elif self.radiovar.get() == "exam" and percent > remainingExam:
                        if modules[work_module].exam_percent == 0.0:
                            self.addwork_error("tooManyExam%", incomplete=remainingExam, zeroWork=True)
                        else:
                            self.addwork_error("tooManyExam%", incomplete=remainingExam)
                    elif self.radiovar.get() == "coursework" and percent > remainingCoursework:
                        if modules[work_module].coursework_percent == 0.0:
                            self.addwork_error("tooManyCoursework%", incomplete=remainingCoursework, zeroWork=True)
                        else:
                            self.addwork_error("tooManyCoursework%", incomplete=remainingCoursework)
                    else:
                        self.addwork()
                except ValueError:
                    self.addwork_error("%value")

    def addwork_error(self, errortype, incomplete=0.0, zeroWork=False):
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
        elif errortype == "negativePercent":
            self.addwork_error_lbl.configure(text="The work must be a percentage of the module")
        elif errortype == "%value":
            self.addwork_error_lbl.configure(text="Percentages must be given as numbers")
        elif errortype == "tooManyExam%":
            if incomplete != 0.0:
                self.addwork_error_lbl.configure(text="There is only " + str(incomplete) + "% of exams left"
                                                      + " to complete")
            elif zeroWork is False:
                self.addwork_error_lbl.configure(text="You have completed all of this module's exams")
            elif zeroWork is True:
                self.addwork_error_lbl.configure(text="There are no exams for this module")
        elif errortype == "tooManyCoursework%":
            if incomplete != 0.0:
                self.addwork_error_lbl.configure(text="There is only " + str(incomplete) + "% of coursework left"
                                                      + " to complete")
            elif zeroWork is False:
                self.addwork_error_lbl.configure(text="You have completed all of this module's coursework")
            elif zeroWork is True:
                self.addwork_error_lbl.configure(text="There is no coursework for this module")
        self.addwork_error_lbl.grid(row=8, column=3, columnspan=4)

    def addwork(self):
        """Creates a piece of work object using the info inputted into the addwork menu"""
        # Get relevant inputs for creating work
        workName = self.addwork_name_entry.get()
        workModule = self.addwork_combobox.get()
        workType = self.radiovar.get()
        workPercent = round(float(self.addwork_percent_entry.get()), 1)
        workScore = round(float(self.addwork_score_entry.get()), 1)

        # Load current module and work data
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()

        # Write new data (with new work) to file
        f_modulesData = open(direct + "modulesData.dat", "wb")
        modules[workModule].works[workName] = Work(workName, workType, workScore, workPercent)
        pickle.dump(modules, f_modulesData, True)
        f_modulesData.close()

        # Return to main menu with confirmation message
        self.addwork_home()
        self.main_edit_redtext(workName + " in module " + workModule + " created")

    def deletework_validate_access(self):
        """Checks to see if there is any completed work before accessing deletework menu"""
        validated = False
        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        if len(modules) == 0:
            self.main_edit_redtext("There is no work to delete")
        else:
            for module in modules:
                if modules[module].works != {}:
                    validated = True
                    break
            if validated is True:
                self.deletework_menu()
            elif validated is False:
                self.main_edit_redtext("There is no work to delete")

    def deletework_menu(self):
        """Opens menu for deleting a piece of work"""
        self.clear_main_menu()

        # Create title label and home button

        self.deletework_home_bttn = Button(self,
                                           text="Home",
                                           font="Helvetica 13 bold",
                                           width=8,
                                           height=1,
                                           command=self.deletework_home,
                                           cursor="hand2"
                                           )
        self.deletework_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.deletework_title_lbl = Label(self,
                                          text="Delete Piece of Work",
                                          font="Helvetica 30")
        self.deletework_title_lbl.grid(row=0, column=2, columnspan=7, padx=120)

        # Create list of module names for combobox

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        moduleList = []
        for module in modules:
            moduleList.append(module)

        # Sort list of modules alphabetically

        moduleList = sorted(moduleList, key=self.moduleListSortFunc)

        # Create combobox

        self.deletework_combobox_lbl = Label(self,
                                             text="Select Module",
                                             font="Helvetica 13")
        self.deletework_combobox_lbl.grid(row=1, column=2, sticky=E, padx=(50, 5), pady=(50, 0))
        self.deletework_combobox = ttk.Combobox(self, values=moduleList, width=47, state="readonly")
        self.deletework_combobox.grid(row=1, column=3, columnspan=4, pady=(50, 0))
        self.deletework_combobox.bind("<<ComboboxSelected>>", self.deletework_loadWorks)

        # Create frame to contain textbox and scrollbar

        self.deletework_frame = Frame(self, width=80, height=10)
        self.deletework_frame.grid(row=2, column=2, columnspan=6, padx=30)

        # Create scrollbar

        self.deletework_scroll = Scrollbar(self.deletework_frame, width=20)
        self.deletework_scroll.pack(side=RIGHT, fill=Y)

        # Create listbox for work selection

        self.deletework_listbox = Listbox(self.deletework_frame, width=70, height=10, state=NORMAL,
                                          yscrollcommand=self.deletework_scroll.set, font="Helvetica 11",
                                          selectmode=SINGLE, relief=FLAT, activestyle=NONE)
        self.deletework_listbox.pack(side=LEFT, fill=BOTH)
        self.deletework_scroll.configure(command=self.deletework_listbox.yview)

        # Add error message label

        self.deletework_error_lbl = Label(self,
                                          text="",
                                          font="Helvetica 12",
                                          fg="brown")
        self.deletework_error_lbl.grid(row=4, column=2, columnspan=5, padx=(20, 0), pady=(5, 0))

        # Create button for confirming work deletion

        self.deletework_submit_bttn = Button(self,
                                             font="Helvetica 9",
                                             text="Delete piece of work",
                                             width=42,
                                             command=self.deletework_validate)
        self.deletework_submit_bttn.grid(row=3, column=2, columnspan=3, padx=(150, 0), pady=(20, 0))

    def deletework_home(self):
        """Returns to the main menu from the work deletion menu"""
        self.deletework_home_bttn.grid_forget()
        self.deletework_title_lbl.grid_forget()
        self.deletework_combobox.grid_forget()
        self.deletework_combobox_lbl.grid_forget()
        self.deletework_frame.grid_forget()
        self.deletework_listbox.pack_forget()
        self.deletework_scroll.pack_forget()
        self.deletework_submit_bttn.grid_forget()
        self.deletework_error_lbl.grid_forget()
        self.main_menu()

    def deletework_loadWorks(self, event):
        """Load all work from the selected module into the listbox on the deletework menu"""

        # Retrieve saved modules data

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()

        # Delete current listbox content

        self.deletework_listbox.delete(0, END)

        # Insert works form selected module into listbox

        module = self.deletework_combobox.get()
        moduleWorks = modules[module].works
        for work in moduleWorks:
            self.deletework_listbox.insert(END, work)

    def deletework_validate(self):
        """Validates that a worksheet has been selected for deletion"""

        # If no line is selected, return an error, otherwise delete the selected work

        if self.deletework_listbox.curselection() == ():
            self.deletework_error_lbl.configure(text="You must select a piece of work to be deleted")
        else:
            self.deletework()

    def deletework(self):
        """Deletes the selected piece of work and returns to the main menu with a confirmation message"""

        # Retrieve selected line number and module

        selectedLine = self.deletework_listbox.curselection()
        module = self.deletework_combobox.get()

        # Retrieve name of work at that line

        workName = self.deletework_listbox.get(selectedLine)

        # Load module data

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()

        # Delete selected piece of work

        moduleWorks = modules[module].works
        del moduleWorks[workName]

        # Save new data with selected work omitted

        f_modulesData = open(direct + "modulesData.dat", "wb")
        pickle.dump(modules, f_modulesData, True)
        f_modulesData.close()

        # Return to main menu with confirmation message

        self.deletework_home()
        self.main_edit_redtext(workName + " in " + module + " successfully deleted")

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
                                           command=self.viewmodule_home,
                                           cursor="hand2"
                                           )
        self.viewmodule_home_bttn.grid(row=0, column=0, padx=10, sticky=N, pady=10)

        self.viewmodule_title_lbl = Label(self,
                                          text="View a Module",
                                          font="Helvetica 30")
        self.viewmodule_title_lbl.grid(row=0, column=2, columnspan=7, padx=170, pady=(0, 20))

        # Create list of module names for combobox

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        moduleList = []
        for module in modules:
            moduleList.append(module)

        # Sort list of modules alphabetically

        moduleList = sorted(moduleList, key=self.moduleListSortFunc)

        # Create combobox

        self.viewmodule_combobox_lbl = Label(self,
                                             text="Select Module",
                                             font="Helvetica 13")
        self.viewmodule_combobox_lbl.grid(row=1, column=2, sticky=E, padx=(50, 5))
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
                                        yscrollcommand=self.viewmodule_work_scroll.set, font="Helvetica 11")
        self.viewmodule_work_txt.pack(side=LEFT, fill=BOTH)
        self.viewmodule_work_scroll.configure(command=self.viewmodule_work_txt.yview)

        # Create percentage exam and coursework labels

        self.viewmodule_percentexam_lbl = Label(self, font="Helvetica 10")
        self.viewmodule_percentcoursework_lbl = Label(self, font="Helvetica 10")
        self.viewmodule_scoreexam_lbl = Label(self, font="Helvetica 10")
        self.viewmodule_scorecoursework_lbl = Label(self, font="Helvetica 10")
        self.viewmodule_scoretotal_lbl = Label(self, font="Helvetica 10")
        self.viewmodule_credits_lbl = Label(self, font="Helvetica 10")

    def viewmodule_loadData(self, event):
        """Loads module data when a module is selected"""

        # Load the module data

        f_modulesData = open(direct + "modulesData.dat", "rb")
        modules = pickle.load(f_modulesData)
        f_modulesData.close()
        module = self.viewmodule_combobox.get()

        # Initiate variables used in loading worksheet data

        textbox_content = ""
        workNumber = 1
        moduleWorks = modules[module].works  # Dictionary of module's works

        # Sort the dictionary of works

        sortedWorksList = sorted(moduleWorks.items(), reverse=True, key=self.worksSortFunc)
        sortedWorks = {}
        for work in sortedWorksList:
            sortedWorks[work[0]] = work[1]

        # Load data into textbox

        for work in sortedWorks:
            textbox_content += str(workNumber) + ") " + moduleWorks[work].name + " - " + moduleWorks[work].work_type \
                               + " - " + str(moduleWorks[work].score) + "%\n"
            workNumber += 1
        self.viewmodule_work_txt.configure(state=NORMAL)
        self.viewmodule_work_txt.delete(0.0, END)
        self.viewmodule_work_txt.insert(0.0, textbox_content)
        self.viewmodule_work_txt.configure(state=DISABLED)

        # Calculate values for displaying stats

        # Determine if module has no coursework or no exams
        noExam = False
        noCoursework = False
        if modules[module].exam_percent == 0.0:
            noExam = True
        if modules[module].coursework_percent == 0.0:
            noCoursework = True

        # Calculate completed coursework and exam percentages of module
        completedExamTotal = 0.0
        completedCourseworkTotal = 0.0
        for work in moduleWorks:
            if moduleWorks[work].work_type == "exam":
                completedExamTotal += moduleWorks[work].percentage_module
            elif moduleWorks[work].work_type == "coursework":
                completedCourseworkTotal += moduleWorks[work].percentage_module

        # Calculate completed exams as a percentage of total exams
        if modules[module].exam_percent != 0:
            completedExamPercent = (completedExamTotal / modules[module].exam_percent) * 100
        else:
            completedExamPercent = 0.0

        # Calculate completed coursework as a percentage of total coursework
        if modules[module].coursework_percent != 0:
            completedCourseworkPercent = (completedCourseworkTotal / modules[module].coursework_percent) * 100
        else:
            completedCourseworkPercent = 0.0

        # Calculate current achieved exam and coursework percentage scores
        completedExamScore = 0.0
        completedCourseworkScore = 0.0
        for work in moduleWorks:
            if moduleWorks[work].work_type == "exam":
                completedExamScore += (moduleWorks[work].score / 100) * moduleWorks[work].percentage_module
            elif moduleWorks[work].work_type == "coursework":
                completedCourseworkScore += (moduleWorks[work].score / 100) * moduleWorks[work].percentage_module

        # Calculate average score of completed exams
        completedExamScoreModule = completedExamScore
        if completedExamTotal != 0.0:
            completedExamScore /= (completedExamTotal / 100)

        # Calculate average score of completed coursework
        completedCourseworkScoreModule = completedCourseworkScore
        if completedCourseworkTotal != 0.0:
            completedCourseworkScore /= (completedCourseworkTotal / 100)

        # Calculate average score of all completed work
        completedModuleScore = completedCourseworkScoreModule + completedExamScoreModule
        completedModuleTotal = completedExamTotal + completedCourseworkTotal
        if completedModuleTotal != 0.0:
            completedModuleScore /= (completedModuleTotal / 100)

        # Round any displayed values

        completedExamPercent = round(completedExamPercent, 2)
        completedExamScore = round(completedExamScore, 2)
        completedCourseworkPercent = round(completedCourseworkPercent, 2)
        completedCourseworkScore = round(completedCourseworkScore, 2)
        completedModuleScore = round(completedModuleScore, 2)

        # Load course data and retrieve maximum course credits

        f_courseData = open(direct + "courseData.dat", "rb")
        courseData = pickle.load(f_courseData)
        f_courseData.close()
        maxCourseCreds = courseData[1]

        # Calculate module percentage worth of overall course

        percentageCourse = round((modules[module].max_credits / maxCourseCreds) * 100, 2)

        # Display percentage exam and coursework in labels

        if noExam is False:
            if completedExamTotal != 0:
                self.viewmodule_percentexam_lbl.configure(text=str(modules[module].exam_percent)
                                                               + "% of the module is exams. "
                                                               + "You have completed " + str(completedExamPercent)
                                                               + "% of your exams.")
                self.viewmodule_scoreexam_lbl.configure(text="In your completed exams, you have scored an overall "
                                                             + str(completedExamScore) + "%.")
            else:
                self.viewmodule_percentexam_lbl.configure(text=str(modules[module].exam_percent)
                                                               + "% of the module is exams. "
                                                               + "You have completed " + str(completedExamPercent)
                                                               + "% of your exams.")
                self.viewmodule_scoreexam_lbl.configure(text="")

        elif noExam is True:
            self.viewmodule_percentexam_lbl.configure(text="You have no exams for this module.")
            self.viewmodule_scoreexam_lbl.configure(text="")

        if noCoursework is False:
            if completedCourseworkTotal != 0:
                self.viewmodule_percentcoursework_lbl.configure(text=str(modules[module].coursework_percent)
                                                                     + "% of the module is coursework. You have completed "
                                                                     + str(completedCourseworkPercent)
                                                                     + "% of your coursework.")
                self.viewmodule_scorecoursework_lbl.configure(text="In your completed coursework, "
                                                                   + "you have scored an overall "
                                                                   + str(completedCourseworkScore) + "%.")
            else:
                self.viewmodule_percentcoursework_lbl.configure(text=str(modules[module].coursework_percent)
                                                                     + "% of the module is coursework. You have completed "
                                                                     + str(completedCourseworkPercent)
                                                                     + "% of your coursework.")
                self.viewmodule_scorecoursework_lbl.configure(text="")

        elif noCoursework is True:
            self.viewmodule_percentcoursework_lbl.configure(text="You have no coursework for this module.")
            self.viewmodule_scorecoursework_lbl.configure(text="")

        if completedModuleTotal != 0 and noExam is False and noCoursework is False:
            self.viewmodule_scoretotal_lbl.configure(text="In all your completed work so far in this module, you have "
                                                          + "an overall score of " + str(completedModuleScore) + "%.")
        elif completedModuleTotal != 0 and (noCoursework is True or noExam is True):
            self.viewmodule_scoretotal_lbl.configure(text="")
        else:
            self.viewmodule_scoretotal_lbl.configure(text="You have not created any work for this module yet.")

        self.viewmodule_credits_lbl.configure(text="This module is worth " + str(modules[module].max_credits)
                                                   + " credits (" + str(percentageCourse) + "% of the course).")

        self.viewmodule_percentexam_lbl.grid(row=3, column=2, columnspan=6, sticky=W, padx=(50, 0))
        self.viewmodule_scoreexam_lbl.grid(row=4, column=2, columnspan=6, sticky=W, padx=(50, 0))
        self.viewmodule_percentcoursework_lbl.grid(row=5, column=2, columnspan=6, sticky=W, padx=(50, 0))
        self.viewmodule_scorecoursework_lbl.grid(row=6, column=2, columnspan=6, sticky=W, padx=(50, 0))
        self.viewmodule_scoretotal_lbl.grid(row=7, column=2, columnspan=6, sticky=W, padx=(50, 0))
        self.viewmodule_credits_lbl.grid(row=8, column=2, columnspan=6, sticky=W, padx=(50, 0))

    def worksSortFunc(self, work):
        """Function used when sorting a module's worksheets by score. It simply returns the score of the work"""
        return work[1].score

    def viewmodule_home(self):
        """Returns to the main menu from the module viewing menu"""
        self.viewmodule_home_bttn.grid_forget()
        self.viewmodule_title_lbl.grid_forget()
        self.viewmodule_combobox_lbl.grid_forget()
        self.viewmodule_combobox.grid_forget()
        self.viewmodule_work_txt.pack_forget()
        self.viewmodule_work_scroll.pack_forget()
        self.viewmodule_work_frame.grid_forget()
        self.viewmodule_percentexam_lbl.grid_forget()
        self.viewmodule_percentcoursework_lbl.grid_forget()
        self.viewmodule_scoreexam_lbl.grid_forget()
        self.viewmodule_scorecoursework_lbl.grid_forget()
        self.viewmodule_scoretotal_lbl.grid_forget()
        self.viewmodule_credits_lbl.grid_forget()
        self.main_menu()

    def about_page(self):
        """Displays information page about the application"""
        self.clear_main_menu()
        self.about_home_bttn = Button(self,
                                      text="Home",
                                      font="Helvetica 13 bold",
                                      width=8,
                                      height=1,
                                      command=self.about_home,
                                      cursor="hand2"
                                      )
        self.about_home_bttn.grid(row=0, column=0, padx=10, pady=5)

        self.about_text1_lbl = Label(self,
                                     text="This application was created by Isaac Wetton. "
                                          + "It is designed to assist with the organisation\nand tracking of "
                                          + "a university degree's progress. The app allows for the creation "
                                          + "of modules\nand worksheets which can then be assigned to those "
                                          + "modules. \n\nEach module and worksheet's average marks and "
                                          + "grades can be tracked, as well as overall\nprogress. "
                                          + "The app makes the assumption that 40% is a third class, 50% is "
                                          + "a 2:2, 60% is a 2:1\nand 70% is a first class degree.\n\n"
                                          + "The course data for this program is stored in the directory "
                                          + "User\\Documents\\DegreeTracker\\.\nIf the program stops working "
                                          + "at any point, it can be reset by deleting this directory and "
                                          + "its\ncontents.\n\nThis is the first GUI program I have created "
                                          + "with Python so please appreciate there may be some\nissues. "
                                          + "Bugs and other problems can be reported on the GitHub page "
                                          + "below.",
                                     font="Helvetica 13",
                                     justify=LEFT)
        self.about_text1_lbl.grid(row=1, column=0, columnspan=7, pady=10, padx=50)

        self.about_github_bttn = Button(self, text="degree-progress-tracker GitHub Repository",
                                        width=50, height=1, command=self.githublink, font="Helvetica 9", cursor="hand2")
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

    def reset_page(self):
        """Opens a menu where the user can edit or reset their course information"""

        # Clear the main menu
        self.clear_main_menu()

        # Create home button for the menu
        self.reset_home_bttn = Button(self,
                                      text="Home",
                                      font="Helvetica 13 bold",
                                      width=8,
                                      height=1,
                                      command=self.reset_home,
                                      cursor="hand2"
                                      )
        self.reset_home_bttn.grid(row=0, column=0, padx=10)

        # Create title label for editing course info
        self.reset_edit_lbl = Label(self,
                                    text="Edit Course Info",
                                    font="Helvetica 30")
        self.reset_edit_lbl.grid(row=0, column=2, columnspan=7, padx=150, pady=(0, 20))

        # Create label, entry and button for increasing course credits

        self.reset_increasecreds_lbl = Label(self,
                                             text="Increase Course Credits By:",
                                             font="Helvetica 12")
        self.reset_increasecreds_lbl.grid(row=1, column=3, sticky=E, padx=(80, 0))

        self.reset_increasecreds_entry = Entry(self, width=21)
        self.reset_increasecreds_entry.grid(row=1, column=4)

        self.reset_increasecreds_bttn = Button(self,
                                               text="Increase Course Credits",
                                               font="Helvetica 9",
                                               width=42,
                                               cursor="hand2",
                                               command=self.increasecreds_validation)
        self.reset_increasecreds_bttn.grid(row=2, column=3, columnspan=2, pady=(5, 0), padx=(100, 0))

        # Create label for error messages

        self.reset_increasecreds_error_lbl = Label(self,
                                                   text="",
                                                   font="Helvetica 13",
                                                   fg="brown")
        self.reset_increasecreds_error_lbl.grid(row=3, column=3, columnspan=4)

        # Create label, combobox and button for changing target grade

        self.reset_target_lbl = Label(self,
                                      text="New Target Grade:",
                                      font="Helvetica 12")
        self.reset_target_lbl.grid(row=4, column=3, sticky=E, padx=(0, 0), pady=(20, 0))

        self.reset_target_combobox = ttk.Combobox(self,
                                                  values=["Third",
                                                          "2:2",
                                                          "2:1",
                                                          "First"],
                                                  width=18,
                                                  state="readonly")
        self.reset_target_combobox.grid(row=4, column=4, pady=(20, 0))

        self.reset_target_bttn = Button(self,
                                        text="Change Target Grade",
                                        font="Helvetica 9",
                                        width=42,
                                        cursor="hand2",
                                        command=self.change_target)
        self.reset_target_bttn.grid(row=5, column=3, columnspan=2, pady=(5, 0), padx=(100, 0))

        # Set combobox value to current target grade

        f_courseData = open(direct + "courseData.dat", "rb")
        courseData = pickle.load(f_courseData)
        f_courseData.close()
        target = courseData[2]
        if target == "First":
            self.reset_target_combobox.current(3)
        elif target == "2:1":
            self.reset_target_combobox.current(2)
        elif target == "2:2":
            self.reset_target_combobox.current(1)
        else:
            self.reset_target_combobox.current(0)

        # Create title label for resetting course data

        self.reset_reset_lbl = Label(self,
                                     text="Reset All Course Info",
                                     font="Helvetica 30")
        self.reset_reset_lbl.grid(row=6, column=2, columnspan=7, padx=150, pady=(20, 0))

        # Create warning message and button for resetting course info

        self.reset_reset_warning_lbl = Label(self,
                                             text="Here you can reset all program data - all created modules\nand"
                                                  + " pieces of work will be deleted, and you will be\nprovided with "
                                                  + "a fresh version of the application.",
                                             font="Helvetica 11",
                                             fg="brown")
        self.reset_reset_warning_lbl.grid(row=7, column=3, columnspan=4, padx=(30, 0))

        self.reset_reset_bttn = Button(self,
                                       text="Reset the Application",
                                       font="Helvetica 9",
                                       width=22,
                                       height=2,
                                       cursor="hand2",
                                       command=self.reset_app_confirm)
        self.reset_reset_bttn.grid(row=8, column=3, columnspan=4, padx=(30, 0))

    def reset_home(self):
        """Clears the reset_page menu and returns to the main menu"""
        self.reset_home_bttn.grid_forget()
        self.reset_edit_lbl.grid_forget()
        self.reset_increasecreds_lbl.grid_forget()
        self.reset_increasecreds_entry.grid_forget()
        self.reset_increasecreds_bttn.grid_forget()
        self.reset_increasecreds_error_lbl.grid_forget()
        self.reset_target_lbl.grid_forget()
        self.reset_target_combobox.grid_forget()
        self.reset_target_bttn.grid_forget()
        self.reset_reset_lbl.grid_forget()
        self.reset_reset_warning_lbl.grid_forget()
        self.reset_reset_bttn.grid_forget()
        self.main_menu()

    def increasecreds_validation(self):
        """Validates that the entered string value is a positive integer"""
        # Test for integer
        try:
            creds = int(self.reset_increasecreds_entry.get())
            if creds < 0:
                self.increasecreds_error("You must input a positive value")
            elif creds == 0:
                self.increasecreds_error("You cannot increase credits by zero")
            else:
                self.increasecreds(creds)
        except ValueError:
            self.increasecreds_error("You must input an integer value")

    def increasecreds_error(self, error_msg):
        """Changes the error message displayed"""
        self.reset_increasecreds_error_lbl.configure(text=error_msg)

    def increasecreds(self, creds):
        """Changes maximum course credits, increasing it by the passed creds parameter"""

        # Load course data
        f_courseData = open(direct + "courseData.dat", "rb")
        courseData = pickle.load(f_courseData)
        f_courseData.close()

        # Increase maximum credits by creds

        courseData[1] += creds

        # Overwrite course data with the new data

        f_courseData = open(direct + "courseData.dat", "wb")
        pickle.dump(courseData, f_courseData, True)
        f_courseData.close()

        # Return to main menu with confirmation message

        self.reset_home()
        self.main_edit_redtext("Maximum course credits increased by " + str(creds))

    def change_target(self):
        """Changes the courseData target info to the newly selected target grade"""

        # Retrieve selected target from combobox
        target = self.reset_target_combobox.get()

        # Load current course data
        f_courseData = open(direct + "courseData.dat", "rb")
        courseData = pickle.load(f_courseData)
        f_courseData.close()

        # Change course data's target grade to the selected target
        if courseData[2] != target:
            courseData[2] = target
            targetChanged = True
        else:
            targetChanged = False

        # Save course data (overwrite)
        f_courseData = open(direct + "courseData.dat", "wb")
        pickle.dump(courseData, f_courseData, True)
        f_courseData.close()

        # Return to main menu with confirmation message
        self.reset_home()
        if targetChanged:
            self.main_edit_redtext("Target grade changed to a " + target)
        else:
            self.main_edit_redtext("Target grade is already a " + target)

    def reset_app_confirm(self):
        """Opens page where the user is asked to confirm their decision to reset the program"""

        # Clear all tkinter elements
        self.reset_home()
        self.clear_main_menu()

        # Create Label and Yes/No buttons
        # 'Yes' resets the program. 'No' returns to the previous menu.
        self.reset_app_confirm_lbl = Label(self,
                                           text="Are you sure that you want to reset this application?",
                                           font="Helvetica 18",
                                           fg="brown")
        self.reset_app_confirm_lbl.grid(row=0, column=0, pady=(150, 0), padx=(120, 0), columnspan=10)

        self.reset_app_confirm_no_bttn = Button(self,
                                                text="No",
                                                font="Helvetica 13 bold",
                                                width=10,
                                                height=1,
                                                cursor="hand2",
                                                command=self.reset_app_denied)
        self.reset_app_confirm_no_bttn.grid(row=1, column=4, pady=10)

        self.reset_app_confirm_yes_bttn = Button(self,
                                                 text="Yes",
                                                 font="Helvetica 13 bold",
                                                 width=10,
                                                 height=1,
                                                 cursor="hand2",
                                                 command=self.reset_app)
        self.reset_app_confirm_yes_bttn.grid(row=1, column=7, pady=10)

    def reset_app_denied(self):
        """Returns the user to the edit/reset course info menu"""
        self.reset_app_confirm_lbl.grid_forget()
        self.reset_app_confirm_no_bttn.grid_forget()
        self.reset_app_confirm_yes_bttn.grid_forget()
        self.reset_page()

    def reset_app(self):
        """Resets the program and returns the user to the first time setup screen. Displays messagebox"""

        # Remove displayed tkinter elements
        self.reset_app_confirm_lbl.grid_forget()
        self.reset_app_confirm_no_bttn.grid_forget()
        self.reset_app_confirm_yes_bttn.grid_forget()

        # Delete saved program data
        # Checks that modulesData.dat exists before attempting deletion to prevent error
        os.remove(direct + "courseData.dat")
        if os.path.exists(direct + "modulesData.dat"):
            os.remove(direct + "modulesData.dat")

        # Initiate first time setup
        self.first_time()

        # Display messagebox confirming program reset
        tkinter.messagebox.showinfo("Program Reset", "The program has now been reset, and your previous data "
                                                     "has been erased.")

    def save_page(self):
        return None

# main program

# Determine operating system
operatingSystem = system()

# create directory
direct = ""
if operatingSystem == "Darwin":
    try:
        os.mkdir(os.path.expanduser("~/Documents/DegreeTracker/"))
        direct = os.path.expanduser("~/Documents/DegreeTracker/")
    except FileExistsError:
        direct = os.path.expanduser("~/Documents/DegreeTracker/")
elif operatingSystem == "Windows":
    try:
        os.mkdir(os.path.expanduser("~\\Documents\\DegreeTracker\\"))
        direct = os.path.expanduser("~\\Documents\\DegreeTracker\\")
    except FileExistsError:
        direct = os.path.expanduser("~\\Documents\\DegreeTracker\\")

# Determine if first-time use
try:
    f_courseData = open(direct + "courseData.dat", "rb")
    firstTime = False
    data = pickle.load(f_courseData)
    f_courseData.close()

    # For backwards compatibility, the following converts a tuple into a string.
    # This is because prior to v1.1.0, courseData.dat stored a tuple.

    newData = [data[0], data[1], data[2]]
    f_courseData = open(direct + "courseData.dat", "wb")
    pickle.dump(newData, f_courseData, True)
    f_courseData.close()
except IOError:
    firstTime = True

# Create root and main application window
root = Tk()
root.title("Degree Progress Tracker")
root.geometry("800x465")
root.resizable(False, False)
mainApp = Application(root)

# Invoke first time setup sequence if required

if firstTime is True:
    mainApp.first_time()
else:
    mainApp.main_menu()

# Set window icon (if using Windows) and start the program

if operatingSystem == "Windows":
    root.iconbitmap('degreetrackericon.ico')
root.mainloop()
