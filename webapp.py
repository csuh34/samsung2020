# 8/6/20

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output, State
import os
import flask
from sklearn.ensemble import RandomForestRegressor
pj = os.path.join
import pathlib
import os
import glob
import dash_bootstrap_components as dbc
import math

from functions1 import empty_png, plot_shap, predict_gain
from functions2 import get_max, gain_pred_file, column_name, filter_df

# image load variables
static_image_route = '/static/'
mypath = str(pathlib.Path('__file__').parent.absolute())
image_directory = mypath +'/png/'

# check if final csv exists
model_run = mypath + '/gain_pred_result.csv'
binnan_run = mypath + '/binwise_samples_nan_removed.csv'

# dash bootstrap components stylesheet
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([

    # header
    dbc.Row(
        [
            dbc.Col(html.H2('MMU Gain Prediction Visualization', style={'textAlign':'center'}), width=12),
            dbc.Col(html.H3('Prediction Overview', style={'textAlign':'center'}), width=12),
            dbc.Col(html.Br(), width=12)
        ]
    ),

    # contents
    dbc.Row(
        [
            # filters
            dbc.Col(
                [
                    dbc.Row(
                        html.H6('Upload Model File for IP Tput:')
                    ),
                    # uplaod ip tput model
                    dbc.Row(
                        dcc.Upload(
                            id='upload_model1',
                            children=html.Div([
                                'Drag and Drop or ', html.A('Select Files')
                            ]),
                            style={
                                'width': '99%', 'height': '40px', 'lineHeight': '40px',
                                'borderWidth': '1px', 'borderStyle': 'dashed',
                                'borderRadius': '5px', 'textAlign': 'center',
                                'margin': '3px', 'display': 'inline-block'
                            }, multiple=False
                        )
                    ),
                    dbc.Row(html.Br()),
                    dbc.Row(
                        html.H6('Upload Model File for Volume:')
                    ),
                    # uplaod vol model
                    dbc.Row(
                        dcc.Upload(
                            id='upload_model2',
                            children=html.Div([
                                'Drag and Drop or ', html.A('Select Files')
                            ]),
                            style={
                                'width': '99%', 'height': '40px', 'lineHeight': '40px',
                                'borderWidth': '1px', 'borderStyle': 'dashed',
                                'borderRadius': '5px', 'textAlign': 'center',
                                'margin': '3px', 'display': 'inline-block'
                            }, multiple=False
                        )
                    ),
                    dbc.Row(html.Br()),
                    dbc.Row(
                        html.H6('Upload Input File (.feather):')
                    ),
                    # uplaod input file
                    dbc.Row(
                        dcc.Upload(
                            id='upload_input',
                            children=html.Div([
                                'Drag and Drop or ', html.A('Select Files')
                            ]),
                            style={
                                'width': '99%', 'height': '40px', 'lineHeight': '40px',
                                'borderWidth': '1px', 'borderStyle': 'dashed',
                                'borderRadius': '5px','textAlign': 'center',
                                'margin': '3px', 'display': 'inline-block'
                            }, multiple=True
                        )
                    ),
                  dbc.Row(html.Hr()),
                    dbc.Row(
                        html.H6('Select Gain Type:')
                    ),
                    # select gain type - radio items
                    dbc.Row(
                        dcc.RadioItems(
                            id='gain_type',
                            options=[
                                {'label': 'Tput', 'value': '_cell_iptgain_weighted_pred'},
                                {'label': 'Volume', 'value': '_cell_dlvolgain_pred'}
                            ],
                            value='_cell_iptgain_weighted_pred', labelStyle={'display': 'inline-block'},
                            className="dcc_control", inputStyle={"margin-left": "10px", "margin-right": "3px"}
                        )
                    ),
                    dbc.Row(html.Br()),
                    dbc.Row(
                        html.H6('Filter by Gain Range:')
                    ),
                    # set gain range - rangeslider
                    dbc.Col(
                        dcc.RangeSlider(
                            id='gain_range', min=0, max=10, step=0.01, value=[0,10], updatemode='drag',
                            marks={i: '{}00%'.format(i) for i in range(1, 11)}
                        )
                    ),
                    dbc.Row(html.Br()),
                    dbc.Row(
                        html.H6('Filter by Circle:')
                    ),
                    # select circles, radioitems & dropdown - all or custom
                    dbc.Row(
                        dcc.RadioItems(
                            id='radio_circle',
                            options=[
                                {'label': 'All', 'value': 'all'},
                                {'label': 'Customize', 'value': 'custom'}
                            ],
                            value='all', labelStyle={'display': 'inline-block'},
                            className="dcc_control", inputStyle={"margin-left": "10px", "margin-right": "3px"}
                        )
                    ),
                    dbc.Row(
                        dcc.Dropdown(
                            id='dropdown_circle', multi=True, className="dcc_control", style=dict(width='80%')
                        )
                    ),
                    dbc.Row(html.Br()),
                    dbc.Row(
                        html.H6('Filter by Band:')
                    ),
                    # select band - dropdown
                    dbc.Row(
                        dcc.Dropdown(
                            id='dropdown_band',className="dcc_control", style=dict(width='80%')
                        )
                    ),
                    dbc.Row(html.Br()),
                    dbc.Row(
                        html.H6('Select Interference:')
                    ),
                    # select interference
                    dbc.Row(
                        dcc.RadioItems( # interference
                            id='inter',
                            options=[
                                {'label': 'True', 'value': 'true'},
                                {'label': 'False', 'value': 'false'},
                                {'label': 'All', 'value': 'all'}
                            ],
                            value='all', labelStyle={'display': 'inline-block'},
                            className="dcc_control", inputStyle={"margin-left": "10px", "margin-right": "3px"}
                        )
                    ),
                    dbc.Row(html.Hr()),
                    dbc.Row(html.Br())
                ], width={"size": 2, "offset": 1}
            ), # filters end

            # table and bar
            dbc.Col(
                [
                    dbc.Row(
                        html.H4('Sorted Table Chart of Gain Prediction')
                    ),
                    # dislay table chart
                    dbc.Row(
                        html.Div(
                            # sorted table chart
                            html.H4('Sorted Table Chart of Gain Prediction'),
                            id='table_chart'
                        )
                    ),
                    dbc.Row(
                        html.H4('Sorted Bar Chart of Gain Prediction')
                    ),
                    # dislay bar chart
                    dbc.Row(
                        html.Div(
                            [
                                # sorted bar plot
                                dcc.Graph(
                                    id='bar_plot'
                                )
                            ]
                        )
                    )
                ], width={"size": 4, "offset": 0}
            ), # table and bar end
          
          
            # shap plots
            dbc.Col(
                [
                    dbc.Row(
                        html.H4('SHAP Values')
                    ),
                    dbc.Row(
                        html.H6('Select short names to generate SHAP value')
                    ),
                    # select short names to generate shap value plots
                    dbc.Row(
                        dcc.Dropdown(
                                id='dropdown_shap', multi=True, className="dcc_control", style=dict(width='80%')
                        )
                    ),
                    dbc.Row(
                        html.Div(
                            id='return_names'
                        )
                    ),
                    # click to generate plots
                    dbc.Row(
                        html.Button('Generate Plots', id='button_shap', n_clicks=0)
                    ),
                    dbc.Row(
                        html.Br()
                    ),
                    dbc.Row(
                        html.H6('Select feature of SHAP dependence plot:')
                    ),
                    # dependence plots dropdown
                    dbc.Row(
                        dcc.Dropdown(
                            id='dropdown_dep', multi=False, className="dcc_control", style=dict(width='80%')
                        )
                    ),
                    dbc.Row(
                        html.Br()
                    ),
                    dbc.Row(
                        html.H4('SHAP Summary Plot'),
                    ),
                    # click to display summary plot
                    dbc.Row(
                        html.Button('Display Summary', id='button_sum', n_clicks=0)
                    ),
                    dbc.Row(
                        html.Img(id='image1', style={'height':'100%', 'width':'100%'})
                    ),
                    dbc.Row(
                        html.H4('SHAP Decision Plot'),
                    ),
                    # click to display decision plot
                    dbc.Row(
                        html.Button('Display Decision', id='button_dec', n_clicks=0)
                    ),
                    dbc.Row(
                        html.Img(id='image2', style={'height':'100%', 'width':'100%'})
                    ),
                    dbc.Row(
                        html.H4('SHAP Dependence Plot'),
                    ),
                    # click to display dependence plot
                    dbc.Row(
                        html.Button('Display Dependence', id='button_dep', n_clicks=0)
                    ),
                    dbc.Row(
                        html.Img(id='image3', style={'height':'100%', 'width':'100%'})
                    )
                ], width={"size": 4, 'offset':0}
            ) # shap plots end
            ]
        )
    ]
)


