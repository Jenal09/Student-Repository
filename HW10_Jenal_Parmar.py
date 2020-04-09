# Homework- 10
# Name:Jenal Parmar 
# CWID:10444852

from typing import Tuple, DefaultDict, Dict, Iterator,List
from collections import defaultdict
from prettytable import PrettyTable
import os

class Student:
    """A class that holds all of the details of a student """
        
    def __init__(self , cwid: str, name: str , major: str)-> None:
        """A function to initailize the student info columns"""
        
        self._cwid: int = cwid
        self._name: str = name
        self._major: str = major
        self._stud_detail :Dict[str, str] = defaultdict(str)
        self._stud_remaining_req: List[str] = []
        self._stud_remaining_elect: List[str] = []
        self._gpa: float=0;

    def set_gpa(self)-> None:
        """A function to calucalte GPA of a student"""
        
        student_completed_courses = self._stud_detail
        list_grades = student_completed_courses.values();
        grades = {'A':4.0 , 'A-':3.75 ,'B+':3.25 , 'B':3.0 , 'B-':2.75 , 'C+':2.75 , 'C':2.0 , 'C-':0 , 'D+':0 , 'D':0 , 'D-':0 , 'F':0}
        total_courses = len(list_grades)
        grade_total=0;
        for value in list_grades:
            grade_total += grades[value]
        if total_courses!=0:
            gpa=grade_total/total_courses;
            gpa = round(gpa,2)
            self._gpa = gpa
        
    def add_grade(self, course, grade)-> None:
        """A function to add student grades for courses"""

        self._stud_detail[course] = grade

    def stud_add_remaining_req(self, courses, elect)-> None:
        """A function to add remaining courses to student table """
        
        self._stud_remaining_req = courses
        self._stud_remaining_elect = elect

    def pretty_table_stud(self):
        """A function to return all the info about a student in a form of a table."""
        
        return ([self._cwid, self._name, self._major, sorted(self._stud_detail.keys()), self._stud_remaining_req,  [] if(self._stud_remaining_elect) == None else self._stud_remaining_elect, self._gpa])

class Instructor:
    """A class that holds all of the details of an instructor """

    def __init__(self, cwid: str, name: str, department: str)-> None:
        """A function to initailize the instructor info columns"""
        
        self._cwid: int = cwid
        self._name: str= name
        self._department: str = department
        self._courses: Dict[str, int]= defaultdict(int)

    def add_student_count(self,course:str)-> None:
        """A function to add students in a course"""
        
        self._courses[course] += 1

    def pretty_table_inst(self):
        """A function to return instructor info in a sorted manner"""

        return [self._cwid,self._name, self._department], self._courses
              
