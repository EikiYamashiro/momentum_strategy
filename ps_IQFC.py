# %%
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import numpy as np
from dateutil.relativedelta import relativedelta

# %%
import requests

url = "https://finance.yahoo.com/quote/%5EBVSP/components?p=%5EBVSP"

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)
table = pd.read_html(r.text)[0]
tickers = table["Symbol"].tolist()
tickers

# %%
del tickers[28]

# %%

start_day = (datetime.today() - timedelta(days=3650)).strftime('%Y-%m-%d')
end_day = datetime.today().strftime('%Y-%m-%d')
df = yf.download(tickers_,
                start = start_day,
                end = end_day)["Adj Close"]
print("Data início: ",start_day, "\nData fim: ", end_day)

# %%
df

# %%
df.index = pd.to_datetime(df.index)

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(16,8))
plt.title("Adj. Close Price")
plt.xlabel("Date")
plt.ylabel("US$ Price")
plt.plot(df)
plt.legend(df.columns,loc='upper right')
plt.show()

# %%
mtl_ret = df.pct_change().resample('M').agg(lambda x: (x+1).prod() - 1)

# %%
mtl_ret

# %%
past11 = (mtl_ret+1).rolling(12).apply(np.prod)-1
past11

# %%
def momentum(i):
    end_measurement = past11.index[i-1]
    ret_12 = past11.loc[end_measurement]
    ret_12 = ret_12.reset_index()
    ret_12['decile'] = pd.qcut(ret_12.iloc[:,1], 10, labels=False, duplicates='drop')
    winners = ret_12[ret_12.decile == 9]
    loosers = ret_12[ret_12.decile == 0]
    winnerret = mtl_ret.loc[past11.index[i], mtl_ret.columns.isin(winners['index'])]
    looserret = mtl_ret.loc[past11.index[i], mtl_ret.columns.isin(loosers['index'])]
    Momentumprofit = winnerret.mean() - looserret.mean()
    return Momentumprofit

# %%

profits = []
dates = []
for i in range(120):
    profits.append(momentum(i))
    dates.append(past11.index[i])

# %%
bvsp = yf.download('^BVSP',
                start = start_day,
                end = end_day)["Adj Close"]
print("Data início: ",start_day, "\nData fim: ", end_day)

# %%
bvsp_ret = bvsp.pct_change().resample('M').agg(lambda x: (x+1).prod() - 1)

# %%
frame = pd.DataFrame()
frame["Model"] = profits
frame["BVSP"] = bvsp_ret.values
frame["excess"] = frame.iloc[:,0] - frame.iloc[:,1]
frame["outperformed"] = ["Yes" if i>0 else "No" for i in frame.excess]

# %%
frame[frame.outperformed == "Yes"].shape

# %%
frame[frame.outperformed == "No"].shape

# %%
plt.style.use("dark_background")
plt.figure(figsize=(10,10))
plt.plot(dates, frame["Model"], color="#ED3237")
plt.plot(dates, frame["BVSP"], color="#FEF0F0")
plt.title("Retorno da Estratégia")
plt.legend(["Model", "BVSP"])


# %%
60/121

# %%
frame["Model"].corr(frame["BVSP"], method='pearson')

# %%
Sharpe_Ratio = frame["Model"].mean() / frame["Model"].std()
Sharpe_Ratio

# %%
frame['cumluative_return'] = np.exp(np.log1p(new_frame['Model']).cumsum())
frame['cumluative_return_bvsp'] = np.exp(np.log1p(new_frame['BVSP']).cumsum())

# %%
frame

# %%



