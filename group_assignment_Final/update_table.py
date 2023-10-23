import psycopg2
from config import config


def update_student_name(student_id, student_name, student_table):
    """ update student name based on the student id """
    sql = """ UPDATE {}
                SET student_name = %s
                WHERE student_id = %s""".format(student_table)
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (student_name, student_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return "Error"
    finally:
        if conn is not None:
            conn.close()
    return "Updated!"

def update_student_subject(student_id, student_subject, student_table):
    """ update student name based on the student id """
    sql = """ UPDATE {}
                SET student_subject = %s
                WHERE student_id = %s""".format(student_table)
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (student_subject, student_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        return "Error"
    finally:
        if conn is not None:
            conn.close()

    return "Updated!"

def update_student_attendance(student_id, student_attendance, student_table):
    """ update student name based on the student id """
    sql = """ UPDATE {}
                SET student_attendance = %s
                WHERE student_id = %s""".format(student_table)
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (student_attendance, student_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        return "Error"
    finally:
        if conn is not None:
            conn.close()
    return "Updated!"
#update_student_attendance(1111, 'False')