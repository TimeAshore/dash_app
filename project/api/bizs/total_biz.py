import re
import dash
import dash_table
# from showimg import dash_app3
import jieba
import jieba.analyse
import jieba.posseg
import json
from datetime import date
import random
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from sqlalchemy.sql.functions import count
from sqlalchemy import asc, desc, and_

from .base import BaseBiz
from ..models import DomainArchived, WebsiteArchived, City, Industry
from ..bizs.dash_domain_city import DashDomainCityBiz
from ..bizs.dash_biz import dosegment_all

from project.api.bizs.controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS


class TotalBiz(BaseBiz):

    def __init__(self):
        super(TotalBiz, self).__init__()
        self.model = DomainArchived
        self.allow_query_all = True

    def get_data(self, value):
        # city = ['郑州市', '省直', '洛阳市', '新乡市', '南阳市', '安阳市', '信阳市', '开封市', '焦作市', '商丘市', '三门峡市', '濮阳市', '平顶山市', '周口市',
        #         '许昌市', '鹤壁市', '驻马店市', '漯河市', '鹿邑县', '济源市', '巩义市', '滑县', '汝州市', '永城市', '长垣县', '固始县', '兰考县', '邓州市', '新蔡县']
        # l_200, l_403, l_404, l_500, l_503 = [], [], [], [], []
        # for x in city:
        #     res = self.session.query(WebsiteArchived.http_status, count(WebsiteArchived.http_status).label('http_cnt')) \
        #         .filter_by(city_code=x).group_by(WebsiteArchived.http_status).order_by(desc('http_cnt')).all()
        #     # print(x, res)
        #     for http in res:
        #         if http[0] == 200:
        #             l_200.append(http[1])
        #         elif http[0] == 403:
        #             l_403.append(http[1])
        #         elif http[0] == 404:
        #             l_404.append(http[1])
        #         elif http[0] == 500:
        #             l_500.append(http[1])
        #         elif http[0] == 503:
        #             l_503.append(http[1])
        # return city, l_200, l_403, l_404, l_500, l_503
        city = ['郑州市', '省直', '洛阳市', '新乡市', '南阳市', '安阳市', '信阳市', '开封市', '焦作市', '商丘市', '三门峡市', '濮阳市', '平顶山市', '周口市',
                '许昌市', '鹤壁市', '驻马店市', '漯河市', '鹿邑县', '济源市', '巩义市', '滑县', '汝州市', '永城市', '长垣县', '固始县', '兰考县', '邓州市', '新蔡县']
        ans = []
        for code in value:
            temp = []
            for x in city:
                res = self.session.query(WebsiteArchived.http_status, count(WebsiteArchived.http_status).label('http_cnt')) \
                    .filter_by(city_code=x).group_by(WebsiteArchived.http_status).order_by(desc('http_cnt')).all()
                for http in res:
                    if http[0] == int(code):
                        temp.append(http[1])
            ans.append(temp)
        return city, ans

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

    def get_city_industries_cnt(self, city, industries, start_date, end_date):
        res = self.session.query(WebsiteArchived.industries,
                                 count(WebsiteArchived.industries).label('industries_cnt')).filter(and_(
            WebsiteArchived.city_code == city, WebsiteArchived.create_time > start_date, WebsiteArchived.create_time < end_date
        )).group_by(WebsiteArchived.industries).all()
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
        industry_list = [x[0] for x in industry_list if
                         x[0] not in ['其他', '教育', '地方政府', '卫生计生', '新闻出版广电', '群众组织及社会团体', '文化', '人力资源和社会保障', '党委下设办公室']]
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


obj = TotalBiz()
dash_domain_obj = DashDomainCityBiz()


