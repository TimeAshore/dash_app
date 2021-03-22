from flask import Blueprint, jsonify
import dash
import dash_table
# from showimg import dash_app3
import dash_core_components as dcc
import dash_html_components as html
from flask import render_template, redirect, Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from project.api.bizs import CityBiz

bala_blueprint = Blueprint('bala', __name__)
payload_location = ('json',)


@bala_blueprint.route('/dash_app/page1', methods=['GET'])
def obtain_page1():
    print('dash')
    # # ========================== dash服务 ===========================================================
    # from manage2 import app
    # dash_app1 = dash.Dash(__name__, server=app)
    # # dash_app1 = dash.Dash(__name__, server=app, url_base_pathname='/dash_app')
    # markdown_text = '''
    #        # yiji
    #        ## erji
    #        ### sanji
    #        #### siji
    #
    #        ```
    #        import os
    #        print(os.getcwd())
    #        ```
    #
    #        > sjdkf
    #
    #        **jdfklsjf**
    #
    #        sdjklfjsf
    #
    #         ---
    #         '''
    #
    # dash_app1.layout = html.Div([
    #     # dcc.Markdown(children=markdown_text),
    #     html.Div(dcc.Markdown(children=markdown_text), style={'backgroundColor': '#fffbf8'}),
    #     html.Div(html.Img(src='图片链接', height=600, width=900))
    # ])
    #
    # return dash_app1