# callbacks

# range slider
@app.callback([Output('gain_range', 'max'),
               Output('gain_range', 'value'),
               Output('gain_range', 'marks')],
              [Input('upload_input', 'contents'),
               Input('upload_input', 'filename'),
               Input('upload_model1', 'filename'),
               Input('upload_model2', 'filename'),
               Input('gain_type', 'value')
               ])
def update_slider(contents, filename, filename1, filename2, gaintype):
    if contents is not None:
        if os.path.exists(model_run) == False:
            dfs = predict_gain(contents, filename, filename1, filename2)
        else:
            dfs = gain_pred_file()
        maxval = get_max(dfs, gaintype)
        val = [0, maxval]
        marks = {i: '{}00%'.format(i) for i in range(1, int(math.ceil(maxval)) + 1)}
        return maxval, val, marks
    else:
        return 10, [0,10], {}

# radio -> dropdown circle
@app.callback([Output('dropdown_circle', 'options'),
               Output('dropdown_circle', 'value')],
              [Input('radio_circle', 'value'),
               Input('upload_input', 'contents'),
               Input('upload_input', 'filename'),
               Input('upload_model1', 'filename'),
               Input('upload_model2', 'filename')
               ])
def update_circle(radio, contents, filename, filename1, filename2):
    if contents is not None:
        if os.path.exists(model_run) == False:
            dfs = predict_gain(contents, filename, filename1, filename2)
        else:
            dfs = gain_pred_file()
        options = [{'label': i, 'value': i} for i in dfs['Circle'].unique()]
        if radio == 'all':
            circlelist = dfs['Circle'].unique()
            return options, list(circlelist)
        else:
            return options, []
    else:
        return [], []