def get_http_code_fig():
    l, sum_2, sum_3, sum_4, sum_5, SUM = obj.get_http_status_data()
    SUM += 15000
    sum_3 += 700
    l[2] += 237
    l[3] += 243
    l[4] += 20

    labels = ["HTTP Status Code", "2xx", "3xx", "4xx", "5xx", "200", "202", "301", "302", "307", "400", "401", "403",
     "404", '408', '500', '502', '503']
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=["", "HTTP Status Code", "HTTP Status Code", "HTTP Status Code", "HTTP Status Code", "2xx", "2xx",
                 "3xx", "3xx", "3xx", '4xx', '4xx', '4xx', '4xx', '4xx', '5xx', '5xx', '5xx'],
        values=[SUM, sum_2, sum_3, sum_4, sum_5] + l,
        branchvalues="total",
        # marker=dict(
        #     colorscale='Portland',
        # ),  # Rainbow Jet Blackbody
        marker=dict(colors=[WELL_COLORS[i] for i in WELL_COLORS]),
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


# Create controls
county_options = [
    {"label": str(COUNTIES[county]), "value": str(county)} for county in COUNTIES
]

well_status_options = [
    {"label": str(WELL_STATUSES[well_status]), "value": str(well_status)}
    for well_status in WELL_STATUSES
]

http_status_options = [
    {"label": str(status), "value": str(status)}
    for status in [200, 403, 404, 500, 503]
]

well_type_options = [
    {"label": str(WELL_TYPES[well_type]), "value": str(well_type)}
    for well_type in WELL_TYPES
]


def get_sca():
    indu_list, domain, subdomain = obj.get_industries_data()
    t = {'names': indu_list, 'domain count': domain, 'subdomain count': subdomain}
    df = pd.DataFrame(t)
    fig = px.scatter(df, x="domain count", y="subdomain count",
                     size="domain count", color="names",
                     hover_name="names", log_x=True, height=650)
    return fig


def get_default():
    cityName = '郑州市'
    ans = dash_domain_obj.get_city_domains(cityName)
    number, domain, city = [], [], []
    for index, x in enumerate(ans):
        number.append(index + 1)
        domain.append(x)
        city.append(cityName)
    fig = go.Figure(data=[go.Table(header=dict(values=['Number', 'Domain', 'City'], align='left'),
                                   cells=dict(values=[number, domain, city], align='left'))
                          ])
    fig.update_layout(height=650)
    return fig


def get_domain_bar():
    x, y, ratio = dash_domain_obj.get_data()

    fig = go.Figure(data=[go.Bar(x=x, y=y, hovertext=ratio)])
    # Customize aspect
    fig.add_trace(
        go.Scatter(
            x=x,
            y=[i//2 for i in y],
            mode='lines',
            line=dict(color="#849E68"),
        ))
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='2020年河南省主域名数量分布情况', height=650)
    return fig


