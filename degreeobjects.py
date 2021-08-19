# Degree Objects
# Provides software object classes for degree-progress-tracker
import pickle, shelve

class Work(object):
    """A piece of university work (Coursework or Exam)"""

    def __init__(self, name, module, work_type, score, max_score):
        global works
        self.name = name
        self.module = module
        self.work_type = work_type
        self.score = score
        self.max_score = max_score
        works.append(self)
        f_worksData = open(direct + "worksData.dat", "wb")
        pickle.dump(works, f_worksData, True)
        f_worksData.close()

class Module(object):
    """A degree module"""

    def __init__(self, name, max_credits):
        global modules
        self.name = name
        self.max_credits = max_credits
        self.works = []
        modules.append(self)
        self.collect_work()

    def collect_work(self, module):
        global works
        for work in works:
            if work.module == module:
                self.works.append(work)



if __name__ == "__main__":
    print("This is a module and is not intended to be run directly.")
    input("Press the enter key to exit this window.")