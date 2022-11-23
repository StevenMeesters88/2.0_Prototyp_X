import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_prototype_data():
    nyfors = {'YEAR': ['2019', '2019', '2019', '2019', '2019', '2019',
                       '2020', '2020', '2020', '2020', '2020', '2020',
                       '2021', '2021', '2021', '2021', '2021', '2021',
                       '2022', '2022', '2022', '2022', '2022', '2022'],
              'PRODUCT': ['FRITID', 'DIREKT/LEV', 'MASKINFINANS', 'PARTNER FÖRETAG', 'BIL', 'BILKUND'] * 4,
              'NUMBER': [2000, 2998, 2400, 3728, 3092, 2000,
                         2300, 6392, 3628, 2983, 2900, 2973,
                         3782, 2983, 4763, 1092, 3698, 2563,
                         9376, 1999, 2876, 3764, 5782, 1763],
              'AMOUNT': [200000000, 299800000, 240000000, 372800000, 309200000, 200000000,
                         230000000, 639200000, 362800000, 298300000, 290000000, 297300000,
                         378200000, 298300000, 476300000, 109200000, 369800000, 256300000,
                         937600000, 199900000, 287600000, 376400000, 578200000, 176300000],
              'VIKT_PD': [0.659258906, 0.460561449, 0.358049346, 0.432985079, 0.555518317, 0.896592186,
                          0.708299122, 0.815828718, 0.133684565, 0.648763896, 0.449169742, 0.012256129,
                          0.330783015, 0.622984669, 0.024536918, 0.784785186, 0.041116266, 0.674404458,
                          0.594336136, 0.615146963, 0.877339341, 0.601747963, 0.714285171, 0.252606651],
              'VIKT_LGD': [0.659258906363315, 0.460561448904706, 0.35804934602234, 0.432985079203213, 0.55551831683985,
                           0.896592186106071,
                           0.7082991216033, 0.815828718152686, 0.133684565126567, 0.648763896030477, 0.44916974212386,
                           0.0122561291612644,
                           0.330783014510771, 0.622984669456101, 0.0245369181361743, 0.784785186109233,
                           0.0411162658349272, 0.674404458384901,
                           0.594336135849715, 0.615146963415038, 0.87733934062785, 0.601747963188352, 0.714285170539325,
                           0.252606650756994]}
    df_nyfors = pd.DataFrame(nyfors)
    return df_nyfors


df_ = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="Nyförsäljning", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_x",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_nyfors', children=[]),
    html.Br(),

    dcc.Graph(id='line_nyfors', figure={}),
    html.Br(),

    dcc.Graph(id='bar_nyfors', figure={}),
    html.Br(),

    dcc.Dropdown(id='slct_prod_x',
                 options=[
                     {'label': 'Fritid', 'value': 'FRITID'},
                     {'label': 'Direkt/Lev', 'value': 'DIREKT/LEV'},
                     {'label': 'Maskinfinans', 'value': 'MASKINFINANS'},
                     {'label': 'Partner Företag', 'value': 'PARTNER FÖRETAG'},
                     {'label': 'Bil', 'value': 'BIL'},
                     {'label': 'Bil Kund', 'value': 'BILKUND'}
                 ]),

    dcc.Graph(id='pie_nyfors_one', figure={}),
    html.Br(),

    dcc.Graph(id='line_nyfors_vikt_pd', figure={}),
    html.Br(),

    dcc.Graph(id='line_nyfors_vikt_el', figure={})
    ]),


@callback(
    [Output(component_id='output_container_nyfors', component_property='children'),
     Output(component_id='line_nyfors', component_property='figure'),
     Output(component_id='bar_nyfors', component_property='figure'),
     Output(component_id='pie_nyfors_one', component_property='figure'),
     Output(component_id='line_nyfors_vikt_pd', component_property='figure'),
     Output(component_id='line_nyfors_vikt_el', component_property='figure')],
    [Input(component_id='slct_year_x', component_property='value'),
     Input(component_id='slct_prod_x', component_property='value')]
)
def update_graph(option_slctd, prod_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = df_.copy()
    line = px.line(data_frame=x, x='YEAR', y='NUMBER', color='PRODUCT', title='Nyförsäljning: Antal avtal')
    bar_data = px.bar(x, x="YEAR", y="AMOUNT", color="PRODUCT", title="Nyförsäljning i kronor")
    # bar_data.update_layout(template='plotly_dark')

    f = df_
    f = f[f['YEAR'] == option_slctd]
    p = []
    if prod_slctd == 'FRITID': p = [0.2, 0, 0, 0, 0, 0]
    if prod_slctd == 'DIREKT/LEV': p = [0, 0.2, 0, 0, 0, 0]
    if prod_slctd == 'MASKINFINANS': p = [0, 0, 0.2, 0, 0, 0]
    if prod_slctd == 'PARTNER FÖRETAG': p = [0, 0, 0, 0.2, 0, 0]
    if prod_slctd == 'BIL': p = [0, 0, 0, 0, 0.2, 0]
    if prod_slctd == 'BILKUND': p = [0, 0, 0, 0, 0, 0.2]
    fig = go.Figure(data=[go.Pie(labels=f['PRODUCT'], values=f['NUMBER'], pull=p)])
    fig.update_layout(title='Antal nya avtal')

    df_pd = df_.copy()
    vikt_pd = px.line(data_frame=df_pd, x='YEAR', y='VIKT_PD', color='PRODUCT', title='Viktat PD Nyförsäljning')

    df_pd['VIKT_EL'] = df_pd['VIKT_PD'] * df_pd['VIKT_LGD']
    vikt_el = px.line(data_frame=df_pd, x='YEAR', y='VIKT_EL', color='PRODUCT', title='Viktat EL Nyförsäljning')

    return container, line, bar_data, fig, vikt_pd, vikt_el
