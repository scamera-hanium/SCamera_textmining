import pymysql.cursors

def init(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM KEYWORD"
            cursor.execute(sql)
    except:
        pass