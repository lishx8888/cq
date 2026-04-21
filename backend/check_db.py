import sqlite3
conn = sqlite3.connect('skincare.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])
if ('videos',) in tables:
    cursor.execute('SELECT * FROM videos LIMIT 1')
    cols = [d[0] for d in cursor.description]
    print('Videos columns:', cols)
conn.close()