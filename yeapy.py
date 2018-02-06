import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()


app.layout = html.Div(children=[
    html.H1(children='CryptoKnight Challenge 2018'),
    
    html.Div(children='''
        Crown yourself the CryptoKing of 2018
    '''),


dcc.Dropdown(
    options=[
        {'label': 'King Thur', 'value': 'King Thur'},
        {'label': 'Sir KnightVision', 'value': 'Sir KnightVision'},
        {'label': 'Sir Buddha', 'value': 'Sir Buddha'},
        {'label': 'Sir Rise and Shine', 'value': 'Sir Rise and Shine'},
        {'label': 'Sir Braveheart', 'value': 'Sir Braveheart'},
        {'label': 'Sir Attitude', 'value': 'Sir Attitude'},
        {'label': 'Sir Blackbetty', 'value': 'Sir Blackbetty'},
        {'label': 'Sir Lucky Nr. 13', 'value': 'Sir Lucky Nr. 13'},
        {'label': 'Sir Rocco the Ripper', 'value': 'Sir Rocco the Ripper'},
        {'label': 'Sir Rascal', 'value': 'Sir Rascal'}
    ],
    value='MTL'
)

])

if __name__ == '__main__':
    app.run_server(debug=True)