import pandas as pd
import numpy as np
import os
# tickers = ['SBER', 'GAZP', 'LKOH', 'ROSN', 'YDEX', 'MGNT', 'NLMK', 'GMKN', 'VTBR', 'PLZL']

tickers = ['SBER', 'VTBR', 'GAZP', 'LKOH', 'ROSN',
    'NLMK', 'GMKN', 'MGNT', 'YDEX', 'PLZL',
    'TATN', 'SNGS', 'SNGSP',
    'CHMF', 'MAGN', 'ALRS', 'RASP',
    'MOEX', 'BSPB',
    'IRAO', 'FEES', 'HYDR',
    'LENT', 'MVID', 'FIXR', 'BELU',
    'MTSS', 'RTKM', 'RTKMP',
    'PHOR', 'AKRN', 'KZOS',
    'AFLT', 'URAL', 'TRMK', 'KMAZ',
    'PIKK', 'LSRG', 'SMLT',
    'LIFE', 'APTK',
    'AFKS', 'CNRU', 'OZON',
    'ENPG', 'BANE', 'TRNFP',
    'T', 'SELG', 'ASTR']

data_folder = 'C:/Users/User/Desktop/курсовая/акции'
prices_dict = {}

for ticker in tickers:
    filename = f'{ticker}_250101_260101.csv'
    filepath = os.path.join(data_folder, filename)

    if os.path.exists(filepath):
        df = pd.read_csv(filepath, sep=';')
        df['<DATE>'] = pd.to_datetime(df['<DATE>'], format='%y%m%d')

        df = df.set_index('<DATE>')
        prices_dict[ticker] = df['<CLOSE>']


prices = pd.DataFrame(prices_dict)
returns = np.log(prices / prices.shift(1)).dropna(how='all')

corr_pearson = returns.corr(method='pearson')
corr_spearman = returns.corr(method='spearman')
corr_kendall = returns.corr(method='kendall')

corr_pearson.to_csv('correlation_pearson.csv')
corr_spearman.to_csv('correlation_spearman.csv')
corr_kendall.to_csv('correlation_kendall.csv')