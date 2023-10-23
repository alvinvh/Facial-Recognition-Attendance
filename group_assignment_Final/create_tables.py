import psycopg2
from config import config


def create_tables(table_name):
    """ create tables in the group_assignment database"""
    commands = (
        """
        CREATE TABLE {} (
            student_id INTEGER PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            student_subject VARCHAR(255) NOT NULL,
            student_attendance BOOLEAN
        )
        """.format(table_name))
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        #for command in commands:
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return False
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()