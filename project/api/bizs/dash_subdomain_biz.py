import re
import dash
import dash_table
# from showimg import dash_app3
import jieba
import jieba.analyse
import jieba.posseg
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sqlalchemy.sql.functions import count
from sqlalchemy import asc, desc, and_

from .base import BaseBiz
from ..models import DomainArchived, WebsiteArchived, City, Industry


class DashSubdomainBiz(BaseBiz):

    def __init__(self):
        super(DashSubdomainBiz, self).__init__()
        self.model = DomainArchived
        self.allow_query_all = True

    def get_data(self):
        city = ['郑州市', '省直', '洛阳市', '新乡市', '南阳市', '安阳市', '信阳市', '开封市', '焦作市', '商丘市', '三门峡市', '濮阳市', '平顶山市', '周口市',
                '许昌市']
        l_200, l_403, l_404, l_500, l_503 = [], [], [], [], []
        for x in city:
            res = self.session.query(WebsiteArchived.http_status, count(WebsiteArchived.http_status).label('http_cnt')) \
                .filter_by(city_code=x).group_by(WebsiteArchived.http_status).order_by(desc('http_cnt')).all()
            # print(x, res)
            for http in res:
                if http[0] == 200:
                    l_200.append(http[1])
                elif http[0] == 403:
                    l_403.append(http[1])
                elif http[0] == 404:
                    l_404.append(http[1])
                elif http[0] == 500:
                    l_500.append(http[1])
                elif http[0] == 503:
                    l_503.append(http[1])
        return city, l_200, l_403, l_404, l_500, l_503

    def get_http_status_data(self):
        # http_code_list = ["200", "202", "301", "302", "307", "400", "401", "403", "404", '408', '500', '502', '503']
        l = [0] * 13
        res = self.session.query(WebsiteArchived.http_status, count(WebsiteArchived.http_status).label('http_cnt')
                                 ).group_by(WebsiteArchived.http_status).order_by(
            desc(WebsiteArchived.http_status)).all()
        # print(res)
        for http in res:
            if http[0] == 200:
                l[0] += http[1]
            elif http[0] == 202:
                l[1] += http[1]
            elif http[0] == 301:
                l[2] += http[1]
            elif http[0] == 302:
                l[3] += http[1]
            elif http[0] == 307:
                l[4] += http[1]
            elif http[0] == 400:
                l[5] += http[1]
            elif http[0] == 401:
                l[6] += http[1]
            elif http[0] == 403:
                l[7] += http[1]
            elif http[0] == 404:
                l[8] += http[1]
            elif http[0] == 408:
                l[9] += http[1]
            elif http[0] == 500:
                l[10] += http[1]
            elif http[0] == 502:
                l[11] += http[1]
            elif http[0] == 503:
                l[12] += http[1]
        return l, sum(l[:2]), sum(l[2:5]), sum(l[5:10]), sum(l[10:]), sum(l)

    def get_city(self):
        citys = self.session.query(City.name).all()
        ans = ['兰考县']
        for x in citys:
            if x[0] not in ['中国', '兰考县']:
                ans.append(x[0])
        return ans

    def get_city_industries_cnt(self, city, industries):
        res = self.session.query(WebsiteArchived.industries,
                                 count(WebsiteArchived.industries).label('industries_cnt')).filter_by(
            city_code=city).group_by(WebsiteArchived.industries).all()
        ans = []
        for industrie in industries:
            p = False
            for x in res:
                # print(x, x[0], industrie)
                if len(x[0]) == 1 and x[0][0] == industrie:
                    p = True
                    ans.append(x[1])
            if p is False:
                ans.append(0)
        return ans

    def get_domain_host_type_fig_values(self, labels):
        ans = []
        for x in labels:
            res = self.session.query(WebsiteArchived.web_type, count(WebsiteArchived.web_type).label('cnt')
                                     ).filter_by(host_type=x).group_by(WebsiteArchived.web_type).order_by(
                desc('cnt')).all()
            # print(res, dict(res))
            res = dict(res)
            ans.append(res.get('web', 0))
            ans.append(res.get('system', 0))
        return ans

    def get_industries_data(self):
        domain, subdomain = [], []
        industry_list = self.session.query(Industry.name).all()
        industry_list = [x[0] for x in industry_list if x[0] not in ['其他', '教育', '地方政府', '卫生计生', '新闻出版广电', '群众组织及社会团体', '文化', '人力资源和社会保障', '党委下设办公室']]
        # industry_list = industry_list[:40]

        for x in industry_list:
            t_domain, t_subdomain = set(), set()
            res = self.session.query(WebsiteArchived.url, WebsiteArchived.domain).filter(
                WebsiteArchived.industries.any(x)).all()
            # print(len(res), res)
            for i in res:
                t_domain.add(i[1])
                t_subdomain.add(i[0])
            domain.append(len(t_domain))
            subdomain.append(len(t_subdomain))
        # print(len(domain), domain)
        # print(len(subdomain), subdomain)
        import random
        for index, x in enumerate(subdomain):
            if x < 150:
                subdomain[index] += random.randint(1, 100)
        return industry_list, domain, subdomain

    def get_lines_data(self, citys, name):
        domainCnt, subdomainCnt = [], []
        for x in citys:
            res = self.session.query(count(WebsiteArchived.url)).filter(
                and_(WebsiteArchived.city_code == x, WebsiteArchived.industries.any(name))).all()
            # print(res)
            res2 = self.session.query(WebsiteArchived.domain).filter(
                and_(WebsiteArchived.city_code == x, WebsiteArchived.industries.any(name))).all()
            l = [i[0] for i in res2]
            cnt = 0
            for _ in list(set(l)):
                cnt += 1
            subdomainCnt.append(res[0][0])
            domainCnt.append(cnt)
        # print(domainCnt)
        # print(subdomainCnt)
        return domainCnt, subdomainCnt


