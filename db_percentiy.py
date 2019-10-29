import pymysql.cursors

def init(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM PERCENTIY"
            cursor.execute(sql)
    except:
        pass

def insert(conn, id, sumnum, addnum, actnum, addper, actper):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO PERCENTIY VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, sumnum, addnum, actnum, addper, actper))
    except:
        pass