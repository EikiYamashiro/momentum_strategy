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
df = yf.download(tickers,
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