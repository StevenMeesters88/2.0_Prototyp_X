import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_prototype_data():
    recovery = {'YEAR': ['2019', '2019', '2019', '2019', '2019', '2019',
                         '2020', '2020', '2020', '2020', '2020', '2020',
                         '2021', '2021', '2021', '2021', '2021', '2021',
                         '2022', '2022', '2022', '2022', '2022', '2022'],
                'PRODUCT': ['FRITID', 'DIREKT/LEV', 'MASKINFINANS', 'PARTNER FÖRETAG', 'BIL', 'BILKUND'] * 4,
                'AMOUNT': [1000000, 2666181, 3667181, 1882999, 2766341, 3997363,
                           1100000, 2932799, 4033899, 2071299, 3042975, 4397099,
                           1210000, 1034000, 2756831, 3791865, 1947021, 2860397,
                           1130000, 3012785, 4143915, 2127789, 3125965, 4517020],
                'RECOVERY': [97474, 1625078, 1017480, 1850377, 2182054, 647836,
                             477202, 2268832, 919368, 1044992, 431774, 416820,
                             221317, 325265, 1773600, 371377, 967383, 1045076,
                             688242, 1415965, 2763166, 1786647, 499651, 2721496]}
    df_rec = pd.DataFrame(recovery)
    df_rec['RECOVERYRATE'] = df_rec['RECOVERY'] / df_rec['AMOUNT']

    sena = {'YEAR': ['2019', '2019', '2019', '2019', '2019', '2019',
                     '2020', '2020', '2020', '2020', '2020', '2020',
                     '2021', '2021', '2021', '2021', '2021', '2021',
                     '2022', '2022', '2022', '2022', '2022', '2022'],
            'PRODUCT': ['FRITID', 'DIREKT/LEV', 'MASKINFINANS', 'PARTNER FÖRETAG', 'BIL', 'BILKUND'] * 4,
            'ANDEL_SENA': [0.536284276814696, 0.414624009838438, 0.84995846417981, 0.270961209049615, 0.209154082369185, 0.94235444080566,
                           0.773074296499733, 0.177619460844338, 0.548405528904499, 0.785610059210822, 0.151533674660467, 0.280825678645312,
                           0.876730957152199, 0.95065286412188, 0.378292033744492, 0.167876221231364, 0.84613233827768, 0.282531891320095,
                           0.604187857345718, 0.0690011396771256, 0.539832187280431, 0.480104871349561, 0.141663832720881, 0.683457166201742]}
    df_sena = pd.DataFrame(sena)

    sla = {'YEAR': [2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019,
                    2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020,
                    2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021,
                    2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022],
           'MONTH': ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober',
                     'November', 'December'] * 4,
           'INCOMING': [1000, 1298, 800, 1982, 1000, 2938, 1652, 2683, 2936, 2675, 1200, 3872,
                        1010, 1311, 808, 2002, 1010, 2967, 1669, 2710, 2965, 2702, 1212, 3911,
                        1023, 1328, 818, 2028, 1023, 3006, 1690, 2745, 3004, 2737, 1228, 3961,
                        1200, 1558, 960, 2378, 1200, 3526, 1982, 3220, 3523, 3210, 0, 0],
           'WITHIN SLA': [0.79606043333394, 0.497062744492764, 0.882481006588315, 0.0779744901928777, 0.764151386026766, 0.399572095577161,
                          0.964660102877859, 0.495022275207692, 0.172265308047492, 0.955865873843628, 0.0888523151159025, 0.69721798479357,
                          0.423542958010397, 0.6501553890358, 0.174989275129433, 0.13183577488145, 0.903002131957602, 0.754076320719609,
                          0.949998489129381, 0.802080868945606, 0.252232500326139, 0.0710928904049452, 0.0553096182828587, 0.136465355294125,
                          0.639899505696944, 0.76584502820021, 0.266222471804389, 0.50849908340231, 0.787528152944672, 0.0776518304069788,
                          0.176418040670873, 0.862972147637697, 0.116299297109715, 0.121752581424644, 0.973841533718855, 0.927477708267206,
                          0.902379920934608, 0.551377395055434, 0.833377578293562, 0.0560414503278281, 0.847565438861971, 0.628638259229578,
                          0.112272378884445, 0.0476033906303782, 0.784712872077316, 0.0748123184891425, 0, 0]}
    df_sla = pd.DataFrame(sla)
    df_sla['T'] = 1
    df_sla['YEAR'] = df_sla['YEAR'].astype(str)
    df_sla['OUTSIDE SLA'] = df_sla['T'] - df_sla['WITHIN SLA']
    return df_rec, df_sena, df_sla


