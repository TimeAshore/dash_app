import json
import psycopg2
import requests


def dispatch(id, domain):
    data = {'id': id, 'domain': domain}
    ans = requests.post('http://icp.socmap.org/api/query', json=data)
    # print(id, domain, ans.json()['data']['icp'], ans.json()['data']['sponsor'], ans.json()['data']['sponsor_type'])
    req = requests.patch('http://127.0.0.1:5000/domain/archived', json={
                                                                'id': id, 'sponsor': ans.json()['data']['sponsor'],
                                                                'sponsor_type': ans.json()['data']['sponsor_type'],
                                                                'icp_number': ans.json()['data']['icp']}
                         )
    print(req.status_code, req.json()['data']['icp_number'])


if __name__ == '__main__':
    domains = []
    with open('domains.txt', 'r') as fp:
        for line in fp:
            domain = line.strip().split(',')
            domains.append((domain[0], domain[1]))
    # print(len(domains))

    for domain in domains:
        dispatch(domain[0], domain[1])
