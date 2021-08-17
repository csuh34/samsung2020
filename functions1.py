# 8/6/20 Hayung Suh
#
# Includes some code by Sujin Jung

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

    # iptp cols
    features = pd.read_csv('ipt_selected_features.csv', header=None)
    ipt_kpi = features.iloc[:, 0].tolist()

    # volume cols
    features = pd.read_csv('vol_selected_features.csv', header=None)
    vol_kpi = features.iloc[:, 0].tolist()

    # load model
    ipt_model = load(filename1)
    dlvol_model = load(filename2)
    grby_cols = ['short_name', '_uebin_left']

    # remove nan rows
    input_dataset = npre_df.copy()

    for train_cols in [ipt_kpi, vol_kpi]:
        input_dataset, train_cols, _ = naCleanser.dropna_by_narate(input_dataset, train_cols, 0.0, axis=0)
        input_dataset, train_cols, _ = naCleanser.dropna_by_narate(input_dataset, train_cols, 0.0, axis=1)

    grby_npre_df = input_dataset.groupby(grby_cols).mean().reset_index().dropna()

    for train_cols in [ipt_kpi, vol_kpi]:
        grby_npre_df.loc[:, train_cols] = grby_npre_df.loc[:, train_cols].applymap(
            lambda x: 9999999999999 if x == np.inf else x)

    grby_npre_df.to_csv('binwise_samples_nan_removed.csv', index=None)

    # predict gain
    predicted = grby_npre_df.copy()
    predicted.loc[:, '_iptratio_pred'] = ipt_model.predict(grby_npre_df.loc[:, ipt_kpi])
    predicted.loc[:, '_pred_post_uebin_dlvol'] = dlvol_model.predict(grby_npre_df.loc[:, vol_kpi])

    # post processing -> calculate gain
    uebinGainer = gainer.UebinGainer(predicted, lookup)
    uebinGainer.cell_iptgain_mean()
    uebinGainer.cell_iptgain_weighted()
    uebinGainer.cell_dlvolgain()

    gainer_report = uebinGainer.report_diff_pred_true()
    gainer_eval = uebinGainer.report_evaluation(['band', 'interference'])

    gainer_report = gainer_report.reset_index()
    gainer_report = gainer_report.merge(lookup[['short_name', 'Region', 'ENBID', 'SAPID', 'band']], how='left',
                                        on='short_name')

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
    # load model
    ipt_model = joblib.load(filename1)
    dlvol_model = joblib.load(filename2)
    # features
    ipt_kpi = pd.read_csv('ipt_selected_features.csv', header=None)
    ipt_kpi = ipt_kpi.iloc[:, 0].tolist()

    vol_kpi = pd.read_csv('vol_selected_features.csv', header=None)
    vol_kpi = vol_kpi.iloc[:, 0].tolist()

    # load bin-wise preprocessed data
    test_df = pd.read_csv('binwise_samples_nan_removed.csv')

    # ipt
    if 'ipt' in gaintype:
        target = 'ipt'
        model = ipt_model
        features = ipt_kpi
    else:
        target = 'vol'
        model = dlvol_model
        features = vol_kpi
    x_test = test_df[features]

    # short name list
    selected_cells = shaplist ## CELL LIST
    print(selected_cells)
    selected_idx = test_df[test_df.short_name.isin(selected_cells)].index

    explainer = shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")
    shap_values = explainer.shap_values(test_df[features])
    print(shap_values.shape, x_test.shape)

    shap.initjs()

    save = 1  # or 1

    newcmp = plt.get_cmap('rainbow')

    return shap_values, selected_idx, x_test, target, explainer, test_df

def summary(shap_values, selected_idx, x_test, target):
    save = 1  # or 1

    newcmp = plt.get_cmap('rainbow')

    # 1. summary plot
    plt.figure()
    shap.summary_plot(shap_values[selected_idx], x_test.iloc[selected_idx], show=False)

    for fc in plt.gcf().get_children():
        for fcc in fc.get_children():
            if hasattr(fcc, "set_cmap"):
                fcc.set_cmap(newcmp)

    if save:
        plt.savefig('png/%s_summary_plot.png' % target, format='png', bbox_inches='tight', facecolor='white')



def decision(explainer, shap_values, selected_idx, test_df, x_test, target):
    save = 1  # or 1

    newcmp = plt.get_cmap('rainbow')

    # 2. decision plot
    plt.figure()
    shap.decision_plot(explainer.expected_value, shap_values[selected_idx],
                       legend_labels=test_df.loc[selected_idx, '_uebin_left'].tolist(),
                       feature_names=x_test.columns.tolist(), show=False, plot_color=newcmp)
    if save:
        plt.savefig('png/%s_decision_plot.png' % target, format='png', bbox_inches='tight', facecolor='white')



def dependence(x_test, selected_idx, shap_values, target):
    save = 1  # or 1

    newcmp = plt.get_cmap('rainbow')

    # 3. dependence plots
    sorted_features = x_test.iloc[selected_idx].columns[np.argsort(-np.mean(np.abs(shap_values[selected_idx]), axis=0))]

    top_n = len(sorted_features)

    kpi = sorted_features[5]

    i = 0
    for kpi in sorted_features[:top_n]:

        i += 1
        print(kpi)
        plt.figure()
        shap.dependence_plot(kpi, shap_values[selected_idx], x_test.iloc[selected_idx], show=False)

        # Change the colormap of the artists
        for fc in plt.gcf().get_children():
            for fcc in fc.get_children():
                if hasattr(fcc, "set_cmap"):
                    fcc.set_cmap(newcmp)

        # plt.title(kpi, size=10)
        plt.xlabel(kpi, fontsize=10)
        plt.ylabel('SHAP value', fontsize=10)
        plt.axhline(y=0)
        if save:
            plt.savefig('png/%s_dependence_plot_%d_%s.png' % (target, i, kpi), format='png', bbox_inches='tight',
                        facecolor='white')
