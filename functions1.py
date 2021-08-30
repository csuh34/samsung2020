# 8/6/20 Hayung Suh
#
# Some code deleted due to confidentiality

# empty_png, plot_shap, predict_gain

import dash_html_components as html
import glob
import os
import pathlib
import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from modules import cleanser
from modules import gainer
from joblib import dump, load

import base64
import io

# predict gain - uses input file, model 1 & 2
def predict_gain(contents, filename, filename1, filename2):
    naCleanser = cleanser.BaseDataCleanser()
    naCleanser.debugprt(1)
    # Load Data
    contents = contents[0]
    filename = filename[0]
    npre_df = input_parse_contents(contents, filename)

    lookup = pd.read_csv('lookup_v7.csv')  # cell 정보

    ###
    #
    # deleted
    #
    ###
    
    # save result file
    gainer_report.to_csv('gain_pred_result.csv')

    tempdf = pd.read_csv('gain_pred_result.csv')
    dfs = tempdf[['short_name', 'Region', 'band', 'interference', '_cell_iptgain_weighted_pred', '_cell_dlvolgain_pred']]
    dfs = dfs.rename(columns={'Region': 'Circle', 'band': 'Band'})
    return dfs

# input file into df
def input_parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_feather(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

# empty png directory before updateing shap value plots
def empty_png():
    mypath = str(pathlib.Path('__file__').parent.absolute())
    image_directory = mypath + '/png/'
    for f in glob.glob('{}*.png'.format(image_directory)):
        os.remove(f)

def plot_shap(filename1, filename2, gaintype, shaplist):
    
    ###
    #
    # deleted
    #
    ###

    return shap_values, selected_idx, x_test, target, explainer, test_df

def summary(shap_values, selected_idx, x_test, target):
    save = 1  # or 1

    newcmp = plt.get_cmap('rainbow')

    # 1. summary plot
    ###
    #
    # deleted
    #
    ###

def decision(explainer, shap_values, selected_idx, test_df, x_test, target):
    save = 1  # or 1

    newcmp = plt.get_cmap('rainbow')

    # 2. decision plot
    ###
    #
    # deleted
    #
    ###

def dependence(x_test, selected_idx, shap_values, target):
    save = 1  # or 1

    newcmp = plt.get_cmap('rainbow')

    # 3. dependence plots
    
    ###
    #
    # deleted
    #
    ###
