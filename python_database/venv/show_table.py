import psycopg2
from config import config
def get_tables():
    """ query parts from the parts table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""SELECT *
                FROM pg_catalog.pg_tables
                WHERE schemaname != 'pg_catalog' AND 
                    schemaname != 'information_schema'""")
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
    get_tables()