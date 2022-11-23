import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_prototype_data():
    general = {'YEAR': [2019, 2019, 2019, 2019, 2019, 2019,
                        2020, 2020, 2020, 2020, 2020, 2020,
                        2021, 2021, 2021, 2021, 2021, 2021,
                        2022, 2022, 2022, 2022, 2022, 2022],
               'PRODUCT': ['FRITID', 'DIREKT/LEV', 'MASKINFINANS', 'PARTNER FÖRETAG', 'BIL', 'BILKUND'] * 4,
               'NUMBER': [2000, 2998, 2400, 3728, 3092, 2000,
                          2300, 6392, 3628, 2983, 2900, 2973,
                          3782, 2983, 4763, 1092, 3698, 2563,
                          9376, 1999, 2876, 3764, 5782, 1763],
               'AMOUNT': [200000000, 299800000, 240000000, 372800000, 309200000, 200000000,
                          230000000, 639200000, 362800000, 298300000, 290000000, 297300000,
                          378200000, 298300000, 476300000, 109200000, 369800000, 256300000,
                          937600000, 199900000, 287600000, 376400000, 578200000, 176300000]}
    df = pd.DataFrame(general)
    df['YEAR'] = df['YEAR'].astype(str)

    beslut = {'YEAR': [2019, 2019, 2019, 2020, 2020, 2020, 2021, 2021, 2021, 2022, 2022, 2022],
              'TYPE': ['Auto-approved', 'Manual', 'Auto-denied'] * 4,
              'NUMBER': [200, 150, 300, 150, 200, 500, 100, 300, 500, 250, 450, 300]}
    df_beslut = pd.DataFrame(beslut)
    df_beslut['YEAR'] = df_beslut['YEAR'].astype(str)

    sla = {'YEAR': [2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019,
                    2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020,
                    2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021,
                    2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022],
           'MONTH': ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December'] * 4,
           'INCOMING': [1000, 1298, 800, 1982, 1000, 2938, 1652, 2683, 2936, 2675, 1200, 3872,
                        1010, 1311, 808, 2002, 1010, 2967, 1669, 2710, 2965, 2702, 1212, 3911,
                        1023, 1328, 818, 2028, 1023, 3006, 1690, 2745, 3004, 2737, 1228, 3961,
                        1200, 1558, 960, 2378, 1200, 3526, 1982, 3220, 3523, 3210, 0, 0],
           'WITHIN SLA': [0.80, 0.50, 0.88, 0.08, 0.76, 0.40, 0.96, 0.50, 0.17, 0.96, 0.09, 0.70,
                          0.42, 0.65, 0.17, 0.13, 0.90, 0.75, 0.95, 0.80, 0.25, 0.07, 0.06, 0.14,
                          0.64, 0.77, 0.27, 0.51, 0.79, 0.08, 0.18, 0.86, 0.12, 0.12, 0.97, 0.93,
                          0.90, 0.55, 0.83, 0.06, 0.85, 0.63, 0.11, 0.05, 0.78, 0.07, 0.00, 0.00]}
    df_sla = pd.DataFrame(sla)
    df_sla['T'] = 1
    df_sla['OUTSIDE SLA'] = df_sla['T'] - df_sla['WITHIN SLA']
    df_sla['YEAR'] = df_sla['YEAR'].astype(str)
    return df, df_beslut, df_sla


df, beslut, sla = create_prototype_data()

dash.register_page(__name__)
# dash.register_page(__name__, title='Custom Page Title', description='Custom Page Description', image='logo.png')


