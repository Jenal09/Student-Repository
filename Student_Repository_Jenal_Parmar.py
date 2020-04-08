# Homework- 09
# Name:Jenal Parmar 
# CWID:10444852

from typing import Dict, DefaultDict, Iterator, Tuple
from collections import defaultdict
from prettytable import PrettyTable
import os

class Student:
    """A class that holds all of the details of a student """

    pt_column_names = ["CWID", "Name", "Completed Courses"]

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """A function to initailize the student info columns"""
        
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def add_course_grade(self, course: str, grade: str) -> None:
        """A function to add student grades for courses"""
        
        self._courses[course] = grade

    def student_info(self):
        """A function to return student info in a sorted manner"""
        
        return [self._cwid, self._name, sorted(self._courses.keys())]


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

class University:
    """A class University holds all of  the students, instructors and grades for a single University.  The class stores all of the data structures and methods together in a single place."""
    
    def __init__(self, path): 
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self.read_students(path)
        self.read_instructors(path)
        self.read_grades(path)
        self.student_prettytable()
        self.instructor_prettytable()


    def file_reader( self, path: str, fields: int, sep: str, header: bool = False) -> Iterator[Tuple[str]]:
        """ A Generator function that read field-separated text files and returns one line at a time """
        
        try:
            file_path = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(f"Cannot open file at path : {path}")
        else:
            with file_path:
                line_num: int = 0
                if header:
                    if len(next(file_path).split(sep)) != fields:
                        raise ValueError(f"Inavlid Header")    
                    line_num = line_num + 1
                for line in file_path:
                    line = line.strip("\n").split(sep)
                    line_num = line_num + 1
                    if len(line) != fields:
                        raise ValueError(f"'{path}' has {len(line)} fields on line {line_num} but expected {fields}")
                    yield tuple(line)


    def read_students(self, path: str) -> None:
        """A function that analyses the information from students.txt file """
        
        try:
            for cwid, name, major in self.file_reader(os.path.join(self._path, 'students.txt'), 3, sep = "\t", header = False):
                if cwid in self._students:
                    print(f"{cwid} is already exists")
                else:
                    self._students[cwid] = Student(cwid, name, major)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def read_instructors(self, path: str) -> None:
        """A function that analyses the information from instructors.txt file """
        
        try:
            for cwid, name, dept in self.file_reader(os.path.join(self._path, 'instructors.txt'), 3, sep = "\t", header = False):
                if cwid in self._instructors:
                    print(f"{cwid} is already exists")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def read_grades(self, path: str) -> None:
        """A function that analyses the information from grades.txt file """
        
        try:
            for student_cwid, course, grade, instructor_cwid in self.file_reader(os.path.join(self._path, 'grades.txt'), 4, sep ='\t', header = False):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course_grade(course, grade) 
                else:
                    print(f"Student cwid {student_cwid} is not available")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_course_student(course) 
                else:
                    print(f"instructor cwid {instructor_cwid} is not available")
        except ValueError as e:
            print(e)


    def student_prettytable(self) -> None:
        """A function to print pretytable with student information """
        
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


def main():
    try:
        University("F:/SSW-810")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()