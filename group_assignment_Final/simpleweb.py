from flask import Flask, redirect, url_for, render_template, Response, request, session
from show_db import get_students
from facial_req import facereceog
from show_db import get_students
from create_tables import create_tables
from insert_student import insert_student
from show_table import get_tables
from headshots_picam import headshot
from train_model import dataset_train
from delete_student import delete_student
from update_table import update_student_attendance, update_student_subject, update_student_name
from show_db_subject import get_students_subject
from show_db_login import get_students_login
import hashlib
app = Flask(__name__)
app.secret_key = "group5"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["pwd"]
        hash = hashlib.md5(str(pwd).encode('utf-8'))
        a = get_students_login(user)
        b = hash.hexdigest()
        if a == b:
            session["user"] = user
            return redirect("/facerecog_choice")
        else:
            return render_template("login.html", message = "Login Error")
    else:
        if "user" in session:
            return redirect("/facerecog_choice")

        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/home/<table>", methods=["GET","POST"])
def home(table):
    if "user" in session:
        #table = request.form.get("table_name")
        #dataset_train(table)
        return render_template("index.html", table=table)
    else:
        return redirect(url_for("login"))

@app.route("/facerecog/<table>", methods = ["GET", "POST"])
def facerecog(table):
    if "user" in session:
        return Response(facereceog(table), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for("login"))
@app.route("/faces_processing", methods = ["GET", "POST"])
def faces_processing():
    if "user" in session:
        table = request.form.get("table_name")
        dataset_train(table)
        return redirect("/home/{}".format(table))
    else:
        return redirect(url_for("login"))
@app.route("/facerecog_choice")
def choose_table():
    if "user" in session:
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("table_choice.html", dropdownlist=dropdownlist)
    else:
        return redirect(url_for("login"))



@app.route("/showdatabase/", methods=["GET","POST"])

def showdatabase_init():
    if "user" in session:
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("show_database.html", dropdownlist=dropdownlist)
    else:
        return redirect(url_for("login"))


@app.route("/showdatabase/<table_name>", methods=["GET","POST"])
def showdatabase(table_name):
    if "user" in session:
        data = get_students(table_name)
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("show_database.html", data=data, dropdownlist=dropdownlist)
    else:
        return redirect(url_for("login"))


@app.route("/showdb", methods=["GET","POST"])
def showdb():
    if "user" in session:
        table_name = request.form.get("table_name")

        return redirect(url_for('showdatabase', table_name=table_name))
    else:
        return redirect(url_for("login"))



@app.route("/add_student", methods=['POST', 'GET'])
def add_student():
    if "user" in session:
        table_name = request.form.get("table_name")
        student_id = request.form.get("student_id")
        student_name = request.form.get("student_name")
        student_subject = request.form.get("student_subject")
        student_subject = student_subject.replace(" ", "").split(',')

        reply = insert_student(table_name, (student_id, student_name, student_subject, False))
        if reply == True:
            message = "Student ID: {}\n" \
                      "Student Name: {}\n" \
                      "Student Subject: {}\n" \
                      "Successfully recorded!!".format(student_id, student_name, student_subject)
        else:
            message = "Error occured"

        return redirect(url_for('form_student', message=message))
    else:
        return redirect(url_for("login"))


@app.route("/insert_student/")

def form_student_init():
    if "user" in session:
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("insert_student.html", dropdownlist=dropdownlist)
    else:
        return redirect(url_for("login"))


@app.route("/insert_student/<message>")
def form_student(message):
    if "user" in session:
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("insert_student.html", dropdownlist=dropdownlist, message=message)
    else:
        return redirect(url_for("login"))


@app.route("/addtable/")

def addtable_init():
    if "user" in session:
        return render_template("create_table.html")
    else:
        return redirect(url_for("login"))


@app.route("/addtable/<message>")

def addtable(message):
    if "user" in session:
        return render_template("create_table.html", message=message)
    else:
        return redirect(url_for("login"))


@app.route("/form_table", methods=["POST", "GET"])

def form_table():
    if "user" in session:
        classroom = request.form.get("classroom")
        db_reply = create_tables(classroom)
        if db_reply == True:
            return redirect(url_for('addtable', message="Classroom {} created!".format(classroom)))
        else:
            return redirect(url_for('addtable', message="Failed to create {} classroom!".format(classroom)))
    else:
        return redirect(url_for("login"))






