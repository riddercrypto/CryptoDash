import os
import datetime as dt
import time
import flask

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.plotly as pp
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import psycopg2 as psyc
import sqlalchemy
from sqlalchemy import create_engine


server = flask.Flask(__name__)
app = dash.Dash(__name__, sharing=True, server=server, csrf_protect=False)

engine = create_engine('postgresql+psycopg2://crypto:knight@localhost:5432/crypto')

###  Get df for graph x & y  ###
df = pd.read_sql_table('knights', engine, columns=['name'])
df['deposit_net'] = pd.read_sql_table('deposits', engine, columns=['deposit_net'])
df['factor'] = pd.read_sql_table('deposits', engine, columns=['deposit_factor'])

knight_total_usd = []
for k in df['name']:
	dk = pd.read_sql_table(k, engine).tail(1)
	dktu = float(dk.total_usd)
	knight_total_usd.append(dktu)

df['total_usd'] = knight_total_usd
df['score'] = df.total_usd / df.factor
df['score'] = df.score.fillna(0.0).astype(int)
###

colors = {
	'background': '#3F3F3F',
	'text': '#ececec'
}

app.layout = html.Div(
	style={
		'font-family': 'sans-serif',
		'backgroundColor': colors['background'],
	},
	children=[
		html.Img(src="static/logo-600x315.png",
			style={
			'float': 'left',
			'height': '80px',
			'position': 'relative',
			}
		),

		html.H1(children='Holy Crypto Challenge',
			style={
				'textAlign': 'center',
				'color': colors['text'],
			}
		),


		html.Div(
			[
				html.Div(
					[
						dcc.Graph(
							id='score-graph',
							figure={
								'data': [
									{'x': df.name, 'y': df.score, 'type': 'bar', 'name': u'Score'},
								],
								'layout': {
									'title': 'Score = Total_usd / Deposit * 100',
									'plot_bgcolor': colors['background'],
									'paper_bgcolor': colors['background'],
									'font': {'color': colors['text']},
									'width': '40%',
								}
							}
						)
					]
				),

				html.Div(
					[
						dcc.Graph(
							id='usd-graph',
							figure={
								'data': [
									{'x': df.name, 'y': df.total_usd, 'type': 'bar', 'name': 'Current Total_usd'},
									{'x': df.name, 'y': df.deposit_net, 'type': 'bar', 'name': 'Netto Deposit_usd'},
								],
								'layout': {
									'plot_bgcolor': colors['background'],
									'paper_bgcolor': colors['background'],
									'font': {'color': colors['text']},
									'width': '40%',
									'legend': {'x': 0.95, 'y': 1.2},
								}
							}
						)
					]
				)
			]
		)

	]
)


if __name__ == '__main__':
	app.run_server(debug=True, host='0.0.0.0')