class University:
    """A class University holds all of  the students, instructors and grades for a single University.  The class stores all of the data structures and methods together in a single place."""
    
    def __init__(self, directory):
        """A function to in initialize all the variables."""
        
        self._directory = directory
        self._stud_data: Dict[str, Student] = dict()
        self._inst_data: Dict[str, Instructor]= dict()
        self._major_data = defaultdict(lambda: defaultdict(list))
        self.grades = ['A','A-','B+','B','B-','C+','C']
        self.analyze_file() 

    def analyze_file(self)-> None:
        """A function that summarizes the data."""
        
        dir:str = os.path.isdir(self._directory)
        if not dir:
            raise FileNotFoundError("Invalid Path")
        
        try:
            f:str = os.listdir(self._directory)
        except FileNotFoundError:
             raise FileNotFoundError("File cannot be opened")
        
        if 'students.txt' in f:
            path = os.path.join(self._directory, 'students.txt')
            for cwid, name, major in list(self.file_reader(path, 3 ,";", True)):
                if cwid in self._stud_data:
                    print(f"{cwid} is already exists")
                else:
                    self._stud_data[cwid] = Student(cwid, name, major)
        if 'instructors.txt' in f:
            path = os.path.join(self._directory, 'instructors.txt')
            for cwid, name, department in list(self.file_reader(path, 3 ,"|", True)):
                if cwid in self._inst_data:
                    print(f"{cwid} is already exists")
                else:
                    self._inst_data[cwid] = Instructor(cwid, name, department)

        if 'majors.txt' in f:
            path = os.path.join(self._directory, 'majors.txt')
            for major,req, course in list(self.file_reader(path, 3 ,"\t", True)):
                self._major_data[major][req].append(course)

        if 'grades.txt' in f:
            path = os.path.join(self._directory, 'grades.txt')
            for stud_cwid, course, grade,inst_cwid in list(self.file_reader(path, 4 ,"|", True)):
                if stud_cwid in self._stud_data.keys() and grade in self.grades:
                    self._stud_data[stud_cwid].add_grade(course,grade)
                else:
                    print(f"Student {stud_cwid} has not passed the minimum passing criteria")
                if inst_cwid in self._inst_data.keys():
                    self._inst_data[inst_cwid].add_student_count(course)
                else:
                    print(f"Instructor With cwid {inst_cwid} is not in the instructor file")

          
        for v in self._stud_data.values():
            remaining_required = []
            remaining_elective = []
            if v._major not in self._major_data.keys():
                print(f"{v.major} is not available in majors table")
            for major, req in self._major_data.items():
                if v._major == major:
                    for course in req['E']:
                        if course in v._stud_detail:
                            remaining_elective = None
                            break
                    for course in req['R']:
                        if course not in v._stud_detail:
                            remaining_required.append(course)
                    if remaining_elective is not None or remaining_elective == []:
                        remaining_elective = sorted(req['E'])
            self._stud_data[v._cwid].stud_add_remaining_req(sorted(remaining_required),remaining_elective)
            self._stud_data[v._cwid].set_gpa()

               
    def file_reader(self,path: str,num_fields:int,sep =',',header = False)-> Iterator[Tuple[str]]:
        """A Generator function that read field-separated text files and returns one line at a time"""
        
        try:
            f1:str = open(path,'r')
        except FileNotFoundError:
            raise FileNotFoundError("Could not find the file!")
        else:
            with f1:
                line_num:int = 0
                if header and len(next(f1).split(sep)) != num_fields:
                    f1.seek(0)
                    raise ValueError(f"{path} has {len(f1.readline().split(sep))} fields on line 0 but expected {num_fields}")
                if header:
                    line_num +=1
                for line in f1:
                    line = line.strip().split(sep)
                    line_num +=1
                    if len(line)!= num_fields:
                        raise ValueError(f"{path} has {len(line)} fields on line {line_num} but expected {num_fields}")
                    yield tuple(line)

    def pretty_table_major(self):
        """A function to summarize table of all majors"""
        
        major_list:Iterator[Tuple[str]] = []
        pt = PrettyTable(field_names= ['Major','Required Courses','Electives'])
        print(f"Summary of Majors")
        for d, v  in self._major_data.items():
            pt.add_row([d, v['R'],v['E']])
            major_list.append([d, v['R'],v['E']])
        print(pt)
        return major_list
        

    def pretty_table_student(self):
        """A function to summarize table of all Students"""
    
        stud_list:Iterator[Tuple[str]] = []
        pt = PrettyTable(field_names = ['CWID','Name','Majors','Completed Courses','Remaining Required','Remaining Electives', 'GPA'])
        print(f"Summary of Students")
        for stud in self._stud_data.values():
            pt.add_row(stud.pretty_table_stud())
            stud_list.append(stud.pretty_table_stud())
        print(pt)
        
        return stud_list

    def pretty_table_instructor(self):
        """A function to summarize table of all Instructors"""
        
        inst_list:Iterator[Tuple[str]] = []
        pt = PrettyTable(field_names = ['CWID','Name','Department','Courses','Student'])
        print(f"Summary of Instructor")
        for inst in self._inst_data.values():
            inst_information, courses = inst.pretty_table_inst()
            for course, students in courses.items():
                inst_information.extend([course,students])
                pt.add_row(inst_information)
                inst_list.append(inst_information)
                inst_information = inst_information[0:3]
        print(pt)
        return inst_list
        
def main():
    try:
        univ = University(r"C:\Users\parma\Desktop\H10")
        univ.pretty_table_major()
        univ.pretty_table_student()
        univ.pretty_table_instructor()
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()


        
                



        