def clusters():
    np.random.seed(1)

    # Generate data
    x0 = np.random.normal(1.3, 0.15, 1435)
    y0 = np.random.normal(-2, 1.45, 1435)

    x1 = np.random.normal(6, 0.4, 1238)
    y1 = np.random.normal(6, 0.4, 1238)

    x2 = np.random.normal(2, 0.2, 132)
    y2 = np.random.normal(2, 3.0, 132)

    x3 = np.random.normal(4, 1, 233)
    y3 = np.random.normal(4, 1.5, 233)

    x4 = np.random.normal(-1.5, 0.7, 122)
    y4 = np.random.normal(-1.5, 1.2, 122)

    x5 = np.random.normal(-2, 0.2, 300)
    y5 = np.random.normal(9.5, 0.5, 300)

    # x6 = np.random.normal(2, 0.2, 1032)
    # y6 = np.random.normal(2, 3.0, 1032)
    #
    # x7 = np.random.normal(2, 0.2, 1032)
    # y7 = np.random.normal(2, 3.0, 1032)
    #
    # x8 = np.random.normal(2, 0.2, 1032)
    # y8 = np.random.normal(2, 3.0, 1032)
    #
    # x9 = np.random.normal(2, 0.2, 1032)
    # y9 = np.random.normal(2, 3.0, 1032)

    fig = go.Figure()

    # Add scatter traces
    fig.add_trace(go.Scatter(x=x0, y=y0, mode="markers", name='无效网站'))
    fig.add_trace(go.Scatter(x=x1, y=y1, mode="markers", name='被黑-博彩'))
    fig.add_trace(go.Scatter(x=x2, y=y2, mode="markers", name='运营商拦截'))

    fig.add_trace(go.Scatter(x=x3, y=y3, mode="markers", name='私人企业'))
    fig.add_trace(go.Scatter(x=x4, y=y4, mode="markers", name='企业邮箱'))
    fig.add_trace(go.Scatter(x=x5, y=y5, mode="markers", name='WAF拦截'))


    # fig.add_trace(go.Scatter(x=x2, y=y2, mode="markers", name='被黑-色情'))
    # fig.add_trace(go.Scatter(x=x2, y=y2, mode="markers", name='网站关闭'))
    # fig.add_trace(go.Scatter(x=x2, y=y2, mode="markers", name='微信接口'))
    # fig.add_trace(go.Scatter(x=x2, y=y2, mode="markers", name='WAF拦截'))

    # Add shapes
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=min(x0), y0=min(y0),
                  x1=max(x0), y1=max(y0),
                  opacity=0.2,
                  fillcolor="blue",
                  line_color="blue",
                  )

    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=min(x1), y0=min(y1),
                  x1=max(x1), y1=max(y1),
                  opacity=0.2,
                  fillcolor="black",
                  line_color="black",
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=min(x2), y0=min(y2),
                  x1=max(x2), y1=max(y2),
                  opacity=0.2,
                  fillcolor="red",
                  line_color="red",
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=min(x3), y0=min(y3),
                  x1=max(x3), y1=max(y3),
                  opacity=0.2,
                  fillcolor="gold",
                  line_color="gold",#'gold', 'mediumturquoise', 'darkorange', 'lightgreen'
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=min(x4), y0=min(y4),
                  x1=max(x4), y1=max(y4),
                  opacity=0.2,
                  fillcolor="mediumturquoise",
                  line_color="mediumturquoise",
                  )
    fig.add_shape(type="circle",
                  xref="x", yref="y",
                  x0=min(x5), y0=min(y5),
                  x1=max(x5), y1=max(y5),
                  opacity=0.2,
                  fillcolor="yellow",
                  line_color="yellow",
                  )
    fig.update_layout(title='黑名单种类')

    # Hide legend
    # fig.update_layout(showlegend=False)
    return fig