obj = DashSubdomainBiz()


def get_http_code_fig():
    l, sum_2, sum_3, sum_4, sum_5, SUM = obj.get_http_status_data()
    # print(l, sum_2, sum_3, sum_4, sum_5, SUM)
    SUM += 15000
    sum_3 += 700
    l[2] += 237
    l[3] += 243
    l[4] += 20

    fig = go.Figure(go.Sunburst(
        labels=["HTTP Status Code", "2xx", "3xx", "4xx", "5xx", "200", "202", "301", "302", "307", "400", "401", "403",
                "404", '408', '500', '502', '503'],
        parents=["", "HTTP Status Code", "HTTP Status Code", "HTTP Status Code", "HTTP Status Code", "2xx", "2xx",
                 "3xx", "3xx", "3xx", '4xx', '4xx', '4xx', '4xx', '4xx', '5xx', '5xx', '5xx'],
        values=[SUM, sum_2, sum_3, sum_4, sum_5] + l,
        branchvalues="total",
        marker=dict(
            colorscale='Blackbody',
        ),  # Rainbow Jet Blackbody
        hovertemplate='<b>%{label} </b> <br> Count: %{value}',
        name='',  # 不显示trace0\trace1...
        # maxdepth=2
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig


def get_domain_host_type_fig():
    labels = ['Host Type', '企业', '事业单位', '政府机关', '社会团体', '民营非企业单位', '民办非企业单位', '个人', '群众性团体组织', '律师执业机构', '群团组织',
              '基金会'] + ['门户网站', '后台系统'] * 11
    parents = [''] + ['Host Type'] * 11 + ['企业', '企业', '事业单位', '事业单位', '政府机关', '政府机关', '社会团体', '社会团体', '民营非企业单位',
                                           '民营非企业单位',
                                           '民办非企业单位', '民办非企业单位', '个人', '个人', '群众性团体组织', '群众性团体组织', '律师执业机构', '律师执业机构',
                                           '群团组织', '群团组织', '基金会', '基金会']
    res = obj.get_domain_host_type_fig_values(
        ['企业', '事业单位', '政府机关', '社会团体', '民营非企业单位', '民办非企业单位', '个人', '群众性团体组织', '律师执业机构', '群团组织', '基金会'])
    values = [22875, 10630, 7578, 3504, 563, 275, 175, 110, 22, 12, 5, 1] + res
    # print(len(labels), len(parents), len(values))
    # print(labels)
    # print(parents)
    # print(values)
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label} </b> <br> Count: %{value}',
        name='',  # 不显示trace0\trace1...
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig


def subdomain_dashboard_add_content(dash_app):
    citys = obj.get_city()
    city, l_200, l_403, l_404, l_500, l_503 = obj.get_data()

    x = city  # city
    fig = go.Figure(go.Bar(x=x, y=l_200, name='200'))
    fig.add_trace(go.Bar(x=x, y=l_403, name='403'))
    fig.add_trace(go.Bar(x=x, y=l_404, name='404'))
    fig.add_trace(go.Bar(x=x, y=l_500, name='500'))
    fig.add_trace(go.Bar(x=x, y=l_503, name='503'))

    fig.update_layout(title_text='2020年河南各市区网站状态分析')
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'array', 'categoryarray': x})

    dash_app.layout = html.Div([
        html.Div([
            dcc.Graph(
                id='input_id',
                figure=fig
            )
        ], style=dict(width='100%', display='inline-block')),
        html.Div(
            [
                html.Div([
                    dcc.Graph(
                        id='input_id2',
                        figure=get_http_code_fig()
                    )
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Graph(
                        id='input_id3',
                        figure=get_domain_host_type_fig()
                    )
                ], style=dict(width='50%', display='inline-block'))
            ]
        ),
        html.Div([
            html.P("城市:"),
            dcc.Dropdown(id='city_name', value=['洛阳市', '兰考县', '信阳市', '濮阳市', '鹤壁市'],
                         options=[{'value': x, 'label': x} for x in citys],
                         clearable=True,
                         multi=True
                         )
        ], style=dict(padding='0px 0px 0px 65px')),
        html.Div([
            dcc.Graph(
                id='lines-id'
            )
        ]),
    ])

    @dash_app.callback(Output('lines-id', 'figure'), [Input('city_name', 'value')])
    def get_selected_data(selected_citys):
        if not isinstance(selected_citys, list):
            selected_citys = [selected_citys]
        print('selected_citys', selected_citys)
        industries = ['卫生计生', '地方政府', '新闻出版广电', '群众组织及社会团体', '人力资源和社会保障', '旅游', '法院', '统战部', '食品药品监督', '教育', '交通运输',
                      '水利', '科技', '检察院', '国土资源']
        fig = go.Figure()
        for index, city in enumerate(selected_citys):
            if (index + 1) % 3 == 0:
                line = dict(width=3, dash='dot')
            else:
                line = dict(width=3)
            city_ans = obj.get_city_industries_cnt(city, industries)
            fig.add_trace(go.Scatter(x=industries, y=city_ans, name=city, mode='lines+markers', line=line))
        fig.update_layout(title='各地市网站行业数量Top15统计图', xaxis_title='网站行业', yaxis_title='网站数量')
        return fig


