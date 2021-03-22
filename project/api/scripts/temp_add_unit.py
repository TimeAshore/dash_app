"""临时脚本"""
import psycopg2

conn = psycopg2.connect(host="192.168.199.17", port="5432", database="socweb_ha", user="postgres", password="123456")
cur = conn.cursor()
cur.execute(
    "select name, spell, category, city_code, region_code, keywords, website_count, domain, tags, domains from unit")
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
print(len(rows), rows)
print(len(city), city)
print(len(region), region)


conn = psycopg2.connect(host="192.168.199.17", port="5432", database="socamas", user="postgres", password="123456")
cur = conn.cursor()
for x in rows:
    cur.execute(
        "insert into unit(name, spell, category, city, region, keywords, website_count, domain, tags, domains) values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s)",
        (x[0], x[1], x[2], city[x[3]], region[x[4]], x[5], x[6], x[7], x[8], x[9]))
conn.commit()
cur.close()
conn.close()
