# Homework- 09 Unittest
# Name:Jenal Parmar 
# CWID:10444852

import unittest
from HW09_Jenal_Parmar import Student, Instructor, University

class TestUniversity(unittest.TestCase):

    def test_student(self):
        """A function to test the student info"""
        
        test = University("F:/SSW-810")
        student_list = {cwid: student.student_info() for cwid, student in test._students.items()}
        expected = {'10103': ['10103','Baldwin, C',['CS 501','SSW 564', 'SSW 567', 'SSW 687']],
                    '10115': ['10115','Wyatt, X',['CS 545','SSW 564', 'SSW 567', 'SSW 687']],
                    '10172': ['10172','Forbes, I',['SSW 555', 'SSW 567']],
                    '10175': ['10175','Erickson, D',['SSW 564', 'SSW 567', 'SSW 687']],
                    '10183': ['10183','Chapman, O',['SSW 689']],
                    '11399': ['11399','Cordova, I',['SSW 540']],
                    '11461': ['11461','Wright, U',['SYS 611','SYS 750', 'SYS 800']],
                    '11658': ['11658','Kelly, P',['SSW 540']],
                    '11714': ['11714','Morton, A',['SYS 611','SYS 645']],
                    '11788': ['11788','Fuller, E',['SSW 540']]}
        self.assertEqual(student_list, expected)


    def test_instructor(self):
        """A function to test the instructor info"""
        
        test = University("F:/SSW-810")
        instructor_list = {tuple(i) for instructor in test._instructors.values() for i in instructor.instructor_info()}
        expected = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}
        self.assertEqual(instructor_list, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)