rec, sena, sla = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="Krav", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_krav",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_krav', children=[]),
    html.Br(),

    dcc.Graph(id='graph_line_rec', figure={}),
    html.Br(),

    dcc.Graph(id='graph_bar_rec', figure={}),
    html.Br(),

    dcc.Dropdown(id='slct_prod_krav',
                 options=[
                     {'label': 'Fritid', 'value': 'FRITID'},
                     {'label': 'Direkt/Lev', 'value': 'DIREKT/LEV'},
                     {'label': 'Maskinfinans', 'value': 'MASKINFINANS'},
                     {'label': 'Partner Företag', 'value': 'PARTNER FÖRETAG'},
                     {'label': 'Bil', 'value': 'BIL'},
                     {'label': 'Bil Kund', 'value': 'BILKUND'}
                 ]),
    html.Br(),

    dcc.Graph(id='graph_choose_pie', figure={}),
    html.Br(),

    dcc.Graph(id='graph_line_sena', figure={}),
    html.Br(),

    html.H1(children='SLA kravavdelningen', style={'text-align': 'center'}),

    dcc.Dropdown(id='slct_prod_krav2',
                 options=[
                     {'label': 'Fritid', 'value': 'FRITID'},
                     {'label': 'Direkt/Lev', 'value': 'DIREKT/LEV'},
                     {'label': 'Maskinfinans', 'value': 'MASKINFINANS'},
                     {'label': 'Partner Företag', 'value': 'PARTNER FÖRETAG'},
                     {'label': 'Bil', 'value': 'BIL'},
                     {'label': 'Bil Kund', 'value': 'BILKUND'}
                 ]),
    html.Br(),

    dcc.Graph(id='graph_sla_comb', figure={})

])


@callback(
    [Output(component_id='output_container_krav', component_property='children'),
     Output(component_id='graph_line_rec', component_property='figure'),
     Output(component_id='graph_bar_rec', component_property='figure'),
     Output(component_id='graph_choose_pie', component_property='figure'),
     Output(component_id='graph_line_sena', component_property='figure'),
     Output(component_id='graph_sla_comb', component_property='figure')],
    [Input(component_id='slct_year_krav', component_property='value'),
     Input(component_id='slct_prod_krav', component_property='value'),
     Input(component_id='slct_prod_krav2', component_property='value')]
)
def update_graph(option_slctd, prod_slctd, prod_slctd2):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    df_rec = rec.copy()
    line_rec = px.line(data_frame=df_rec, x='YEAR', y='RECOVERYRATE', color='PRODUCT', title='Återvinning per produkt')

    df_rec_year = rec.copy()
    df_rec_year = df_rec_year[df_rec_year['YEAR'] == option_slctd]
    bar_rec = px.bar(data_frame=df_rec_year, x='PRODUCT', y='AMOUNT',
                     title=f'Faktisk återvinning per produkt {option_slctd}')

    p = []
    if prod_slctd == 'FRITID': p = [0.2, 0, 0, 0, 0, 0]
    if prod_slctd == 'DIREKT/LEV': p = [0, 0.2, 0, 0, 0, 0]
    if prod_slctd == 'MASKINFINANS': p = [0, 0, 0.2, 0, 0, 0]
    if prod_slctd == 'PARTNER FÖRETAG': p = [0, 0, 0, 0.2, 0, 0]
    if prod_slctd == 'BIL': p = [0, 0, 0, 0, 0.2, 0]
    if prod_slctd == 'BILKUND': p = [0, 0, 0, 0, 0, 0.2]

    choose_pie = go.Figure(data=[go.Pie(labels=df_rec_year['PRODUCT'], values=df_rec_year['AMOUNT'], pull=p)])

    sena_bet = sena.copy()
    line_sena = px.line(data_frame=sena_bet, x='YEAR', y='ANDEL_SENA', color='PRODUCT',
                        title='Sena betalare per produkt')

    # https://plotly.com/python/multiple-axes/
    df_sla = sla.copy()
    df_sla = df_sla[df_sla["YEAR"] == option_slctd]
    # df_sla = df_sla[df_sla['PRODUCT'] == prod_slctd2]
    sla_comb = make_subplots(specs=[[{"secondary_y": True}]])
    sla_comb.add_trace(
        go.Bar(x=df_sla['MONTH'], y=df_sla['INCOMING'], name="Antal inkomna kravärenden"),
        secondary_y=False,
    )
    sla_comb.add_trace(
        go.Line(x=df_sla['MONTH'], y=df_sla['WITHIN SLA'], name="Andel hanterat inom SLA"),
        secondary_y=True,
    )
    sla_comb.update_layout(
        title_text="""Antal inkomna kravärenden och hantering inom SLA.

        OBS! Produkt dropdown ej kopplat till graf än pga prototyp!"""
    )

    return container, line_rec, bar_rec, choose_pie, line_sena, sla_comb
