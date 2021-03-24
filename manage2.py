# services/socamas/manage.py
# import pytest
from flask.cli import FlaskGroup

from project import create_app
from project.api.models import db
from flask_migrate import Migrate
from flask_script import Manager
from project.api.bizs.dash_biz import dash1_add_content, dtest
from project.api.bizs.dash_domain_city import domain_city_add_content
from project.api.bizs.total_biz import total_content
from project.api.bizs.dash_subdomain_biz import subdomain_dashboard_add_content, add_test, twice_test

import dash
import dash_table
# from showimg import dash_app3
import dash_core_components as dcc
import dash_html_components as html
from flask import render_template, redirect, Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware


app = create_app()
app.app_context().push()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# ========================== dash服务 ===========================================================
dash_app1 = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/index/')
dash_app2 = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/domain/')
dash_app3 = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/subdomain/')
dash_test = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/test/')
dash_test2 = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/test2/', external_stylesheets=external_stylesheets)
dash_test3 = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/total/')
dtest(dash_app1)
domain_city_add_content(dash_app2)
subdomain_dashboard_add_content(dash_app3)
add_test(dash_test)
twice_test(dash_test2)

total_content(dash_test3)
# =========================================================================================================


# @app.route('/')
# def hello():
#     return redirect('/dash_app')


# @app.route('/dash_app')
# def test_a():
#     return render_template('1.html')


# migrate = Migrate(app, Base)
# manager = Manager(app)


# @manager.command
# def runserver():
#     app.run(debug=True, host=os.getenv('HOST'), port=os.getenv('PORT'), threaded=True)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