# band filter
@app.callback([Output('dropdown_band', 'options'),
               Output('dropdown_band', 'value')],
              [Input('upload_input', 'contents'),
               Input('upload_input', 'filename'),
               Input('upload_model1', 'filename'),
               Input('upload_model2', 'filename')
               ])
def update_band(contents, filename, filename1, filename2):
    if contents is not None:
        if os.path.exists(model_run) == False:
            dfs = predict_gain(contents, filename, filename1, filename2)
        else:
            dfs = gain_pred_file()
        uni = dfs['Band'].unique()
        options = [{'label': i, 'value': i} for i in uni]
        return options, uni[0]
    else:
        return [], ''

# table chart
@app.callback(Output('table_chart','children'),
              [Input('gain_type', 'value'),
               Input('gain_range', 'value'),
               Input('dropdown_circle', 'value'),
               Input('dropdown_band', 'value'),
               Input('inter', 'value'),
               Input('upload_input', 'contents'),
               Input('upload_input', 'filename'),
               Input('upload_model1', 'filename'),
               Input('upload_model2', 'filename')
               ])
def update_table(gain_type, range, circle, band, interference, contents, filename, filename1, filename2):
    if contents is not None:
        if os.path.exists(model_run) == False:
            dfs = predict_gain(contents, filename, filename1, filename2)
        else:
            dfs = gain_pred_file()
        dff = filter_df(dfs, gain_type, range, circle, band, interference)
        name = column_name(gain_type) #reset column name
        dff.columns = name

        table = dash_table.DataTable(
                data=dff.to_dict('rows'),
                # columns=column_name(gain_type),
                columns=[{'name': i, 'id': i} for i in name],
                style_header={'fontWeight': 'bold', 'height': 'auto'},
                style_cell={'fontSize': 13, 'font-family': 'sans-serif',
                            'whiteSpace': 'normal', 'height': 'auto'},
                style_cell_conditional=[{'if': {'column_id': c}, 'textAlign': 'center'} for c in dff.columns],
                page_size=20,
                export_format='csv',
                export_headers='display',
                merge_duplicate_headers=True
            )
        return table

# bar plot
@app.callback(Output('bar_plot','figure'),
              [Input('gain_type', 'value'),
               Input('gain_range', 'value'),
               Input('dropdown_circle', 'value'),
               Input('dropdown_band', 'value'),
               Input('inter', 'value'),
               Input('upload_input', 'contents'),
               Input('upload_input', 'filename'),
               Input('upload_model1', 'filename'),
               Input('upload_model2', 'filename')
               ])
