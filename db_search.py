import pymysql.cursors

def init(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM search WHERE nameCheck = (%s)"
            cursor.execute(sql, ("1"))
    except:
        pass

def find(conn, check):
    result = []
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM search WHERE nameCheck = %s'
            cursor.execute(sql, (check))
            result = cursor.fetchall()

            print(result[0])
    except:
        pass

    finally:
        return result

def update(conn, name, check):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE search SET nameCheck = %s WHERE name = %s"
            cursor.execute(sql, (check, name))
    except:
        pass