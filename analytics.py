import dash
import dash_core_components as dcc
import dash_html_components as html
import urllib.parse
import pandas as pd
import json
import plotly
from plotly.subplots import make_subplots   
from dash.dependencies import Input, Output
import dash_table

df = pd.read_csv('data.csv')
print(df.columns)


data_dict = df.to_dict() 

#Filter By Source
source_uni = df['Source'].unique()
drop_init_val = source_uni.tolist()

#Filter By LOB
lob_uni = df['LOB'].unique()

#Filter By SUB LOB 2
sub_lob_uni = df['SUB_LOB2'].unique()

#Filter By Country Domicile
domicile_country_uni = df['Domicile_Country'].unique()

#Filter By Filter1
filter1_uni = df['Filter1'].unique()

#Filter By Year
year_uni = df['Policy_Year'].unique()

all_cols = df.columns.to_list()

tab3_metrics_cols = ['PremiumAmount','Loss_Cnt','Loss_Cntgt0', 'Loss_Cntgt1000' ,'LossAmount']

tab3_feat_cols = []

for i in all_cols:
    if i not in tab3_metrics_cols:
        tab3_feat_cols.append(i)

tab3_update = {}

col_arr = ['red' , 'yellow' , 'green' , 'orange' , 'pink' ,'blue' , 'brown' , 'cyan' ,'gold' , 'gray' ,'olive' , 'orangered']  

data_download = pd.DataFrame()

app = dash.Dash(__name__, assets_external_path= './assets/')

app.scripts.serve_locally=True

