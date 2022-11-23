import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_prototype_data():
    inkasso = {'YEAR': ['2019', '2019', '2019', '2019', '2019', '2019',
                        '2020', '2020', '2020', '2020', '2020', '2020',
                        '2021', '2021', '2021', '2021', '2021', '2021',
                        '2022', '2022', '2022', '2022', '2022', '2022'],
               'PRODUCT': ['FRITID', 'DIREKT/LEV', 'MASKINFINANS', 'PARTNER FÖRETAG', 'BIL', 'BILKUND'] * 4,
               'AMOUNT': [1000000, 2666181, 3667181, 1882999, 2766341, 3997363,
                          1100000, 2932799, 4033899, 2071299, 3042975, 4397099,
                          1210000, 1034000, 2756831, 3791865, 1947021, 2860397,
                          1130000, 3012785, 4143915, 2127789, 3125965, 4517020],
               'CASES': [287, 1098, 3621, 112, 615, 2272,
                         720, 1848, 992, 1320, 2817, 1644,
                         331, 804, 2488, 457, 1237, 2483,
                         542, 2288, 2791, 1994, 3005, 1532],
               'KFM': [9, 33, 109, 3, 18, 68,
                       22, 55, 30, 40, 85, 49,
                       10, 24, 75, 14, 37, 74,
                       16, 69, 84, 60, 90, 46],
               'DISPUTE': [19, 40, 30, 200, 39, 48,
                           37, 49, 62, 83, 99, 30,
                           37, 22, 88, 76, 46, 76,
                           39, 98, 201, 87, 109, 70]}
    df_inkasso = pd.DataFrame(inkasso)
    return df_inkasso


df_ = create_prototype_data()

dash.register_page(__name__)


layout = html.Div([

    html.H1(children="Inkasso", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_dc",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_dc', children=[]),
    html.Br(),

    dcc.Graph(id='dc_bar', figure={}),
    html.Br(),

    dcc.Graph(id='dc_pie', figure={}),
    html.Br(),

    dcc.Graph(id='dc_kfm_dispute', figure={}),
    html.Br()
    ]),

@callback(
    [Output(component_id='output_container_dc', component_property='children'),
     Output(component_id='dc_bar', component_property='figure'),
     Output(component_id='dc_pie', component_property='figure'),
     Output(component_id='dc_kfm_dispute', component_property='figure')],
    [Input(component_id='slct_year_dc', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = df_.copy()
    dc_bar = px.bar(data_frame=x, x='YEAR', y='CASES', color='PRODUCT', title='Inkassoärenden per produkt')

    df_pie = df_.copy()
    df_pie = df_pie[df_pie['YEAR'] == option_slctd]
    dc_pie = px.pie(data_frame=df_pie, names='PRODUCT', values='AMOUNT', title='Kapitalbelopp per produkt')

    df_kfm_disp = x.groupby('YEAR').sum()
    df_kfm_disp = df_kfm_disp.reset_index()
    kfm_dispute = make_subplots(specs=[[{"secondary_y": True}]])
    kfm_dispute.add_trace(
        go.Line(x=df_kfm_disp['YEAR'], y=df_kfm_disp['KFM'], name="Antal KFM ärenden"),
        secondary_y=False,
    )
    kfm_dispute.add_trace(
        go.Line(x=df_kfm_disp['YEAR'], y=df_kfm_disp['DISPUTE'], name="Antal bestridanden"),
        secondary_y=True,
    )
    kfm_dispute.update_layout(
        title_text="Antal KFM ärenden och bestridna fordringar"
    )

    return container, dc_bar, dc_pie, kfm_dispute
