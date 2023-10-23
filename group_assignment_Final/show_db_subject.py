import psycopg2
from config import config

def get_students_subject(table):
    """ query parts from the parts table """
    conn = None
    try:
        if table == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT student_id, student_name, student_attendance, student_subject FROM {} ORDER BY student_id".format(table))
            rows = cur.fetchall()
            #print("The number of parts: ", cur.rowcount)
            #for row in rows:
            #    print(row)
            cur.close()
            return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    get_students()
