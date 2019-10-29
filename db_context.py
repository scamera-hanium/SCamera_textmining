import pymysql.cursors

def init(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM CONTEXT"
            cursor.execute(sql)
    except:
        pass

def insert(conn, id, title, link, imglink, context1, date, nicname, add, active, text):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO CONTEXT VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, title, link, imglink, context1, date, nicname, add, active, text))
    except:
        pass

def update_addtext(conn, id, add):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTEXT SET ADD_TEXT = %s WHERE ID = %s"
            cursor.execute(sql, (add, id))
    except:
        pass

def update_activetext(conn, id, active):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTEXT SET ACTIVE_TEXT = %s WHERE ID = %s"
            cursor.execute(sql, (active, id))
    except:
        pass

def update_set(conn, text):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE CONTEXT SET TEXT = %s"
            cursor.execute(sql, (text))
    except:
        pass