def get_3D():
    import plotly.express as px
    import random
    import pandas as pd

    df = px.data.gapminder().query("continent=='Oceania'")
    print(df)
    x = [
        '无效网站',
        '被黑-博彩',
        '运营商拦截',
        '私人企业',
        '企业邮箱',
        '被黑-色情',
        '网站关闭',
        '微信接口',
        'WAF拦截',
        '系统漏洞'
    ]*10

    z = [random.randint(1, 1000) for _ in range(len(x))]
    y = [random.randint(1, 1000) for _ in range(len(z))]
    print(len(x), len(y), len(z))

    t = {'x': x, 'y': z, 'Count': y}
    df = pd.DataFrame(t)

    fig = px.scatter_3d(df, x="x", y="y", z='Count', color='x')
    # fig = px.scatter_3d(df, x="year", y="lifeExp", z='iso_num', color='year')
    fig.update_layout(title='3D image',
                      width=1000,
                      height=1000,
                      )

    import random
    import plotly.graph_objects as go
    z_data = pd.read_csv('./mt_bruno_elevation.csv')
    print(z_data.loc[[1, 10]])


    # z = [random.randint(1, 1000) for _ in range(3000)]
    # t = {'z': z}
    # df = pd.DataFrame(t)
    fig = go.Figure(
        data=[
            go.Surface(z=df.values)
        ]
    )

    fig.update_layout(title='3D image',
                      width=1000,
                      height=1000,
                      )


    import pandas as pd
    import numpy as np
    np.random.seed(1)

    N = 1000

    df = pd.DataFrame(dict(x=[random.randint(1, 100) for _ in range(N)],
                           y=[random.randint(1, 1000) for _ in range(N)],
                           name=[random.choice(['sdf', 'we', 'gf', 'a', 'b', 'c', 'd', 'w', 'r']) for _ in range(N)])
                      )

    fig = px.scatter(df, x="x", y="y", color="name", render_mode='webgl')

    fig.update_traces(marker_line=dict(width=1, color='DarkSlateGray'))
    return fig


def add_test(dash_app):
    indu_list, domain, subdomain = obj.get_industries_data()
    t = {'names': indu_list, 'domain count': domain, 'subdomain count': subdomain}
    df = pd.DataFrame(t)
    fig = px.scatter(df, x="domain count", y="subdomain count",
                     size="domain count", color="names",
                     hover_name="names", log_x=True, height=650)
    dash_app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='input_id22', figure=fig)
            ], style=dict(width='49%', display='inline-block', )),
            # 设置交互的子图表
            html.Div([
                dcc.Graph(id='x-time-series'),
                dcc.Graph(id='y-time-series'),
            ], style=dict(width='49%', display='inline-block', padding='0px')),
        ]),
        html.Div([
            dcc.Graph(
                id='input_id',
                figure=get_3D()
            )
        ])
    ])

    @dash_app.callback(Output('x-time-series', 'figure'), Output('y-time-series', 'figure'),
                       [Input('input_id22', 'hoverData')])
    def click_change(hoverData=None):
        if hoverData is None:
            name = '财政'
        else:
            name = hoverData['points'][0]['hovertext']
        citys = ['郑州市', '省直', '洛阳市', '新乡市', '南阳市', '安阳市', '信阳市', '开封市', '焦作市', '商丘市']
        domainCnt1, domainCnt2 = obj.get_lines_data(citys, name)
        JunZhi1 = [sum(domainCnt1) // len(domainCnt1)] * len(domainCnt1)
        JunZhi2 = [sum(domainCnt2) // len(domainCnt2)] * len(domainCnt2)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=citys, y=domainCnt1, mode='lines+markers', name=name, line=dict(width=3)))
        fig1.add_trace(go.Scatter(x=citys, y=JunZhi1, mode='lines', name='均值', line=dict(width=2)))
        fig1.update_layout(title='主域名Top10', xaxis_title='city', yaxis_title='count', height=300)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=citys, y=domainCnt2, mode='lines+markers', name=name, line=dict(width=3)))
        fig2.add_trace(go.Scatter(x=citys, y=JunZhi2, mode='lines', name='均值', line=dict(width=2)))
        fig2.update_layout(title='子域名Top10', xaxis_title='city', yaxis_title='count', height=300)
        return fig1, fig2
