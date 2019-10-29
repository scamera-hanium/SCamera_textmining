import pymysql.cursors

def setting():
    conn = pymysql.connect(host='15.164.192.198', port=3306, user='davichiar', passwd='1234', db='SCamera', charset='utf8')
    conn.query("set character_set_connection=utf8;")
    conn.query("set character_set_server=utf8;")
    conn.query("set character_set_client=utf8;")
    conn.query("set character_set_results=utf8;")
    conn.query("set character_set_database=utf8;")
    return conn

