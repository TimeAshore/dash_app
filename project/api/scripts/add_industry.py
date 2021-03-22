import json
import psycopg2
import requests


conn = psycopg2.connect(host="192.168.199.17", port="5432", database="socweb_ha", user="postgres", password="123456")
cur = conn.cursor()
cur.execute("select name, spell from industry")
rows = cur.fetchall()
cur.close()
conn.close()


for x in rows:
    url = 'http://127.0.0.1:5001/industry/add'
    data = {
        "name": x[0],
        "spell": x[1]
    }
    res = requests.post(url, data=json.dumps(data))
    print(res.status_code)

