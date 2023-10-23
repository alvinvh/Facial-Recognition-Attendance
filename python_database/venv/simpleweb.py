from flask import Flask, redirect, url_for, render_template, request, sessions

from show_db import get_students
from create_tables import create_tables
from insert_student import insert_student
from show_table import get_tables

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/showdatabase/", methods=["GET","POST"])

def showdatabase_init():
    dropdownlist = []
    list = get_tables()
    for i in list:
        dropdownlist.append(i[1])
    return render_template("show_database.html", dropdownlist=dropdownlist)

@app.route("/showdatabase/<table_name>", methods=["GET","POST"])
def showdatabase(table_name):
    data = get_students(table_name)
    dropdownlist = []
    list = get_tables()
    for i in list:
        dropdownlist.append(i[1])
    return render_template("show_database.html", data=data, dropdownlist=dropdownlist)

@app.route("/showdb", methods=["GET","POST"])
def showdb():
    table_name = request.form.get("table_name")

    return redirect(url_for('showdatabase', table_name = table_name))


@app.route("/add_student", methods=['POST', 'GET'])
def add_student():

    table_name = request.form.get("table_name")
    student_id = request.form.get("student_id")
    student_name = request.form.get("student_name")
    student_subject = request.form.get("student_subject")
    student_subject = student_subject.replace(" ","").split(',')


    reply = insert_student(table_name,(student_id, student_name, student_subject, False))
    if reply == True:
        message = "Student ID: {}\n" \
                  "Student Name: {}\n" \
                  "Student Subject: {}\n" \
                  "Successfully recorded!!".format(student_id,student_name,student_subject)
    else:
        message = "Error occured"


    return redirect(url_for('form_student', message = message))

@app.route("/insert_student/")
def form_student_init():
    dropdownlist = []
    list = get_tables()
    for i in list:
        dropdownlist.append(i[1])
    return render_template("insert_student.html", dropdownlist=dropdownlist)

@app.route("/insert_student/<message>")
def form_student(message):
    dropdownlist = []
    list = get_tables()
    for i in list:
        dropdownlist.append(i[1])
    return render_template("insert_student.html", dropdownlist=dropdownlist, message=message)

@app.route("/addtable/")

def addtable_init():
    return render_template("create_table.html")

@app.route("/addtable/<message>")

def addtable(message):
    return render_template("create_table.html", message=message)

@app.route("/form_table", methods=["POST", "GET"])

def form_table():
    classroom = request.form.get("classroom")
    db_reply = create_tables(classroom)
    if db_reply == True:
        return redirect(url_for('addtable', message="Classroom {} created!".format(classroom)))
    else:
        return redirect(url_for('addtable', message="Failed to create {} classroom!".format(classroom)))

if __name__ == "__main__":
    app.run()