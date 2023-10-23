import psycopg2
from config import config

def insert_student(table, student_list):
    """ insert student into the student table  """
    sql = "INSERT INTO {}(student_id, student_name, student_subject, student_attendance) VALUES(%s, %s, %s, %s)".format(table)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql,student_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return False
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # insert multiple students
    """insert_student([
        ('3333', 'Alvin Handoko', ['ICT01','ICT02'], 'False'),
        ('2222', 'AAA', ['ICT01'],'False'),
        ('1111', 'Alvin H', ['ICT03'],'False')

    ])"""