@app.route("/add_student_face")
def add_student_face():
    if "user" in session:
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("table_choice_face_2.html", dropdownlist=dropdownlist)
    else:
        return redirect(url_for("login"))


@app.route("/add_student_face_2", methods = ["GET", "POST"])
def add_student_face_2():
    if "user" in session:
        table = request.form.get("table_name")
        dropdownlist = []
        list = get_students(table)
        for i in list:
            dropdownlist.append(i[0])
        return render_template("table_choice_face.html", dropdownlist=dropdownlist, table=table)
    else:
        return redirect(url_for("login"))


@app.route("/add_student_face_3", methods = ["GET", "POST"])
def add_student_face_3():
    if "user" in session:
        table = request.form.get("table_name")
        id = request.form.get("student_id")
        headshot(id, table)
        return redirect("/add_student_face")
    else:
        return redirect(url_for("login"))


@app.route("/student_update")
def student_update():
    if "user" in session:
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("student_update_table_choice.html", dropdownlist=dropdownlist)
    else:
        return redirect(url_for("login"))


@app.route("/student_update_/<message>", methods = ["GET", "POST"])
def student_update_(message):
    if "user" in session:
        dropdownlist = []
        list = get_tables()
        for i in list:
            dropdownlist.append(i[1])
        return render_template("student_update_table_choice.html", dropdownlist=dropdownlist, message=message)
    else:
        return redirect(url_for("login"))


@app.route("/student_update_2", methods = ["GET", "POST"])
def student_update_2():
    if "user" in session:
        table = request.form.get("table_name")
        dropdownlist = ["Update Student Name", "Update Student Subject", "Update Student Attendance", "Delete Student"]
        return render_template("student_update_update_choice.html", dropdownlist=dropdownlist, table=table)
    else:
        return redirect(url_for("login"))


@app.route("/student_update_3", methods = ["GET", "POST"])
def student_update_3():
    if "user" in session:
        table = request.form.get("table_name")
        choice = request.form.get("choice")
        if choice == "Delete Student":
            data = get_students(table)
            dropdownlist = []
            list = get_students(table)
            for i in list:
                dropdownlist.append(i[0])
            return render_template("student_update_delete.html", dropdownlist=dropdownlist, table=table, data=data)
        elif choice == "Update Student Attendance":
            data = get_students(table)
            dropdownlist = ["True", "False"]
            dropdownlist_stu = []
            list = get_students(table)
            for i in list:
                dropdownlist_stu.append(i[0])
            return render_template("student_update_attendance.html", dropdownlist=dropdownlist, table=table, data=data,
                                   dropdownlist_stu=dropdownlist_stu)
        elif choice == "Update Student Name":
            data = get_students_subject(table)
            dropdownlist_stu = []
            list = get_students(table)
            for i in list:
                dropdownlist_stu.append(i[0])
            return render_template("student_update_name_subject.html", table=table, data=data,
                                   dropdownlist_stu=dropdownlist_stu, choice="Student Name")
        elif choice == "Update Student Subject":
            data = get_students_subject(table)
            dropdownlist_stu = []
            list = get_students(table)
            for i in list:
                dropdownlist_stu.append(i[0])
            return render_template("student_update_name_subject.html", table=table, data=data,
                                   dropdownlist_stu=dropdownlist_stu, choice="Student Subject")
    else:
        return redirect(url_for("login"))


@app.route("/student_update_delete", methods = ["GET", "POST"])
def student_update_delete():
    if "user" in session:
        table = request.form.get("table_name")
        student_id = request.form.get("student_id")
        delete_student(table, student_id)
        return redirect("/student_update_/{}".format("Deleted!"))
    else:
        return redirect(url_for("login"))


@app.route("/student_update_attendance", methods = ["GET", "POST"])
def student_update_attendance():
    if "user" in session:
        table = request.form.get("table_name")
        student_id = request.form.get("student_id")
        attendance = request.form.get("student_attendance")
        message = update_student_attendance(student_id, attendance, table)
        return redirect("/student_update_/{}".format(message))
    else:
        return redirect(url_for("login"))


@app.route("/student_update_name_subject", methods = ["GET", "POST"])
def student_update_name_subject():
    if "user" in session:
        table, choice = request.form.get("table_name").split(",")
        student_id = request.form.get("student_id")
        student_data = request.form.get("student_data")
        if choice == "Student Name":
            message = update_student_name(student_id, student_data, table)
        elif choice == "Student Subject":
            message = update_student_subject(student_id, student_data, table)
        return redirect("/student_update_/{}".format(message))
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()