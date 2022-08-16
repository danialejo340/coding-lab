import riskfolio as rp
import numpy as np
import pandas as pd
import yfinance as yf
import warnings


warnings.filterwarnings("ignore")
pd.options.display.float_format = '{:.4%}'.format

# Date range
per, inter = "10y", "1mo"

# Tickers of assets

def optimization(risk_aversion = 1):
    assets =  pd.read_csv('assets.csv', sep=';', index_col=0)
    names = assets['Ticker'].to_list()
    print(names)
    e_returns = assets.ER.to_list()
    assets = assets.Ticker.to_list()

    # Downloading data
    data = yf.download(assets, period=per, interval=inter)
    data = data.loc[:,('Adj Close', slice(None))]
    data.columns = assets
    data.dropna(inplace=True)
    Y = data[assets].pct_change().dropna()

    port = rp.Portfolio(returns=Y, nea=4)

    method_mu='hist' # Method to estimate expected returns based on historical data.
    method_cov='hist' # Method to estimate covariance matrix based on historical data.

    port.assets_stats(method_mu = method_mu, method_cov=method_cov, d=0.94)

    custom_mu = pd.DataFrame({'returns':e_returns}, index=assets).T # retornos esperados
    port.mu = custom_mu/12

    model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
    rm = 'MV' # Risk measure used, this time will be variance
    obj = 'Utility' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
    hist = True # Use historical scenarios for risk measures that depend on scenarios
    rf = 0 # Risk free rate
    l = risk_aversion # Risk aversion factor, only useful when obj is 'Utility'
    end_port = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
    end_port.columns = ['w']

    end_port.loc[:, 'names'] = names
    end_port.loc[:, 'ret'] = port.mu.T.values*12
    end_port.loc[:, 'vol'] = port.cov.values.diagonal()**0.5*(12**0.5)
    print(end_port)
    return end_port


#print(optimization())
