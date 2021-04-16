import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from flask import session
from package.utility import dash_kwarg
from typing import Dict
from package.login_manager import login_manager

dashboard_app = dash.Dash(__name__, requests_pathname_prefix="/dashboard/")

dashboard_app.layout = html.Div(
    children=[
        dcc.Store(id="session"),
        "Dash app 1",
        html.H1(id="test1", children=[]),
        html.Button(id="test2", n_clicks=0),
    ]
)


@dashboard_app.callback(Output("test1", "children"), Input("test2", "n_clicks"))
def test(n_clicks):
    print(n_clicks)
    print(login_manager.session)

    return ["OK"]
