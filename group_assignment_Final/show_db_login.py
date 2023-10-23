import psycopg2
from config import config

def get_students_login(username):
    """ query parts from the parts table """
    conn = None
    try:
        if username == None:
            pass
        else:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT pwd FROM userlogin WHERE username = '{}'".format(username))
            rows = cur.fetchone()
            #print("The number of parts: ", cur.rowcount)
            #for row in rows:
            #    print(row)
            cur.close()
            return str(rows).rstrip("',)").lstrip("('").rstrip(" ")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


#if __name__ == '__main__':
#    get_students()
