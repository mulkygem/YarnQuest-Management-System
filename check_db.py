import mysql.connector

try:
    conn = mysql.connector.connect(host='127.0.0.1', user='root', password='')
    cur = conn.cursor()
    cur.execute("SHOW DATABASES LIKE 'yarnquest';")
    print(cur.fetchall())
except Exception as e:
    print('ERROR:', e)
finally:
    try:
        cur.close()
    except Exception:
        pass
    try:
        conn.close()
    except Exception:
        pass