def update_bar(gain_type, range, circle, band, interference, contents, filename, filename1, filename2):
    if contents is not None:
        if os.path.exists(model_run) == False:
            dfs = predict_gain(contents, filename, filename1, filename2)
        else:
            dfs = gain_pred_file()
        dff = filter_df(dfs, gain_type, range, circle, band, interference)
        if gain_type == '_cell_iptgain_weighted_pred':
            fig = px.bar(dff, x="short_name", y=gain_type, labels={'_cell_iptgain_weighted_pred':'IP Tput Gain Prediction'})
        else:
            fig = px.bar(dff, x="short_name", y=gain_type, labels={'_cell_iptgain_weighted_pred':'Downlink Volume Gain Prediction'})
    else:
        dff = {'short_name':[], 'gain_type':[]}
        fig = px.bar(dff, x="short_name", y='gain_type')
    return fig

# dropdown shap
@app.callback([Output('dropdown_shap', 'options'),
               Output('dropdown_shap', 'value')],
              [Input('gain_type', 'value'),
               Input('gain_range', 'value'),
               Input('dropdown_circle', 'value'),
               Input('dropdown_band', 'value'),
               Input('inter', 'value'),
               Input('upload_input', 'contents'),
               Input('upload_input', 'filename'),
               Input('upload_model1', 'filename'),
               Input('upload_model2', 'filename')
               ])
def dropdown_shap(gain_type, range, circle, band, interference, contents, filename, filename1, filename2):
    if contents is not None:
        if os.path.exists(model_run) == False:
            dfs = predict_gain(contents, filename, filename1, filename2)
        else:
            dfs = gain_pred_file()
        dff = filter_df(dfs, gain_type, range, circle, band, interference)
        uni = dff['short_name'].unique()
        options = [{'label': i, 'value': i} for i in uni]
        return options, ''
    else:
        return [], ''

# return selected names in the shap dropdown
@app.callback(Output('return_names', 'children'),
               [Input('dropdown_shap', 'value')])
def return_shap(value):
    if value != []:
        shaplist = value
        return '{}'.format(value)

# button_shap -> generate pngs, dropdown_shap
@app.callback([Output('dropdown_dep', 'options'),
               Output('dropdown_dep', 'value')],
              [Input('upload_input', 'contents'),
               #Input('upload_input', 'filename'),
               Input('upload_model1', 'filename'),
               Input('upload_model2', 'filename'),
               Input('gain_type', 'value'),
               Input('dropdown_shap', 'value'),
               Input('button_shap', 'n_clicks')])
def dropdown_dep(contents, filename1, filename2, gaintype, shaplist, n_clicks): # filename
    if (contents is not None) & (shaplist != []) & (n_clicks != 0):
        empty_png()
        plot_shap(filename1, filename2, gaintype, shaplist)
        deplist1 = []
        list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]

        for i in list_of_images:
            if ('dependence' in i):
                deplist1.append(i)

        options = [{'label': i, 'value': i} for i in deplist1]
        value = deplist1[0]
        return options, value
    else:
        return [], ''

# button sum -> image1
@app.callback(Output('image1', 'src'),
              [Input('upload_input', 'contents'),
               Input('button_sum', 'n_clicks')])
def update_image_dep_src(contents, n_clicks):
     if contents:
         if n_clicks !=0:
             list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
             for i in list_of_images:
                 if ('summary' in i):
                     value = i
             return static_image_route + value

# button dec -> image1
@app.callback(Output('image2', 'src'),
              [Input('upload_input', 'contents'),
               Input('button_dec', 'n_clicks')])
def update_image_dep_src(contents, n_clicks):
     if contents:
         if n_clicks !=0:
             list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
             for i in list_of_images:
                 if ('decision' in i):
                     value = i
             return static_image_route + value

# button dep -> image1
@app.callback(Output('image3', 'src'),
              [Input('upload_input', 'contents'),
               Input('button_sum', 'n_clicks'),
               Input('dropdown_dep', 'value')])
def update_image_dep_src(contents, n_clicks, value):
     if contents:
         if n_clicks !=0:
             return static_image_route + value

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)




if __name__ == '__main__':
    app.run_server(debug=True)                  
