from dash_html_components.Output import Output
from dash.dependencies import Input, Output
from pandas.core.tools.numeric import to_numeric
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np



fundamentals = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo")
fundamentals_dict = fundamentals.json()

daily = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo")
daily_dict = daily.json()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'text': '#7FDBFF',
    'background': '#111111',
}

#cleaning and transforming data
daily_prices = pd.DataFrame.from_dict(daily_dict['Time Series (Daily)']).T
daily_volume = daily_prices['5. volume'].apply(to_numeric)

daily_prices.drop(['5. volume'],axis=1,inplace=True)
daily_prices.reset_index(inplace=True)
daily_prices = daily_prices.rename(columns={'index':'date','1. open':'open','2. high':'high','3. low':'low','4. close':'close'})
daily_prices[['open','high','low','close']] = daily_prices[['open','high','low','close']].apply(pd.to_numeric)

#plotinging data
fig = px.line(daily_prices,x=daily_prices['date'],y = daily_prices['high'],
              title = 'Daily high: ' + fundamentals_dict['Symbol'])
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")



app.layout = html.Div(children=[
dcc.Tabs(id='Company-metrics', value='tab-1', children=[
    dcc.Tab(label='Overview', value='tab-1'),
    dcc.Tab(label='Fundamentals', value='tab-2'),
]),
html.Div(id='Company-metrics-content')
])

@app.callback(Output('Company-metrics-content','children'),
              Input('Company-metrics','value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            
            html.H1(children=fundamentals_dict['Name'],
            style={
                'textAlign': 'center',
                
            }
            ),

            html.Div(children=fundamentals_dict['Description'], style={
        'textAlign': 'left',
        'paddingLeft': '3em',
        'paddingTop': '5em',
        'paddingRight': '3em'
    }),
            html.Div([
            html.Div([
                html.Table([
                    html.Tbody([
                        html.Tr([
                         html.Td(['Previous close']),
                         html.Td([daily_prices.iloc[4,2]])   
                        ]),
                        html.Tr([
                         html.Td(['Open']),
                         html.Td([daily_prices.iloc[1,1]])
                        ]),
                        html.Tr([
                            html.Td(['Volume']),
                            html.Td([daily_volume[0]])
                        ]),
                        html.Tr([
                            html.Td(['Avg. Volume']),
                            html.Td([np.mean(daily_volume).round()])
                        ]),
                        
                    ],style={})
                    ],style={})
            ],style={}),
            html.Div([
                html.Table([
                    html.Tbody([
                        html.Tr([
                         html.Td(['Market Cap']),
                         html.Td([f"{float(fundamentals_dict['MarketCapitalization'])/1000000:.2f} M"])   
                        ]),
                        html.Tr([
                         html.Td(['PE Ratio']),
                         html.Td([fundamentals_dict['PERatio']])
                        ]),
                        html.Tr([
                            html.Td(['Book Value']),
                            html.Td([fundamentals_dict['BookValue']])
                        ]),
                        html.Tr([
                            html.Td(['EPS']),
                            html.Td([fundamentals_dict['EPS']])
                        ]),
                        
                    ],style={})
                    ],style={})
            ],style={
                'paddingLeft':'4em'}),
            html.Div([
                html.Table([
                    html.Tbody([
                        html.Tr([
                         html.Td(['Analyst Target Price']),
                         html.Td([fundamentals_dict['AnalystTargetPrice']])   
                        ]),
                        html.Tr([
                         html.Td(['QuarterlyEarningsYOY']),
                         html.Td([fundamentals_dict['QuarterlyEarningsGrowthYOY']])
                        ]),
                        html.Tr([
                            html.Td(['QuarterlyRevenueYOY']),
                            html.Td([fundamentals_dict['QuarterlyRevenueGrowthYOY']])
                        ]),
                        html.Tr([
                            html.Td(['Institution held %']),
                            html.Td([fundamentals_dict['PercentInstitutions']])
                        ]),
                        
                    ],style={})
                    ],style={})
            ],style={
                'paddingLeft':'4em'}),html.Div([
                html.Table([
                    html.Tbody([
                        html.Tr([
                         html.Td(['Dividend per share']),
                         html.Td([fundamentals_dict['DividendPerShare']])   
                        ]),
                        html.Tr([
                         html.Td(['Dividend date']),
                         html.Td([fundamentals_dict['DividendDate']])
                        ]),
                        html.Tr([
                            html.Td(['Expected dividend date']),
                            html.Td([fundamentals_dict['ExDividendDate']])
                        ]),
                        html.Tr([
                            html.Td(['Fiscal year end']),
                            html.Td([fundamentals_dict['FiscalYearEnd']])
                        ]),
                        
                    ],style={})
                    ],style={})
            ],style={
                'paddingLeft':'4em'})
            ],style={
                'paddingLeft':'6em',
               'display':'flex',
               'flex-direction':'row',
               'justify-conetent':'flex-end'}),
            dcc.Graph(
        id="Demo-IBM",
        figure=fig
    )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Company fundamentals')
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
