"""
定时任务，调度搜索引擎子域名
"""
import requests
import psycopg2


def init():
    conn = psycopg2.connect(host='192.168.199.220', port='5432', user='postgres', password='123456', database='search_engine')
    cur = conn.cursor()
    cur.execute('select domain, province from subdomain')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [x[0]+'|'+x[1] for x in rows]


def dispatch(domains):
    res = requests.post('http://127.0.0.1:5000/search_engine/dispatch', json={'domains': domains})
    print(res.json())


if __name__ == '__main__':
    # domains = init()

    # f = open('2.txt', 'w')
    # with open('1.txt', 'r') as fp:
    #     for x in fp:
    #         f.write(x.strip()+'|河北省')
    #         f.write('\n')

    with open('1.txt', 'r') as fp:
        domains = [x.strip() for x in fp]
    print(len(domains), domains)
    dispatch(domains)

