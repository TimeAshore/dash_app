""" 补全主域名信息 """
import json
import psycopg2
import requests
from project.api.bizs import IcpBiz
from project import create_app

app = create_app()
app.app_context().push()


def get_data_from_socweb():
    """
    抽取socweb未备案主域名
    :return:
    """
    conn = psycopg2.connect(database="socweb_ha", user="postgres", password="123456", host="192.168.199.17", port="5432")
    cur = conn.cursor()
    cur.execute("select code, name from city")
    citys = cur.fetchall()
    cur.execute("select code, name from region")
    regions = cur.fetchall()

    city = {}
    for x in citys:
        city[x[0]] = x[1]
    region = {}
    for x in regions:
        region[x[0]] = x[1]
    print(len(city), city)
    print(len(region), region)

    f = open('socweb_domain_no_sponsor.txt', 'w')
    with open('del.txt', 'r') as fp:
        for x in fp:
            domain = x.strip()
            cur.execute("SELECT name, city_code, region_code, icp, sponsor, sponsor_type FROM domain_archived where name=%s", (domain,))
            rows = cur.fetchall()
            for i in rows:
                if i[1] is None:
                    cit = ''
                else:
                    cit = str(city[i[1]])
                if i[2] is None:
                    reg = ''
                else:
                    reg = str(region[i[2]])
                f.write(i[0] + ',' + cit + ',' + reg + ',' + i[3] + ',' + i[4] + ',' + i[5])
                f.write('\n')

    cur.close()
    conn.close()
    f.close()


def core_domain():
    """
    添加到socamas
    :return:
    """
    url = 'http://172.30.0.193:5000/domain/archived'
    with open('socweb_domain_no_sponsor.txt', 'r') as fp:
        for line in fp.readlines():
            line = line.strip().split(',')
            # haut.edu.cn,省直,省直,豫ICP备05002475号-1,河南工业大学,个人
            data = {
                'name': line[0],
                'icp_number': line[3],
                'sponsor': line[4],
                'sponsor_type': line[5],
                'city_code': line[1],
                'region_code': line[2],
            }
            resp = requests.post(url, json=data)
            print(resp.json())


def fix_location():
    """
    补全主域名归属地
    :return:
    """
    conn = psycopg2.connect(database="socamas", user="postgres", password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT id, name, sponsor FROM domain_archived where sponsor!='未备案' and city_code=''")
    rows = cur.fetchall()
    print(len(rows))
    cur.close()
    conn.close()

    # 用备案单位识别归属地信息
    patch_url = 'http://127.0.0.1:5000/domain/archived'

    icp_biz = IcpBiz()
    for x in rows:
        area = icp_biz.recognize_area(x[2])
        area['id'] = x[0]
        area['city_code'] = area['city']
        area['region_code'] = area['region']
        area.pop('city')
        area.pop('region')
        res = requests.patch(patch_url, data=json.dumps(area))
        print(res.status_code)


if __name__ == '__main__':
    get_data_from_socweb()
    core_domain()
    fix_location()
