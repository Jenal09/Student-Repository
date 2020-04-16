# Homework- 11 Unittest
# Name:Jenal Parmar 
# CWID:10444852

import unittest
from HW11_Jenal_Parmar import Major, Student, Instructor, University

class TestUniversity(unittest.TestCase):

    def test_major_summary(self) -> None:
        """Test the major summary"""
        
        test = University("C:/Users/parma/Desktop/HW11")
        major_list = {mjr: Major.major_info() for mjr, Major in test._majors.items()}
        expected = {'SFEN': ['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'] ,['CS 501', 'CS 546']],
                    'CS': ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]}
        self.assertEqual(major_list, expected)

    def test_student_summary(self) -> None:
        """Test the student summary"""
        
        test = University("C:/Users/parma/Desktop/HW11")
        student_list = list()
        for cwid, Student in test._students.items():
            student_list.append(Student.student_info())
        expected = [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38],
                    ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 4.0], 
                    ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'],['CS 501', 'CS 546'], 4.0], 
                    ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5]]
        self.assertEqual(student_list, expected)

    def test_instructor_summary(self) -> None:
        """ Test the instructor summary """
        
        test = University("C:/Users/parma/Desktop/HW11")
        instructor_list = {tuple(i) for instructor in test._instructors.values() for i in instructor.instructor_info()}
        expected = {('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
                    ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                    ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                    ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                    ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                    ('98762', 'Hawking, S', 'CS', 'CS 570', 1)}
        self.assertEqual(instructor_list, expected)

    def test_student_grades_table_db(self) -> None:
        """Test student grade summary"""
        
        test = University("C:/Users/parma/Desktop/HW11")
        student_grade_list = list()
        for row in test.student_grades_table_db("F:/SSW-810/Stevens/HW11_Jenal_Parmar_Database.db"):
            student_grade_list.append(row)
        expected = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                    ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                    ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                    ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                    ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                    ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                    ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                    ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                    ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]
        self.assertCountEqual(student_grade_list, expected)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)