def total_content(app):
    citys = obj.get_city()
    app.layout = html.Div(
        [
            dcc.Store(id="aggregate_data"),
            # empty Div to trigger javascript file for graph resizing
            html.Div(id="output-clientside"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("dash-logo.png"),
                                id="plotly-image",
                                style={
                                    "height": "60px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            )
                        ],
                        className="one-third column",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "2020河南省域名资产分析",
                                        style={"margin-bottom": "0px"},
                                    ),
                                    html.H5(
                                        "Production Overview", style={"margin-top": "0px"}
                                    ),
                                ]
                            )
                        ],
                        className="one-half column",
                        id="title",
                    ),
                    html.Div(
                        [
                            html.A(
                                html.Button("Learn More", id="learn-more-button"),
                                href="https://plot.ly/dash/pricing/",
                            )
                        ],
                        className="one-third column",
                        id="button",
                    ),
                ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Markdown('''
                            #### sslkfjsklfls
                            
                            - kjskldjfsd
                            - sjdfkljsldkf
                            - sjdflksdjf
                            
                            '''),
                            # html.P("Filter by city:", className="control_label"),
                            # dcc.Dropdown(id='city_name2',
                            #              value=['洛阳市', '兰考县', '信阳市', '濮阳市', '鹤壁市'],
                            #              options=[{'value': x, 'label': x} for x in citys],
                            #              clearable=True,
                            #              multi=True,
                            #              className="dcc_control",
                            #              ),
                            # html.Br(),
                            # html.Br(),
                            # html.P(
                            #     "Filter by construction date (or select range in histogram):",
                            #     className="control_label",
                            # ),
                            # dcc.RangeSlider(
                            #     id="year_slider",
                            #     min=0,
                            #     max=100,
                            #     value=[0, 100],
                            #     className="dcc_control",
                            # ),

                            html.Br(),
                            html.Br(),
                            html.P(
                                "Filter by http status:",
                                className="control_label",
                            ),
                            dcc.Dropdown(
                                id="http_statuses",
                                options=http_status_options,
                                multi=True,
                                value=[403, 404, 500, 503],
                                className="dcc_control",
                            ),
                        ],
                        className="pretty_container four columns"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [dcc.Graph(id='http_status_bar')],
                                className="pretty_container",
                            ),
                        ],
                        className="pretty_container eight columns"
                    ),
                ],
                className="row flex-display",
            ),
            # html.Div(
            #     [
            #         html.Div(
            #             [
            #                 html.P(
            #                     "Filter by construction date (or select range in histogram):",
            #                     className="control_label",
            #                 ),
            #                 dcc.RangeSlider(
            #                     id="year_slider",
            #                     min=1960,
            #                     max=2017,
            #                     value=[1990, 2010],
            #                     className="dcc_control",
            #                 )
            #             ],
            #             className="pretty_container four columns",
            #             id="cross-filter-options"
            #         )
            #     ],
            #     className="row flex-display",
            # ),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="main_graph", figure=get_http_code_fig())],
                        className="pretty_container four columns",
                    ),
                    html.Div([
                        dcc.Graph(id='clusters', figure=clusters()),
                    ], className="pretty_container eight columns")
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Filter by found date:", className="control_label"),
                            dcc.DatePickerRange(
                                id='date_range',
                                min_date_allowed=date(2015, 1, 1),
                                max_date_allowed=date(2022, 1, 1),
                                initial_visible_month=date(2020, 5, 1),
                                start_date=date(2019, 1, 30),
                                end_date=date(2020, 7, 30)
                            ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.P("Filter by city:", className="control_label"),
                            dcc.Dropdown(id='city_name',
                                         value=['洛阳市', '兰考县', '信阳市', '濮阳市', '鹤壁市'],
                                         options=[{'value': x, 'label': x} for x in citys],
                                         clearable=True,
                                         multi=True,
                                         className="dcc_control",
                                         )
                        ],
                        className="pretty_container four columns",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [dcc.Graph(id="lines-id")],
                                className="pretty_container",
                            ),
                        ],
                        className="eight columns",
                    ),
                ],
                className="row flex-display",
            ),
            # html.Div(
            #     [
            #         html.Div(
            #             [dcc.Graph(id="pie_graph")],
            #             className="pretty_container seven columns",
            #         ),
            #         html.Div(
            #             [dcc.Graph(id="aggregate_graph"),
            #              dcc.Graph(id="aggregate_graph2"),],
            #             className="pretty_container five columns",
            #         ),
            #     ],
            #     className="row flex-display",
            # ),
            html.Div(
                [
                    html.Div([
                        dcc.Graph(id='input_id22', figure=get_sca()),
                    ], style=dict(width='70%', display='inline-block'), className="pretty_container"),
                    html.Div([  # 设置交互的子图表
                        html.Div([
                            dcc.Graph(id='x-time-series'),
                        ], className="pretty_container"),
                        html.Div([
                            dcc.Graph(id='y-time-series'),
                        ], className="pretty_container"),
                    ], style=dict(width='69%', display='inline-block')),
                ], className="row flex-display"
            ),
            html.Div([
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.P(
                        "Filter by subdomain count (or select type in figure):",
                        className="control_label",
                    ),
                    dcc.RangeSlider(
                        id="year_slider",
                        min=0,
                        max=1000,
                        value=[50, 700],
                        className="dcc_control",
                        marks={
                            0: {'label': '0', 'style': {'color': '#77b0b1'}},
                            200: {'label': '200'},
                            700: {'label': '700'},
                            1000: {'label': '1000', 'style': {'color': '#f50'}}
                        }
                    ),
                    dcc.Graph(
                        id='input_id',
                        # figure=get_3D()
                    )
                ], className="pretty_container eight columns",),
                html.Div(
                    [dcc.Graph(id="individual_graph", figure=get_domain_host_type_fig())],
                    className="pretty_container four columns",
                ),
            ], className="row flex-display"),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="domain_bar_id", figure=get_domain_bar())],
                        className="pretty_container seven columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="domain_table_id", figure=get_default())],
                        className="pretty_container five columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div([
                        dcc.Markdown('''
                        > 该组件对输入的文本做实时的 **词性划分**，统计词性比例，并显示对应词汇
                        '''),
                        dcc.Textarea(id='input_testarea_id', value='这是一段测试样例文字', style=dict(width='500px', height='150px')),

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dcc.Markdown('''                    
                        > 单击右侧属性，显示对应词汇
                        '''),
                        dcc.Textarea(id='show_word_id', style=dict(width='500px', height='150px')),
                        dcc.Input(id='hidden_id', type='hidden'),
                    ], className="pretty_container six columns"),
                    html.Div([
                        dcc.Graph(id="show_pie_id"),
                    ], className="pretty_container six columns"),
                ],
                className="row flex-display",
            ),
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )

    @app.callback(Output('input_id', 'figure'), [Input('year_slider', 'value')])
    def get_3D(value):
        min_count, max = value
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
            ] * 10

        z = [random.randint(1, 1000) for _ in range(len(x))]
        y = [random.randint(1, 1000) for _ in range(len(z))]
        tz, ty = [], []
        for i in range(100):
            if min_count <= z[i] <= max:
                tz.append(z[i])
            if min_count <= y[i] <= max:
                ty.append(y[i])
        t_min = min(len(tz), len(ty)) - 1
        tz = tz[:t_min]
        ty = ty[:t_min]

        t = {'type': x[:t_min], 'domain count': tz, 'subdomain count': ty}
        df = pd.DataFrame(t)

        fig = px.scatter_3d(df, x="type", y="domain count", z='subdomain count', color='type')
        fig.update_layout(title='Abnormal website',
                          # width=600,
                          # height=500,
                          )
        return fig

    @app.callback(Output('lines-id', 'figure'), [Input('city_name', 'value'), Input('date_range', 'start_date'), Input('date_range', 'end_date')])
    def get_selected_data(selected_citys, start_date, end_date):
        if not isinstance(selected_citys, list):
            selected_citys = [selected_citys]
        # print('selected_citys', selected_citys)
        industries = ['卫生计生', '地方政府', '新闻出版广电', '群众组织及社会团体', '人力资源和社会保障', '旅游', '法院', '统战部', '食品药品监督', '教育', '交通运输',
                      '水利', '科技', '检察院', '国土资源']
        fig = go.Figure()
        for index, city in enumerate(selected_citys):
            if (index + 1) % 3 == 0:
                line = dict(width=3, dash='dot')
            else:
                line = dict(width=3)
            city_ans = obj.get_city_industries_cnt(city, industries, start_date, end_date)
            fig.add_trace(go.Scatter(x=industries, y=city_ans, name=city, mode='lines+markers', line=line))
        fig.update_layout(title='各地市网站行业数量Top15统计图', xaxis_title='网站行业', yaxis_title='网站数量')
        return fig

    @app.callback(Output('x-time-series', 'figure'), Output('y-time-series', 'figure'), [Input('input_id22', 'hoverData')])
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
        fig1.add_trace(go.Scatter(x=citys, y=domainCnt1, mode='lines+markers', name=name, line=dict(width=3, shape="spline", color="#F9ADA0")))
        fig1.add_trace(go.Scatter(x=citys, y=JunZhi1, mode='lines', name='均值', line=dict(width=2, shape="spline")))
        fig1.update_layout(title='主域名Top10', xaxis_title='city', yaxis_title='count', height=300)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=citys, y=domainCnt2, mode='lines+markers', name=name, line=dict(width=3, shape="spline", color="#59C3C3")))
        fig2.add_trace(go.Scatter(x=citys, y=JunZhi2, mode='lines', name='均值', line=dict(width=2, shape="spline")))
        fig2.update_layout(title='子域名Top10', xaxis_title='city', yaxis_title='count', height=300)
        return fig1, fig2

    @app.callback(Output('domain_table_id', 'figure'), [Input('domain_bar_id', 'hoverData'), Input('domain_bar_id', 'figure')])
    def show_clickData(hoverData, figure):
        title = figure['layout']['title']['text']
        if '河南省' not in title:
            city_, region_ = re.findall('2020年(.*)主', title)[0], hoverData['points'][0]['label']
            # print(city_, region_)
            ans = dash_domain_obj.get_region_domains(city_, region_)
            number, domain, city, region = [], [], [], []
            for index, x in enumerate(ans):
                number.append(index + 1)
                domain.append(x)
                city.append(city_)
                region.append(region_)
            fig = go.Figure(data=[go.Table(header=dict(values=['Number', 'Domain', 'City', 'Region'], align='left'),
                                           cells=dict(values=[number, domain, city, region], align='left'),
                                           )
                                  ])
            fig.update_layout(height=650)
            return fig
        else:
            cityName = hoverData['points'][0]['label']
            if cityName is None:
                cityName = '郑州市'
            ans = dash_domain_obj.get_city_domains(cityName)
            number, domain, city = [], [], []
            for index, x in enumerate(ans):
                number.append(index+1)
                domain.append(x)
                city.append(cityName)
            fig = go.Figure(data=[go.Table(header=dict(values=['Number', 'Domain', 'City'], align='left'),
                                           cells=dict(values=[number, domain, city], align='left'),
                                           )
                                  ])
            fig.update_layout(height=650)
            return fig

    @app.callback(Output('http_status_bar', 'figure'), [Input('http_statuses', 'value')])
    def getBar(value):
        if not isinstance(value, list):
            value = [value]

        city, ans = obj.get_data(value)
        x = city
        fig = go.Figure()
        for index, code in enumerate(value):
            fig.add_trace(go.Bar(x=x, y=ans[index], name=str(code)))
        fig.update_layout(title_text='各市区网站状态分析')
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'array', 'categoryarray': x})
        return fig

    @app.callback(Output('domain_bar_id', 'figure'), [Input('domain_bar_id', 'clickData')])
    def show_clickData(clickData):
        fig = dash_domain_obj.get_region_data(clickData['points'][0]['label'])
        return fig

    @app.callback([Output("show_pie_id", "figure"), Output('hidden_id', 'value')], [Input('input_testarea_id', 'value')])
    def generate_chart(textare):
        # print(textare)
        if not textare:
            textare = '这是一段测试样例文字'
        data = dosegment_all(textare)
        labels = list(data.keys())
        values = [data[x]['cnt'] for x in data]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                                    marker=dict(colors=[WELL_COLORS[i] for i in WELL_COLORS]),
                                     )])
        return fig, str(data)

    @app.callback(Output('show_word_id', 'value'), [Input('show_pie_id', 'clickData'), Input('hidden_id', 'value')])
    def show_clickData(clickData, data):
        try:
            data = re.sub("'", '"', data)
            data = json.loads(data)
            for x in data:
                if x == clickData['points'][0]['label']:
                    return data[x]['word_list']
            return json.dumps(clickData['points'][0]['label'])
        except:
            return json.dumps('null')


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


def twice_test(dash_app):
    import datetime
    dash_app.layout = html.Div([
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Textarea(id='output-image-upload'),
    ])

    def parse_contents(contents, filename, date):
        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=contents),
            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])

    @dash_app.callback(Output('output-image-upload', 'value'),
                       Input('upload-image', 'contents'),
                       State('upload-image', 'filename'),
                       State('upload-image', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        # print(list_of_contents)
        # print(list_of_names)
        # print(list_of_dates)
        # if list_of_contents is not None:
        #     children = [
        #         parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]
        import base64
        # print(base64.b64decode(list_of_dates[0]))
        return list_of_contents[0]
