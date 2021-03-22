import re
import dash
import dash_table
# from showimg import dash_app3
import dash_core_components as dcc
import dash_html_components as html
from flask import render_template, redirect, Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

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


def dash1_add_content(dash_app1):
    markdown_text = '''
           # yiji
           ## erji
           ### sanji
           #### siji

           ```
           import os
           print(os.getcwd())
           ```

           > sjdkf

           **jdfklsjf**

           sdjklfjsf

            ---
            '''

    dash_app1.layout = html.Div([
        # dcc.Markdown(children=markdown_text),
        html.Div(dcc.Markdown(children=markdown_text), style={'backgroundColor': '#fffbf8'}),
        html.Div(html.Img(src='图片链接', height=600, width=900)),
    ])


def dtest(app):
    app.layout = html.Div([
        html.Div([
            dcc.Textarea(id='input_id', value='这是一段测试样例文字', style=dict(width='500px', height='150px')),
            dcc.Textarea(id='show_id', style=dict(width='400px', height='150px')),
            dcc.Input(id='hidden_id', type='hidden'),
        ]),
        html.Div([
            html.Div([
                html.Div(
                    [html.P("Names:"),
                     dcc.Dropdown(id='names', value='day',
                                  options=[{'value': x, 'label': x} for x in ['smoker', 'day', 'time', 'sex']],
                                  clearable=False)
                     ], style=dict(width='30%', display='inline-block', padding='0px 0px 0px 150px')
                ),
                html.Div(
                    [html.P("Values:"),
                     dcc.Dropdown(id='values', value='total_bill',
                                  options=[{'value': x, 'label': x} for x in ['total_bill', 'tip', 'size']],
                                  clearable=False)
                     ], style=dict(width='30%', display='inline-block', padding='0px 20px')
                )
            ]),
            html.Div([
                dcc.Graph(id="pie-chart"),
            ]),
        ], style=dict(width='49%', display='inline-block', padding='10px 0px')),
        html.Div([
            html.Div([
                html.Div(
                    [html.P("Names:"),
                     dcc.Dropdown(id='city', value='郑州',
                                  options=[{'label': x, 'value': x} for x in ['郑州', '南阳', '安阳', '新乡']],
                                  clearable=False)
                     ], style=dict(width='30%', display='inline-block', padding='0px 0px 0px 150px')
                ),
                html.Div(
                    [html.P("Values:"),
                     dcc.Dropdown(id='http_code', value='200',
                                  options=[{'label': x, 'value': x} for x in ['200', '403', '500', '404']],
                                  clearable=False)
                     ], style=dict(width='30%', display='inline-block', padding='0px 20px')
                )
            ]),
            html.Div([
                dcc.Graph(id="pie-city-httpcode"),
            ]),
        ], style=dict(width='49%', display='inline-block', padding='10px 0px')),
    ], style={'backgroundColor': '#fffbf8'})

    @app.callback([Output("pie-city-httpcode", "figure"), Output("pie-chart", "figure"), Output('hidden_id', 'value')],
                  [Input("city", "value"), Input("http_code", "value"), Input('input_id', 'value')])
    def generate_chart(city, http_code, textare):
        labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
        values = [4500, 2500, 1053, 500]
        print(textare)
        if not textare:
            textare = '这是一段测试样例文字'
        data = dosegment_all(textare)
        labels = list(data.keys())
        values = [data[x]['cnt'] for x in data]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        return fig, fig, str(data)

    @app.callback(Output('show_id', 'value'), [Input('pie-city-httpcode', 'clickData'), Input('hidden_id', 'value')])
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


flag_en2cn = {
    'a': '形容词', 'ad': '副形词', 'ag': '形语素', 'an': '名形词', 'b': '区别词',
    'c': '连词', 'd': '副词', 'df': '不要', 'dg': '副语素',
    'e': '叹词', 'f': '方位词', 'g': '语素', 'h': '前接成分',
    'i': '成语', 'j': '简称略语', 'k': '后接成分', 'l': '习用语',
    'm': '数词', 'mg': '数语素', 'mq': '数量词',
    'n': '名词', 'ng': '名语素', 'nr': '人名', 'nrfg': '古代人名', 'nrt': '音译人名',
    'ns': '地名', 'nt': '机构团体', 'nz': '其他专名',
    'o': '拟声词', 'p': '介词', 'q': '量词',
    'r': '代词', 'rg': '代语素', 'rr': '代词', 'rz': '代词',
    's': '处所词', 't': '时间词', 'tg': '时间语素',
    'u': '助词', 'ud': '得', 'ug': '过', 'uj': '的', 'ul': '了', 'uv': '地', 'uz': '着',
    'v': '动词', 'vd': '副动词', 'vg': '动语素', 'vi': '动词', 'vn': '名动词', 'vq': '动词',
    'x': '非语素字', 'y': '语气词', 'z': '状态词', 'zg': '状态语素',
}


def dosegment_all(sentence):
    '''
    带词性标注，对句子进行分词，不排除停词等
    :param sentence:输入字符
    :return:
    '''
    ans = {}
    sentence_seged = jieba.posseg.cut(sentence.strip())

    for x in sentence_seged:
        if x.word not in [' ']:
            try:
                cha_means = flag_en2cn[x.flag]
            except:
                continue
            x.flag = cha_means
            if x.flag not in ans:
                ans.update({x.flag: {'cnt': 1, 'word_list': [x.word]}})
            else:
                ans[x.flag]['cnt'] += 1
                ans[x.flag]['word_list'].append(x.word)
    return ans

