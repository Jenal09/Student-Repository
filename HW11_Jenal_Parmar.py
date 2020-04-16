# Homework- 11
# Name:Jenal Parmar 
# CWID:10444852

from collections import defaultdict
from typing import Dict, DefaultDict, Iterator, Tuple, List, Set
from prettytable import PrettyTable
import sqlite3
import os

class Student:
    """A class that holds all of the details of a student """

    pt_column_names = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives", "GPA"]

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """A function to initailize the student info columns"""
        
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._course: Dict[str,str] = dict()
    
    def add_course_grade(self, course: str, grade: str) -> None:
        """A function to add student grades for courses"""
        
        self._course[course] = grade
    
    def student_info(self) -> list:
        """A function to return student info in a sorted manner"""
        
        major, passed, remaining_req, remaining_ele, GPA = self._major.remaining_course(self._cwid, self._course)
        return [self._cwid, self._name, major, sorted(passed), sorted(remaining_req), sorted(remaining_ele), GPA]

class Instructor:
    """A class that holds all of the details of an instructor """

    pt_column_names = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """A function to initailize the instructor info columns"""
        
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_course_student(self, course: str) -> None:
        """A function to add students in a course"""
        
        self._courses[course] += 1

    def instructor_info(self):
        """A function to return instructor info in a sorted manner"""
        
        for course, students in self._courses.items():
            yield (self._cwid, self._name, self._dept, course, students)

class Major:
    """A class to represent Majors"""

    pt_column_names = ["Major", "Required Courses", "Electives"]

    def __init__(self, major: str, passing = None) -> None:
        """A function to initialize Major info columns"""
        
        self._major: str = major
        self._required = dict()
        self._electives = dict()
        if passing is None:
            self._grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        else:
            self._grades = passing

    def add_course(self, flag: str, course: str) -> None:   
        """A function to add courses in Majors table"""
         
        if flag == 'R':
            self._required[course] = flag
        elif flag == 'E':
            self._electives[course] = flag
        else:
            print(f"Unknown Flag found {flag}")
        
    def remaining_course(self, cwid, completed_course) -> tuple:

        passed_courses = {course for course, grade in completed_course.items() if grade in self._grades}
        
        remaining_required = set(self._required) - passed_courses
        required = set(self._electives)

        if required.intersection(passed_courses):
            remaining_elective = []
        else:
            remaining_elective = required
        
        gpa: float = 0.0
        GPA: float = 0.0
        
        grade_point: Dict[str, float] = {'A':4.0, 'A-':3.75,'B+':3.25, 'B':3.0, 'B-':2.75, 'C+':2.75, 'C':2.0, 'C-':0, 'D+':0, 'D':0, 'D-':0, 'F':0}
        for grade in completed_course.values():
            for grd, pnt in grade_point.items():
                if grade == grd:
                    gpa += pnt

        if len(passed_courses) == 0:
            print(f"Student {cwid} has not passed with minimum grade point")
        else:
            GPA = round(gpa/len(passed_courses), 2)

        return self._major, passed_courses, remaining_required, remaining_elective, GPA

    def major_info(self) -> list:
        """a function to display Major table record"""

        return [self._major, sorted(self._required), sorted(self._electives)]

class University:
    """A class University holds all of  the students, instructors and grades for a single University.  The class stores all of the data structures and methods together in a single place."""
    
    def __init__(self, path): 
        """A function to in initialize all the variables."""
        
        self._path: str = path
        self._majors: Dict[str, Major] = dict()
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self.read_majors(path)
        self.read_students(path)
        self.read_instructors(path)
        self.read_grades(path)
        self.major_prettytable()
        self.student_prettytable()
        self.instructor_prettytable()
        self.student_grade_prettytable()

    def file_reader( self, path: str, fields: int, sep: str, header: bool = False) -> Iterator[Tuple[str]]:
        """A Generator function that read field-separated text files and returns one line at a time"""
        
        try:
            file_path = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {path} for reading!..")
        else:
            with file_path:
                line_num: int = 0
                if header:
                    if len(next(file_path).split(sep)) != fields:
                        raise ValueError(f"Header not valid")    
                    line_num = line_num + 1
                for line in file_path:
                    line = line.strip("\n").split(sep)
                    line_num = line_num + 1
                    if len(line) != fields:
                        raise ValueError(f"'{path}' has {len(line)} fields on line {line_num} but expected {fields}")
                    yield tuple(line)

    def read_majors(self, path: str) -> None:
        """A function to analyze the information from majors.txt file """
        
        try:
            for major, flag, course in self.file_reader(os.path.join(self._path, 'majors.txt'),3, sep = "\t", header = True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_course(flag, course)
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def read_students(self, path: str) -> None:
        """A function to analyze the information from students.txt file """
        try:
            for cwid, name, major in self.file_reader(os.path.join(self._path, 'students.txt'), 3, sep = "\t", header = True):
                if cwid in self._students:
                    print(f"{cwid} is already exists")
                else:
                    self._students[cwid] = Student(cwid, name, self._majors[major])
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def read_instructors(self, path: str) -> None:
        """A function to analyze the information from instructors.txt file """
        try:
            for cwid, name, dept in self.file_reader(os.path.join(self._path, 'instructors.txt'), 3, sep = "\t", header = True):
                if cwid in self._instructors:
                    print(f"{cwid} is already exists")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def read_grades(self, path: str) -> None:
        """A function to analyze the information from grades.txt file """
        try:
            for student_cwid, course, grade, instructor_cwid in self.file_reader(os.path.join(self._path, 'grades.txt'), 4, sep ='\t', header = True):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course_grade(course, grade) 
                else:
                    print(f"Student cwid {student_cwid} is not in the students file")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_course_student(course) 
                else:
                    print(f"instructor cwid {instructor_cwid} is not in the instructor file")
        except ValueError as e:
            print(e)

    def major_prettytable(self) -> None:
        """A function to print prettytable with major information """
        pt = PrettyTable(field_names = Major.pt_column_names)
        for major in self._majors.values():
            pt.add_row(major.major_info())
        print("Majors Summary")
        print(pt)


    def student_prettytable(self) -> None:
        """A function to print prettytable with student information """
        pt = PrettyTable(field_names = Student.pt_column_names)
        for stud in self._students.values():
            pt.add_row(stud.student_info())
        print("Student Summary")
        print(pt)


    def instructor_prettytable(self) -> None:
        """A function to print prettytable with instructor information """
        pt = PrettyTable(field_names = Instructor.pt_column_names)
        for inst in self._instructors.values():
            for inst_row in inst.instructor_info():
                pt.add_row(inst_row)
        print("Instructor Summary")
        print(pt)

    def student_grades_table_db(self, db_path: str) -> tuple:
        """A function to print prettytable with student and grade information from database """
        try:
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            print(e)
        else:
            try:
                query = "select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor from students s, grades g, instructors i where s.CWID = g.StudentCWID and i.CWID = g.InstructorCWID order by s.Name"
                for row in db.execute(query):
                    yield(row)
            except sqlite3.OperationalError as e:
                print(e)

    def student_grade_prettytable(self) -> None:
        """A function to print prettytable student grade and instructor information """
        pt = PrettyTable(field_names = ["Name", "CWID", "Course", "Grade", "Instructor"])
        for row in self.student_grades_table_db("F:/SSW-810/Stevens/HW11_Jenal_Parmar_Database.db"):
            pt.add_row(row)
        print("Student Grade Summary")
        print(pt)

def main():
    try:
        University("C:/Users/parma/Desktop/HW11")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()