layout = html.Div([

    html.H1(children="Kreditbeslut", style={'text-align': 'center'}),
    html.H2(children='Denna sida visar statistik kring kreditbesluten', style={'text-align': 'center'}),

    dcc.Graph(id='main_graph_v2', figure={}),
    html.Br(),

    dcc.Graph(id='line_beslut_v2', figure={}),
    html.Br(),

    dcc.Dropdown(id='compare_one',
                 options=[
                     {"label": "2019", "value": "2019"},
                     {"label": "2020", "value": "2020"},
                     {"label": "2021", "value": "2021"},
                     {"label": "2022", "value": "2022"}],
                 multi=False,
                 value='2021',
                 style={"width": "40%"}
                 ),

    dcc.Dropdown(id='compare_two',
                 options=[
                     {"label": "2019", "value": "2019"},
                     {"label": "2020", "value": "2020"},
                     {"label": "2021", "value": "2021"},
                     {"label": "2022", "value": "2022"}],
                 multi=False,
                 value="2022",
                 style={"width": "40%"}
                 ),

    dcc.Graph(id='compare_cookie_v2', figure={}),
    html.Br(),

    html.H1(children="SLA Kreditbeslut", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_kredbes",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),
    html.Div(id='output_container_v2', children=[]),
    html.Br(),

    dcc.Graph(id='combined_SLA_v2', figure={})

])


@callback(
    [Output(component_id='main_graph_v2', component_property='figure'),
     Output(component_id='line_beslut_v2', component_property='figure'),
     Output(component_id='compare_cookie_v2', component_property='figure'),
     Output(component_id='combined_SLA_v2', component_property='figure'),
     Output(component_id='output_container_v2', component_property='children')],
    [Input(component_id='compare_one', component_property='value'),
     Input(component_id='compare_two', component_property='value'),
     Input(component_id='slct_year_kredbes', component_property='value')]
)
def update_graph(comp1_slctd, comp2_slctd, option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    dff = df.copy()
    dff = dff.groupby('YEAR').sum()
    dff = dff.reset_index()
    dff_main = make_subplots(specs=[[{"secondary_y": True}]])
    dff_main.add_trace(
        go.Bar(x=dff['YEAR'], y=dff['NUMBER'], name="Antal inkommande ansökningar"),
        secondary_y=False,
    )
    dff_main.add_trace(
        go.Line(x=dff['YEAR'], y=dff['AMOUNT'], name="Belopp inkommande ansökningar"),
        secondary_y=True,
    )
    dff_main.update_layout(
        title_text="Inkomna ansökningar i antal och belopp"
    ),

    df_bes_line = beslut.copy()
    line_beslut = px.line(df_bes_line, x='YEAR', y='NUMBER', color='TYPE', title='Antal Kreditbeslut per år')

    # Compare cookies
    comp = df.copy()
    comp_one = comp[comp['YEAR'] == comp1_slctd]
    comp_two = comp[comp['YEAR'] == comp2_slctd]
    print(comp_one)
    print(comp_two)
    comp_cookie = make_subplots(1, 2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                                subplot_titles=[comp1_slctd, comp2_slctd])
    comp_cookie.add_trace(go.Pie(labels=comp_one['PRODUCT'], values=comp_one['AMOUNT'],
                                 name=f"Data {comp1_slctd}"), 1, 1)
    comp_cookie.add_trace(go.Pie(labels=comp_two['PRODUCT'], values=comp_two['AMOUNT'],
                                 name=f"Data {comp2_slctd}"), 1, 2)
    comp_cookie.update_layout(title_text='Jämför två år')

    # https://plotly.com/python/multiple-axes/
    df_sla = sla.copy()
    df_sla = df_sla[df_sla["YEAR"] == option_slctd]
    sla_comb = make_subplots(specs=[[{"secondary_y": True}]])
    sla_comb.add_trace(
        go.Bar(x=df_sla['MONTH'], y=df_sla['INCOMING'], name="Antal ansökningar"),
        secondary_y=False,
    )
    sla_comb.add_trace(
        go.Line(x=df_sla['MONTH'], y=df_sla['WITHIN SLA'], name="Andel ansökningar inom SLA"),
        secondary_y=True,
    )
    sla_comb.update_layout(
        title_text="Antal inkomna ansökningar och andel hanterade inom SLA"
    )

    return dff_main, line_beslut, comp_cookie, sla_comb, container
