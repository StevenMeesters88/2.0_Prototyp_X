import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_prototype_data():
    portfolio = {'YEAR': ['2019', '2019', '2019', '2019', '2019', '2019',
                          '2020', '2020', '2020', '2020', '2020', '2020',
                          '2021', '2021', '2021', '2021', '2021', '2021',
                          '2022', '2022', '2022', '2022', '2022', '2022'],
                 'PRODUCT': ['FRITID', 'DIREKT/LEV', 'MASKINFINANS', 'PARTNER FÖRETAG', 'BIL', 'BILKUND'] * 4,
                 'VIKT_PD': [0.2, 0.3, 0.1, 0.2, 0.13, 0.07,
                             0.22, 0.33, 0.11, 0.22, 0.143, 0.077,
                             0.1235, 0.0665, 0.209, 0.3135, 0.1045, 0.209,
                             0.11115, 0.05985, 0.1881, 0.28215, 0.09405, 0.1881],
                 'VIKT_LGD': [0.4, 0.5, 0.2, 0.4, 0.4, 0.2,
                              0.4, 0.5, 0.2, 0.4, 0.4, 0.2,
                              0.4, 0.5, 0.2, 0.4, 0.4, 0.2,
                              0.4, 0.5, 0.2, 0.4, 0.4, 0.2],
                 'Exponering': [3000000000, 2000000000, 8000000000, 4000000000, 3000000000, 2000000000,
                                3300000000, 2200000000, 8800000000, 4400000000, 3300000000, 2200000000,
                                3069000000, 2046000000, 8184000000, 4092000000, 3069000000, 2046000000,
                                3696000000, 2464000000, 9856000000, 4928000000, 3696000000, 2464000000]}
    df_portfolio = pd.DataFrame(portfolio)
    return df_portfolio


df_ = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="Portfolio", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_portf",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_portf', children=[]),
    html.Br(),

    dcc.Graph(id='portf_bar_main', figure={}),
    html.Br(),

    dcc.Graph(id='portf_bar_prod', figure={}),
    html.Br(),

    dcc.Graph(id='portf_pie_prod', figure={}),
    html.Br()

    ]),


@callback(
    [Output(component_id='output_container_portf', component_property='children'),
     Output(component_id='portf_bar_main', component_property='figure'),
     Output(component_id='portf_bar_prod', component_property='figure'),
     Output(component_id='portf_pie_prod', component_property='figure')],
    [Input(component_id='slct_year_portf', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = df_.copy()
    x2 = x.groupby('YEAR').sum()
    x2 = x2.reset_index()
    p_bar = px.bar(data_frame=x2, x='YEAR', y='Exponering', title='Utveckling balans i kronor')
    p_bar_prod = px.bar(data_frame=x, x='YEAR', y='Exponering', color='PRODUCT', title='Utveckling balans per produkt i kronor')

    pie_df = df_.copy()
    pie_df = pie_df[pie_df['YEAR'] == option_slctd]
    p_pie_year = px.pie(data_frame=pie_df, names='PRODUCT', values='Exponering', title=f'Portfölj per {option_slctd}')

    return container, p_bar, p_bar_prod, p_pie_year