colors = {
    'background': '#FCFAFA ',
    'text': '#111111'
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
dcc.Tabs([
        dcc.Tab(label='Data Filtering', style = {'fontWeight' : 'bold' , 'fontSize' : '25px'}, children=[
                    html.H1(
                        children='',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                        }
                    ),
                    html.Div(style = {'padding' : '10px 10px 10px 10px','display' : 'flex','flex-direction' : 'row','alignItem' : 'center'} ,children = [html.A(html.Button('Refresh Data'),href='/')]),
                    html.Div(id = 'filters-sec' ,style = {'display' : 'flex','flex-direction' : 'row','alignItem' : 'center'} , 
                             children=[
                                html.Div(id = 'filters-1',style = {'display' : 'flex',
                                                     'flex-direction' : 'row',
                                                     'margin-bottom' : '20px',
                                                     'alignItem' : 'center'} , 
                             children=[
                                 html.Div(id = 'filters-1-1',style = {'display' : 'flex',
                                                     'flex-direction' : 'column',
                                                     'alignItem' : 'center',
                                                    'box-shadow': '0 5px 20px 0 rgba(0,0,0, 0.061), 0 10px 30px 0 rgba(0, 0, 0, 0.061)',
                                                    'margin-right' : '5px'} , 
                                          children =[
                                    html.Label( style = {'color' : colors['text']},children='Filter By Source'),
                                    dcc.RadioItems(
                                        id='radio-items-source',
                                        options = [
                                            {'label': 'Select All', 'value': source_uni},
                                            {'label': 'Deselect All', 'value': ''}
                                            ],
                                        value = drop_init_val,
                                        labelStyle={'display': 'inline-block'}
                                    ),
                                    html.Div(
                                              id="multiSelectCombo"
                                    ),
                                    html.Div(
                                              id="checkboxSelectCombo"
                                    ),
                                    dcc.Dropdown(
                                            id='dropdown_source',
                                            style = {'height' : '35px', 'display': 'inline-block'},
                                            options=[{'label': i, 'value': i} for i in source_uni],
                                            value= drop_init_val,
                                            multi=True,
                                            clearable=False
                                        ),
                            ]),
                            html.Div(id = 'filters-1-2',style = {'display' : 'flex',
                                                     'flex-direction' : 'column',
                                                     'alignItem' : 'center',
                                                    'box-shadow': '0 5px 20px 0 rgba(0,0,0, 0.061), 0 10px 30px 0 rgba(0, 0, 0, 0.061)',
                                                    'margin-left' : '0px'} ,children = [
                            html.Label(style = {'color' : colors['text']},children='Filter By LOB'),
                            dcc.RadioItems(
                                id='radio-items-lob',
                                options = [
                                    {'label': 'Select All', 'value': lob_uni},
                                    {'label': 'Deselect All', 'value': ''}

                                    ],
                                value = [],
                                labelStyle={'display': 'inline-block'}
                            ),
                                    dcc.Dropdown(
                                            id='dropdown_lob',
                                            style = {'height' : '35px', 'display': 'inline-block'},
                                            options=[],
                                            value=[],
                                            multi=True
                                        )
                            ])
                        ]),
                    html.Div(id = 'filters-2',style = {'display' : 'flex',
                                                     'flex-direction' : 'row',
                                                     'margin-bottom' : '20px',
                                                     'alignItem' : 'center'} , 
                             children=[
                                 html.Div(id = 'filters-2-1',style = {'display' : 'flex',
                                                     'flex-direction' : 'column',
                                                     'alignItem' : 'center',
                                                    'box-shadow': '0 5px 20px 0 rgba(0,0,0, 0.061), 0 10px 30px 0 rgba(0, 0, 0, 0.061)',
                                                    'margin-right' : '5px'} ,children = [
                        html.Label( style = {'color' : colors['text']},children='Filter By SUB LOB 2'),
                        dcc.RadioItems(
                            id='radio-items-sub-lob',
                            options = [
                                {'label': 'Select All', 'value': sub_lob_uni},
                                {'label': 'Deselect All', 'value': ''}

                                ],
                            value = [],
                            labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Dropdown(
                                            id='dropdown_sub_lob',
                                            style = {'height' : '35px', 'display': 'inline-block'},
                                            options=[],
                                            value=[],
                                            multi=True
                                        )
                    ]),
                        html.Div(id = 'filters-2-2',style = {'display' : 'flex',
                                                     'flex-direction' : 'column',
                                                     'alignItem' : 'center',
                                                    'box-shadow': '0 5px 20px 0 rgba(0,0,0, 0.061), 0 10px 30px 0 rgba(0, 0, 0, 0.061)',
                                                    'margin-left' : '0px'} ,children = [
                        html.Label( style = {'color' : colors['text']},children='Filter By Country Domicile'),
                        dcc.RadioItems(
                            id='radio-items-country-domicile',
                            options = [
                                {'label': 'Select All', 'value': domicile_country_uni},
                                {'label': 'Deselect All', 'value': ''}

                                ],
                            value = [],
                            labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Dropdown(
                                            id='dropdown_country_domicile',
                                            style = {'height' : '35px', 'display': 'inline-block'},
                                            options=[],
                                            value=[],
                                            multi=True
                                        ),
                    ])
                    ]),
                    html.Div(id = 'filters-3',style = {'display' : 'flex',
                                                         'flex-direction' : 'row',
                                                         'margin-bottom' : '20px',
                                                         'alignItem' : 'center'} ,
                             children=[
                        html.Div(id = 'filters-3-1',style = {'display' : 'flex',
                                                     'flex-direction' : 'column',
                                                     'alignItem' : 'center',
                                                    'box-shadow': '0 5px 20px 0 rgba(0,0,0, 0.061), 0 10px 30px 0 rgba(0, 0, 0, 0.061)',
                                                    'margin-right' : '5px'} ,children = [
                        html.Label( style = {'color' : colors['text']},children='Filter By Filter1'),
                        dcc.RadioItems(
                            id='radio-items-filter1',
                            options = [
                                {'label': 'Select All', 'value': filter1_uni},
                                {'label': 'Deselect All', 'value': ''}

                                ],
                            value = [],
                            labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Dropdown(
                                            id='dropdown_filter1',
                                            style = {'height' : '35px', 'display': 'inline-block'},
                                            options=[],
                                            value=[],
                                            multi=True
                                        )
                        ]),
                        html.Div(id = 'filters-3-2',style = {'display' : 'flex',
                                                     'flex-direction' : 'column',
                                                     'alignItem' : 'center',
                                                    'box-shadow': '0 5px 20px 0 rgba(0,0,0, 0.061), 0 10px 30px 0 rgba(0, 0, 0, 0.061)',
                                                    'margin-left' : '0px'} ,children = [
                        html.Label( style = {'color' : colors['text']},children='Filter By Year'),
                        dcc.RadioItems(
                            id='radio-items-year',
                            options = [
                                {'label': 'Select All', 'value': year_uni},
                                {'label': 'Deselect All', 'value': ''}

                                ],
                            value = [],
                            labelStyle={'display': 'inline-block'}
                        ),
                        dcc.Dropdown(
                                            id='dropdown_year',
                                            style = {'height' : '35px', 'display': 'inline-block'},
                                            options=[],
                                            value=[],
                                            multi=True
                                        )
                     ])
                    ])
                    ]),
                    dcc.Tabs([
                        dcc.Tab(label='Bar Graph', style = {'fontWeight' : 'bold' , 'fontSize' : '20px'}, children=[
                                html.Div(style = {'display' : 'flex',
                                             'flex-direction' : 'row'},
                                             children = [
                                             dcc.Graph(
                                                style = {'width' : '50%',
                                                         'height' : '50%'},
                                                id='Graph1',
                                                figure={}
                                ),
                                dcc.Graph(
                                    style = {'width' : '50%',
                                             'height' : '50%'},
                                    id='Graph2',
                                    figure={}
                                )
                            ]),
                            html.Div(style = {'display' : 'flex',
                                             'flex-direction' : 'row'},
                                             children = [
                                                dcc.Graph(
                                                style = {'width' : '50%',
                                                         'height' : '50%'},
                                                id='Graph3',
                                                figure={}
                                ),
                                dcc.Graph(
                                    style = {'width' : '50%',
                                             'height' : '50%'},
                                    id='Graph4',
                                    figure={}
                                )
                        ])
                    ]),
                dcc.Tab(label='Pie Chart', style = {'fontWeight' : 'bold' , 'fontSize' : '20px'}, children=[
                            html.Div(style = {'display' : 'flex',
                                              'flex-direction' : 'row',
                                              'marginTop' : '30px'}),
                            html.Div(style = {'display' : 'flex',
                                         'flex-direction' : 'row'},  
                                         children=[
                            dcc.Graph(
                                    style = {'width' : '50%',
                                         'height' : '50%'},
                                id='Graph5',
                                figure={}
                            ),
                            dcc.Graph(
                                style = {'width' : '50%',
                                         'height' : '50%'},
                                id='Graph6',
                                figure={}
                            )]),
                    html.Div(id = "bot-g" ,style = {'display' : 'flex',
                                         'flex-direction' : 'row',
                                         'alignItem' : 'center'},  
                                         children=[
                            dcc.Graph(
                                    style = {'width' : '50%',
                                         'height' : '50%',
                                         'margin-left' : '25%'},
                                id='Graph7',
                                figure={}
                            )
                    ]
                )]
            )

        ])
        ]),
        dcc.Tab(label='Data Display', style = {'fontWeight' : 'bold' , 'fontSize' : '25px'}, children=[
            html.Div(id='display-feat-top', style = {'display': 'flex' ,
                                                     'margin-top' : '20px',
                                                 'flex-direction' : 'row'
                                                } ,children = [
                        html.Div(id='display-feat', style = {
                                                             'width' : '20%'} , 
                        children = [
                            html.Div(id='display-table-feat',
                                     style = {'margin-bottom' : '20px' , 'box-shadow': '0 5px 20px 0 rgba(68, 59, 59, 0.2), 0 10px 30px 0 rgba(0, 0, 0, 0.09)'},
                                                                      children = [
                                    html.Label( style = {'color' : 'black', 'fontSize' : '25px'},children='Features :'),
                                    dcc.Dropdown(
                                            id='dropdown_feat_columns',
                                            options=[{'label': i, 'value': i} for i in tab3_feat_cols],
                                            value=[],
                                            multi=True
                                        )
                            ]),
                            html.Div(id='display-table-metric',
                                     style = {'margin-bottom' : '10px' ,'box-shadow': '0 5px 20px 0 rgba(68, 59, 59, 0.2), 0 10px 30px 0 rgba(0, 0, 0, 0.09)'},
                                     children = [
                            html.Label( style = {'color' : 'black' , 'fontSize' : '25px'},children='Metrics :'),
                            dcc.Dropdown(
                                            id='dropdown_metric_columns',
                                            options=[{'label': i, 'value': i} for i in tab3_metrics_cols],
                                            value=[],
                                            multi=True
                                        )
                            ])
                        ]),
            html.Div(id='display-table-in', style = {
                                                  'alignItem' : 'center',
                                                  'textAlign' : 'center',
                                                  'width' : '80%'
                                                } ,
                         children = [
                             
                                 dcc.RadioItems(
                                    id='filter-query-read-write',
                                    options=[
                                        {'label': 'Read filter_query', 'value': 'read'}
                                    ],
                                    value='read'
                                ),

                                dcc.Input(id='filter-query-input', placeholder='Enter filter query'),

                                html.Div(id='filter-query-output'),

                                html.Hr(),
                             html.A(
                                'Download Data',
                                id='download-link',
                                download="rawdata.csv",
                                href="",
                                target="_blank"
                             ),
                             
                             
                            dash_table.DataTable(
                            id='datatable-interactivity',
                            columns=[],
                            data = [],
                            page_current=0,
                            editable=True,
                            page_action='native',
                            page_size=10,
                            filter_action="native",
                            virtualization=True,
                            style_cell_conditional=[
                                    {
                                        'if': {'column_id': c},
                                        'textAlign': 'left'
                                    } for c in ['Date', 'Region']
                                ],
                             style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                             style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'
                                }
                                ),
                             html.Div(id='datatable-query-structure', style={'whitespace': 'pre'})
                         ])
                    ])
            ])
        ])
    ])



