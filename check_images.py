import sqlite3, json

conn = sqlite3.connect('backend/skincare.db')
c = conn.cursor()
c.execute("SELECT id, name, image_url, gallery FROM products ORDER BY id DESC LIMIT 10")
rows = c.fetchall()
for r in rows:
    print(f"ID:{r[0]}, name:{r[1]}")
    print(f"  image_url: {r[2][:100] if r[2] else 'None'}...")
    print(f"  gallery: {r[3][:100] if r[3] else 'None'}...")
    print()
conn.close()
