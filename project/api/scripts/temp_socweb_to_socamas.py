"""老版Data  -->  新版"""
import requests
import psycopg2

conn = psycopg2.connect(host="192.168.199.17", port="5432", database="socweb_ha", user="postgres", password="123456")
cur = conn.cursor()
cur.execute(
    "select url, name, domain, ip, ip_area, host_dept, host_type, industries, city_code, region_code, category, http_status, tags, web_type  from website_archived")
rows = cur.fetchall()
cur.execute("select code, name from city")
citys = cur.fetchall()
cur.execute("select code, name from region")
regions = cur.fetchall()
cur.close()
conn.close()

city = {}
for x in citys:
    city[x[0]] = x[1]
region = {}
for x in regions:
    region[x[0]] = x[1]
print(len(rows))
print(len(city), city)
print(len(region), region)

for x in rows:
    x = list(x)
    if x[8] is None:
        x[8] = ''
    else:
        x[8] = city[x[8]]
    if x[9] is None:
        x[9] = ''
    else:
        x[9] = region[x[9]]
    data = {
        'url': x[0],
        'title': x[1],
        'domain': x[2],
        'ip': x[3],
        'ip_area': x[4],
        'host_dept': x[5],
        'host_type': x[6],
        'industries': x[7],
        'city_code': x[8],
        'region_code': x[9],
        'category': x[10] if x[10] else '',
        'http_status': x[11],
        'tags': x[12],
        'web_type': x[13]
    }
    res = requests.post('http://172.30.0.193:5000/website/archived', json=data)
    if res.status_code != 201:
        print(res)