@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('datatable-interactivity', 'data')])
def update_download_link(data):
    data_download = pd.DataFrame.from_dict(data)
    csv_string = data_download.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

############################################################################################################

@app.callback(
    [Output('filter-query-input', 'style'),
     Output('filter-query-output', 'style')],
    [Input('filter-query-read-write', 'value')])
    
def query_input_output(val):
    input_style = {'width': '100%'}
    output_style = {}
    if val == 'read':
        input_style.update(display='none')
        output_style.update(display='inline-block')
    else:
        input_style.update(display='inline-block')
        output_style.update(display='none')
    return input_style, output_style


@app.callback(
    Output('datatable-interactivity', 'filter_query'),
    [Input('filter-query-input', 'value')]
)
def write_query(query):
    if query is None:
        return ''
    return query


@app.callback(
    Output('filter-query-output', 'children'),
    [Input('datatable-interactivity', 'filter_query')]
)
def read_query(query):
    if query is None:
        return "No filter query"
    return dcc.Markdown('`filter_query = "{}"`'.format(query))


@app.callback(
    Output('datatable-query-structure', 'children'),
    [Input('datatable-interactivity', 'derived_filter_query_structure')]
)
def display_query(query):
    if query is None:
        return ''
    return html.Details([
        html.Summary('Derived filter query structure'),
        html.Div(dcc.Markdown('''```json
{}
```'''.format(json.dumps(query, indent=4))))
    ])

