import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_prototype_data():
    ecl = {'YEAR': ['2019', '2019', '2019', '2019', '2019', '2019',
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
           'ECLFINAL': [2000, 3000, 1000, 3999, 2888, 2635,
                        3761, 2899, 2633, 7762, 2880, 3654,
                        2991, 6527, 4567, 2863, 2735, 2891,
                        2863, 2877, 4556, 8726, 2773, 2774],
           'BALANCEAMOUNT': [1000000, 2666181, 3667181, 1882999, 2766341, 3997363,
                             1100000, 2932799, 4033899, 2071299, 3042975, 4397099,
                             1210000, 1034000, 2756831, 3791865, 1947021, 2860397,
                             1130000, 3012785, 4143915, 2127789, 3125965, 4517020]

           }
    df_ecl = pd.DataFrame(ecl)
    df_ecl['EL'] = df_ecl['VIKT_PD'] * df_ecl['VIKT_LGD']
    df_ecl['REA'] = df_ecl['VIKT_PD'] * df_ecl['VIKT_LGD'] * df_ecl['BALANCEAMOUNT']
    return df_ecl


df_ = create_prototype_data()

dash.register_page(__name__)


layout = html.Div([

    html.H1(children="Kapitaltäckning", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_capReq",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_capReq', children=[]),
    html.Br(),

    dcc.Graph(id='capReq_pd_lgd', figure={}),
    html.Br(),

    dcc.Graph(id='capReq_reaMain', figure={}),
    html.Br(),

    dcc.Graph(id='capReq_reaProd', figure={}),
    html.Br(),

    dcc.Graph(id='capReq_reaPie', figure={})
    ]),


@callback(
    [Output(component_id='output_container_capReq', component_property='children'),
     Output(component_id='capReq_pd_lgd', component_property='figure'),
     Output(component_id='capReq_reaMain', component_property='figure'),
     Output(component_id='capReq_reaProd', component_property='figure'),
     Output(component_id='capReq_reaPie', component_property='figure')],
    [Input(component_id='slct_year_capReq', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    y = df_.copy()
    x = y.groupby('YEAR').mean()
    x = x.reset_index()
    pd_lgd = make_subplots(specs=[[{"secondary_y": True}]])
    pd_lgd.add_trace(
        go.Line(x=x['YEAR'], y=x['VIKT_PD'], name="Viktat PD"),
        secondary_y=False,
    )
    pd_lgd.add_trace(
        go.Line(x=x['YEAR'], y=x['VIKT_LGD'], name="Viktat LGD"),
        secondary_y=True,
    )
    pd_lgd.update_layout(
        title_text="Kapitaltäckning: Viktat PD och LGD"
    )

    rea = df_.copy()

    rea_gr = rea[['YEAR', 'REA']].groupby('YEAR').sum()
    rea_gr = rea_gr.reset_index()
    rea_main = px.bar(data_frame=rea_gr, x='YEAR', y='REA', title='REA per år')

    rea_kst = px.line(data_frame=rea, x='YEAR', y='REA', color='PRODUCT', title='REA utveckling per produkt')

    rea = rea[rea['YEAR'] == option_slctd]
    rea_pie = px.pie(data_frame=rea, names='PRODUCT', values='REA')

    return container, pd_lgd, rea_main, rea_kst, rea_pie
