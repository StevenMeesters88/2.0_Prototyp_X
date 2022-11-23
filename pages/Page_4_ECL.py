import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd


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


ecl_df = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="ECL", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_ecl",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_ecl', children=[]),
    html.Br(),

    dcc.Graph(id='ecl_line_one', figure={}),
    html.Br(),

    dcc.Graph(id='ecl_pie_one', figure={}),
    html.Br()

    ])


@callback(
    [Output(component_id='output_container_ecl', component_property='children'),
     Output(component_id='ecl_line_one', component_property='figure'),
     Output(component_id='ecl_pie_one', component_property='figure')],
    [Input(component_id='slct_year_ecl', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = ecl_df.copy()
    line = px.bar(data_frame=x, x='YEAR', y='ECLFINAL', color='PRODUCT', title='ECL över åren per produkt')

    ecl_pie_df = ecl_df.copy()
    ecl_pie_df = ecl_pie_df[ecl_pie_df['YEAR'] == option_slctd]
    ecl_pie_graph = px.pie(data_frame=ecl_pie_df, names='PRODUCT', values='ECLFINAL', title=f'ECL fördelat per {option_slctd}')

    return container, line, ecl_pie_graph
