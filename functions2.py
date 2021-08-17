# 8/3/20 Hayung Suh

# get_max, gain_pred_file, column_name, filter_df

# get max
def get_max(mydf):
    ipmax = mydf['_cell_iptgain_weighted_pred'].max()
    volmax = mydf['_cell_dlvolgain_pred'].max()
    maxnum = max(ipmax, volmax)
    return maxnum



def gain_pred_file():
    tempdf = pd.read_csv('gain_pred_result.csv')
    dfs = tempdf[
        ['short_name', 'Region', 'band', 'interference', '_cell_iptgain_weighted_pred', '_cell_dlvolgain_pred']]
    dfs = dfs.rename(columns={'Region': 'Circle', 'band': 'Band'})
    #print(dfs.head())
    return dfs

# update column name
def column_name(gain_type):
    if gain_type == '_cell_iptgain_weighted_pred':
        columns = ['Short name', 'Circle', 'Band', 'Interference', 'IP Tput Gain Prediction']
    else:
        columns = ['Short name', 'Circle', 'Band', 'Interference', 'Downlink Volume Gain Prediction']
    return columns


# filter filter_df
def filter_df(df, gain_type, range, circle, band, interference):

    #gaintype = [gain_type] # global gaintype

    if gain_type == '_cell_iptgain_weighted_pred':
        df = df.drop('_cell_dlvolgain_pred', axis=1)
        df = df.sort_values(by='_cell_iptgain_weighted_pred')
        df['_cell_iptgain_weighted_pred'] = df['_cell_iptgain_weighted_pred'].round(decimals=2)
    else:
        df = df.drop('_cell_iptgain_weighted_pred', axis=1)
        df = df.sort_values(by='_cell_dlvolgain_pred')
        df['_cell_dlvolgain_pred'] = df['_cell_dlvolgain_pred'].round(decimals=2)

    dff = df[
        (df[gain_type] >= range[0]) & (df[gain_type] <= range[1]) &
        df['Circle'].isin(circle) &
        (df['Band']==band)
    ]

    if interference == 'true':
        dff2 = dff[dff['interference'] == True]
    elif interference == 'false':
        dff2 = dff[dff['interference'] == False]
    else:
        dff2 = dff

    return dff2
