# Homework- 12
# Name:Jenal Parmar 
# CWID:10444852

from typing import Dict
from flask import Flask, render_template
import sqlite3

app: Flask = Flask(__name__)

db_path = "F:/SSW-810/Stevens/HW11_Jenal_Parmar_Database.db"

@app.route('/')

def student_details():
    """A function that returns Student details"""

    query = "select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor from students s, grades g, instructors i where s.CWID = g.StudentCWID and i.CWID = g.InstructorCWID order by s.Name"
    db: sqlite3.Connection = sqlite3.connect(db_path)
    result = db.execute(query)

    data: Dict[str, str] = [{ "name": name, "cwid": cwid, "course": course, "grade": grade, "instructor": instructor}
			                for name, cwid, course, grade, instructor in result]
    db.close()

    return render_template('student_details.html',
                            my_header = "Stevens Repository",
                            my_param = "Students Details",
                            students = data)

app.run(debug=True)