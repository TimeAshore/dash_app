import re
import dash_table
# from showimg import dash_app3
import jieba
import jieba.analyse
import jieba.posseg
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go


from ..models import DomainArchived
from sqlalchemy.sql.functions import count
from sqlalchemy import asc, desc, and_


from .base import BaseBiz
from ..models import DomainArchived


class DashDomainCityBiz(BaseBiz):

    def __init__(self):
        super(DashDomainCityBiz, self).__init__()
        self.model = DomainArchived
        self.allow_query_all = True

    def get_data(self):
        a = self.session.query(DomainArchived.city_code, count(DomainArchived.city_code).label('city_count'))\
            .group_by(DomainArchived.city_code).order_by(desc('city_count')).all()
        # print(a)
        x = []
        y = []
        for i in a[:20]:
            if i[0]:
                x.append(i[0])
                y.append(i[1])

        ratio = []
        total = sum(y)
        for i in y:
            ratio.append(f'RATIO: {round(i/total, 4)*100}%')
        return x, y, ratio

    def get_city_domains(self, city):
        result = self.session.query(DomainArchived.name).filter_by(city_code=city).all()
        return [x[0] for x in result]

    def get_region_domains(self, city, region):
        result = self.session.query(DomainArchived.name).filter(and_(DomainArchived.city_code==city, DomainArchived.region_code==region)).all()
        return [x[0] for x in result]

    def get_region_data(self, city):
        a = self.session.query(DomainArchived.region_code, count(DomainArchived.region_code).label('region_count')) \
            .filter_by(city_code=city).group_by(DomainArchived.region_code).order_by(desc('region_count')).all()
        # print(a)
        x, y = [], []
        for i in a[:20]:
            if i[0]:
                x.append(i[0])
                y.append(i[1])

        ratio = []
        total = sum(y)
        for i in y:
            ratio.append(f'RATIO: {round(i / total, 4) * 100}%')

        fig = go.Figure(data=[go.Bar(x=x, y=y, hovertext=ratio)])
        # Customize aspect
        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5,
                          opacity=0.6)
        fig.update_layout(title_text=f'2020年{city}主域名分布情况')
        return fig

    def _build_query_filter(self, query, condition, strict=False):
        if condition.get('domain_name'):
            query = query.filter(self.model.name.ilike(condition['domain_name'] + '%'))
        if condition.get('city'):
            query = query.filter(self.model.city_code == condition['city'])
        if condition.get('domain_sponsor'):
            query = query.filter(self.model.sponsor.like('%' + condition['domain_sponsor'] + '%'))
        if condition.get('sponsor_type'):
            query = query.filter(self.model.sponsor_type == condition['sponsor_type'])
        if condition.get('start_date'):
            query = query.filter(and_(self.model.create_time > condition['start_date'], self.model.create_time < condition['end_date']))
        if condition.get('only_icp') is True:
            query = query.filter(self.model.sponsor.notin_(['未备案', '']))
        if 'only_national_level' in condition:
            query = query.filter(self.model.national_level.is_(condition['only_national_level']))
        return query

    def query_table_data(self, domain_name, city, domain_sponsor, sponsor_type, start_date, end_date):
        payload = {
            'filter': { 
                'domain_name': domain_name,
                'city': city,
                'domain_sponsor': domain_sponsor,
                'sponsor_type': sponsor_type,
                'start_date': start_date,
                'end_date': end_date,
            }
        }
        query = self.session.query(self.model)
        result = self.base_query(query, **payload)
        return result


obj = DashDomainCityBiz()


def domain_city_add_content(dash_app):
    def get_default():
        cityName = '郑州市'
        ans = obj.get_city_domains(cityName)
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

    x, y, ratio = obj.get_data()

    fig = go.Figure(data=[go.Bar(x=x, y=y, hovertext=ratio)])
    # Customize aspect
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='2020年河南省主域名数量分布情况', height=650)

    dash_app.layout = html.Div([
        html.Div([
            dcc.Graph(
                id='input_id',
                figure=fig
            )
        ], style=dict(width='60%', display='inline-block')),
        # html.Div([
        #     html.Textarea(id='show_id', placeholder='data display',
        #                   style=dict(height='500px', backgroundColor='#fffbf8'))
        # ], style=dict(width='20%', display='inline-block')),
        html.Div([
            dcc.Graph(
                id='show_id',
                figure=get_default()
            )
        ], style=dict(width='40%', display='inline-block')),
    ], style=dict(width='70%', display='inline-block'))

    @dash_app.callback(Output('show_id', 'figure'), [Input('input_id', 'hoverData'), Input('input_id', 'figure')])
    def show_clickData(hoverData, figure):
        title = figure['layout']['title']['text']
        if '河南省' not in title:
            city_, region_ = re.findall('2020年(.*)主', title)[0], hoverData['points'][0]['label']
            # print(city_, region_)
            ans = obj.get_region_domains(city_, region_)
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
            ans = obj.get_city_domains(cityName)
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

    @dash_app.callback(Output('input_id', 'figure'), [Input('input_id', 'clickData')])
    def show_clickData(clickData):
        fig = obj.get_region_data(clickData['points'][0]['label'])
        return fig