############################################################################################################

# CALLBACKS TO SET THE CHECK LIST OPTIONS ###########
###############################################


# SOURCE TO ALL OTHER FEATURES
@app.callback(
    dash.dependencies.Output('dropdown_lob', 'options'),
    [dash.dependencies.Input('dropdown_source', 'value')])
def update_lob_on_src(source_val):
    data_source = pd.DataFrame()
    
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if data_source.empty:
        options = []
        return options
    
    f_lob_unique = data_source['LOB'].unique()
    options = [{'label': i, 'value': i} for i in f_lob_unique]
    return options

@app.callback(
    dash.dependencies.Output('dropdown_sub_lob', 'options'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value')])
def update_slob_on_sl(source_val , lob_val):
    data_source = pd.DataFrame()
    
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
    
    if data_source.empty:
        options = []
        return options
    
    f_sub_lob_unique = data_source['SUB_LOB2'].unique()
    options = [{'label': i, 'value': i} for i in f_sub_lob_unique]
    return options

@app.callback(
    dash.dependencies.Output('dropdown_country_domicile', 'options'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value')])
def update_f1_on_sls(source_val , lob_val , sub_lob_val):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
        
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
        
    if data_source.empty:
        options = []
        return options
    
    f_filter1_unique = data_source['Domicile_Country'].unique()
    options = [{'label': i, 'value': i} for i in f_filter1_unique]
    return options

@app.callback(
    dash.dependencies.Output('dropdown_filter1', 'options'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value')])
def update_cd_on_slsf(source_val , lob_val , sub_lob_val , country_dom_val):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
        
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
        
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
        
    if data_source.empty:
        options = []
        return options
    
    f_dc_unique = data_source['Filter1'].unique()
    options = [{'label': i, 'value': i} for i in f_dc_unique]
    return options

@app.callback(
    dash.dependencies.Output('dropdown_year', 'options'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value')])
def update_y_on_slsfcd(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
        
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
        
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
        
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
    
    if data_source.empty:
        options = []
        return options
    
    f_y_unique = data_source['Policy_Year'].unique()
    options = [{'label': i, 'value': i} for i in f_y_unique]
    return options


#############################

#TAB1 CHART UPDATION GRAPH1#######
######################################

@app.callback(
    dash.dependencies.Output('Graph1', 'figure'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_graph1_on_features(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val ,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
        
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
        
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
        
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
        
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
    
    if data_source.empty:
        fig = {}
        return fig
        
    avg_premium_data = data_source.groupby(['Policy_Year']).agg({'PremiumAmount': ['mean']}).reset_index()
    
    avg_premium_amt = avg_premium_data['PremiumAmount'].values.tolist()
    pol_year = avg_premium_data['Policy_Year'].values.tolist()
    avg_premium_amt = [item for sublist in avg_premium_amt for item in sublist]
    count_policies = data_source.groupby(['Policy_Year']).agg({'Key_Field': ['count']}).reset_index()
    
    count_policies = count_policies['Key_Field'].values.tolist()
    count_policies = [item for sublist in count_policies for item in sublist]
    pol_year = [str(i) for i in pol_year]
    
    avg_premium_amt = [int(item) for item in avg_premium_amt]
    
    pol_year = avg_premium_data['Policy_Year'].astype('str')

#     data_bar = plotly.graph_objs.Bar(x= pol_year,y=avg_premium_amt)
#     data_scatter = plotly.graph_objs.Scatter(x = pol_year, y = count_policies)
     
        # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
    plotly.graph_objs.Bar(x= pol_year, y= avg_premium_amt, name="Avg Premium Amount"),
    secondary_y=False,
    )
    fig.add_trace(
    plotly.graph_objs.Scatter(x=pol_year, y=count_policies, name="Policies Count"),
    secondary_y=True,
    )
    fig.update_layout(
        title_text=""
    )
    fig.update_layout(
        xaxis= {'type': 'category'}
    )
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="<b>Premium Amount Avg</b> ", secondary_y=False)
    fig.update_yaxes(title_text="<b>PoliciesCount</b> ", secondary_y=True)
    
    
    return fig

     

#TAB1 CHART UPDATION GRAPH2

@app.callback(
    dash.dependencies.Output('Graph2', 'figure'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_graph2_on_features(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
        
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
        
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
        
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
        
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
        
    if data_source.empty:
        fig = {}
        return fig
    
    sum_premium_data = data_source.groupby(['Policy_Year']).agg({'PremiumAmount': ['sum']}).reset_index()
    
    sum_premium_amt = sum_premium_data['PremiumAmount'].values.tolist()
    pol_year = sum_premium_data['Policy_Year'].values.tolist()
    sum_premium_amt = [item for sublist in sum_premium_amt for item in sublist]
    pol_year = [str(i) for i in pol_year]
    
    sum_premium_amt = [int(item) for item in sum_premium_amt]
    
    data_bar = plotly.graph_objs.Bar(x= pol_year,y=sum_premium_amt, name="Premium Amount Sum")
    layout = plotly.graph_objs.Layout(xaxis={'type': 'category'})
    fig = plotly.graph_objs.Figure([data_bar], layout)
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="<b>Premium Amount Sum</b> ")
    
    return fig 

#TAB1 CHART UPDATION GRAPH3

@app.callback(
    dash.dependencies.Output('Graph3', 'figure'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_graph3_on_features(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
        
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
        
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
        
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
        
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
     
    if data_source.empty:
        fig = {}
        return fig
    
    sum_premium_data = data_source.groupby(['Policy_Year']).agg({'LossAmount': ['sum']}).reset_index()
    
    sum_premium_amt = sum_premium_data['LossAmount'].values.tolist()
    pol_year = sum_premium_data['Policy_Year'].values.tolist()
    sum_premium_amt = [item for sublist in sum_premium_amt for item in sublist]
    pol_year = [str(i) for i in pol_year]
    
    sum_premium_amt = [int(item) for item in sum_premium_amt]
    print("SUMMMMMMMMMMM",sum_premium_amt[:5])
    
    data_bar = plotly.graph_objs.Bar(x= pol_year,y=sum_premium_amt , name="Loss Amount")
    layout = plotly.graph_objs.Layout(xaxis={'type': 'category'})
    fig = plotly.graph_objs.Figure([data_bar], layout)
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="<b>Loss Amount Sum</b> ")
     
    return fig

#TAB1 CHART UPDATION GRAPH4

@app.callback(
    dash.dependencies.Output('Graph4', 'figure'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_graph4_on_features(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
        
    if data_source.empty:
        fig = {}
        return fig
    
    loss_premium_data = data_source.groupby(['Policy_Year']).agg({'LossRatio': ['mean']}).reset_index()
    loss_premium_amt = loss_premium_data['LossRatio'].values.tolist()
    pol_year = loss_premium_data['Policy_Year'].values.tolist()
    loss_premium_amt = [item for sublist in loss_premium_amt for item in sublist]
    pol_year = [str(i) for i in pol_year]
    
    loss_premium_amt = [int(item *100) for item in loss_premium_amt]
    
    data_bar = plotly.graph_objs.Scatter(x= pol_year,y=loss_premium_amt)
    layout = plotly.graph_objs.Layout(xaxis={'type': 'category'})
    fig = plotly.graph_objs.Figure([data_bar], layout)
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="<b>Loss Ratio</b> ")
    return fig
     
@app.callback(
    dash.dependencies.Output('Graph5', 'figure'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_graph5_on_features(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
        
    if data_source.empty:
        fig = {}
        return fig
    
    labels = ['Linkage1 : 0','Linkage1 : 1']
    values = []
    a = data_source[data_source['Linkage1'] == 0].count()['Linkage1']
    b = data_source[data_source['Linkage1'] == 1].count()['Linkage1']
    tot = data_source['Linkage1'].shape[0]
    values.append(a/tot)
    values.append(b/tot)
    figure = {'data': [plotly.graph_objs.Pie(labels=labels,
          values=values)], 'layout': {'margin': {
    'l': 30,
    'r': 0,
    'b': 30,
    't': 20,
    }, 'legend': {'x': 0, 'y': 1}}}
    return figure


@app.callback(
    dash.dependencies.Output('Graph6', 'figure'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_graph6_on_features(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
    
    if data_source.empty:
        fig = {}
        return fig
    
    labels = ['Linkage2 : 0','Linkage2 : 1']
    values = []
    a = data_source[data_source['Linkage2'] == 0].count()['Linkage2']
    b = data_source[data_source['Linkage2'] == 1].count()['Linkage2']
    tot = data_source['Linkage2'].shape[0]
    values.append(a/tot)
    values.append(b/tot)
    figure = {'data': [plotly.graph_objs.Pie(labels=labels,
          values=values)], 'layout': {'margin': {
    'l': 30,
    'r': 0,
    'b': 30,
    't': 20,
    }, 'legend': {'x': 0, 'y': 1}}}
    return figure


@app.callback(
    dash.dependencies.Output('Graph7', 'figure'),
    [dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_graph7_on_features(source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
    
    if data_source.empty:
        fig = {}
        return fig
    
    labels = ['Linkage3 : 0','Linkage3 : 1']
    values = []
    a = data_source[data_source['Linkage3'] == 0].count()['Linkage3']
    b = data_source[data_source['Linkage3'] == 1].count()['Linkage3']
    tot = data_source['Linkage3'].shape[0]
    values.append(a/tot)
    values.append(b/tot)
    figure = {'data': [plotly.graph_objs.Pie(labels=labels,
          values=values)], 'layout': {'margin': {
    'l': 30,
    'r': 0,
    'b': 30,
    't': 20,
    }, 'legend': {'x': 0, 'y': 1}}}

    return figure


##############################################

#UPDATING DATA IN TAB3#######
######################################

@app.callback(
    dash.dependencies.Output('datatable-interactivity', 'columns'),
    [dash.dependencies.Input('dropdown_feat_columns', 'value'),
     dash.dependencies.Input('dropdown_metric_columns', 'value'),
    dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_tablecolumns_on_features(val1 , val2 ,source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val ,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    tab = val1 + val2
    tab3_update = {name: name for name in tab}
    columns=[{"name": i, "id": i} for i in tab3_update]
    return columns
    
@app.callback(
    dash.dependencies.Output('datatable-interactivity', 'data'),
    [dash.dependencies.Input('dropdown_feat_columns', 'value'),
     dash.dependencies.Input('dropdown_metric_columns', 'value'),
    dash.dependencies.Input('dropdown_source', 'value'),
    dash.dependencies.Input('dropdown_lob', 'value'),
    dash.dependencies.Input('dropdown_sub_lob', 'value'),
    dash.dependencies.Input('dropdown_filter1', 'value'),
    dash.dependencies.Input('dropdown_country_domicile', 'value'),
    dash.dependencies.Input('dropdown_year', 'value'),
    dash.dependencies.Input('radio-items-source', 'value'),
    dash.dependencies.Input('radio-items-lob', 'value'),
    dash.dependencies.Input('radio-items-sub-lob', 'value'),
    dash.dependencies.Input('radio-items-country-domicile', 'value'),
    dash.dependencies.Input('radio-items-filter1', 'value'),
    dash.dependencies.Input('radio-items-year', 'value')])
def update_tabledata_on_features(val1 , val2 , source_val , lob_val , sub_lob_val , filter1_val , country_dom_val , year_val ,r_s_val , r_l_val, r_sl_val,r_cd_val,r_f_val,r_y_l):
    data_source = pd.DataFrame()
    if len(source_val) != 0:
        data_source = df.loc[df['Source'].isin(source_val)]
    
    if len(lob_val) != 0:
        data_source = data_source.loc[df['LOB'].isin(lob_val)]
        
    if len(sub_lob_val) != 0:
        data_source = data_source.loc[df['SUB_LOB2'].isin(sub_lob_val)]
        
    if len(country_dom_val) != 0:
        data_source = data_source.loc[df['Domicile_Country'].isin(country_dom_val)]
        
    if len(filter1_val) != 0:
        data_source = data_source.loc[df['Filter1'].isin(filter1_val)]
        
    if len(year_val) != 0:
        data_source = data_source.loc[df['Policy_Year'].isin(year_val)]
    
    if data_source.empty:
        return data_source.to_dict('records')
    
    if len(val2) != 0: 
        agg_input = { i : ['sum'] for i in val2}
        data = data_source.groupby(val1).agg(agg_input).reset_index()
        er_tup = data.columns.ravel() 
        data.columns = [x[0] for x in er_tup]
        data_download = data
        return data.to_dict('records')
    else:
        data = data_source[val1]
        data_download = data
        return data.to_dict('records')
    
#     return data.iloc[
#         page_current*page_size:(page_current+ 1)*page_size
#     ].to_dict('records')



######################################

#UPDATE FOR SELECT AND DESELECT ALL#######
######################################

@app.callback(
    dash.dependencies.Output('dropdown_source', 'value'),
    [dash.dependencies.Input('radio-items-source', 'value')])
def update_source_on_radio(val):
    return val

# @app.callback(
#     dash.dependencies.Output('radio-items-source', 'value'),
#     [dash.dependencies.Input('dropdown_source', 'value')])
# def update_radio_on_source(val):
#     return val
    
@app.callback(
    dash.dependencies.Output('dropdown_lob', 'value'),
    [dash.dependencies.Input('radio-items-lob', 'value')])
def update_lob_on_radio(val):
    return val

@app.callback(
    dash.dependencies.Output('dropdown_sub_lob', 'value'),
    [dash.dependencies.Input('radio-items-sub-lob', 'value')])
def update_sub_lob_on_radio(val):
    return val
    
@app.callback(
    dash.dependencies.Output('dropdown_country_domicile', 'value'),
    [dash.dependencies.Input('radio-items-country-domicile', 'value')])
def update_country_domicile_on_radio(val):
    return val
    
@app.callback(
    dash.dependencies.Output('dropdown_filter1', 'value'),
    [dash.dependencies.Input('radio-items-filter1', 'value')])
def update_filter1_on_radio(val):
    return val

@app.callback(
    dash.dependencies.Output('dropdown_year', 'value'),
    [dash.dependencies.Input('radio-items-year', 'value')])
def update_year_on_radio(val):
    return val
    
######################################
			

if __name__ == '__main__':
    app.run_server(debug=False)