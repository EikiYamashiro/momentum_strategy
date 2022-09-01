"""
Collect data from yahoo and plot
"""
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import requests
import matplotlib.pyplot as plt


Url:vars = "https://finance.yahoo.com/quote/%5EBVSP/components?p=%5EBVSP"

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(Url, headers=header,timeout=10)
table = pd.read_html(r.text)[0]
tickers = table["Symbol"].tolist()

del tickers[28]

start_day = (datetime.today() - timedelta(days=3650)).strftime('%Y-%m-%d')
end_day = datetime.today().strftime('%Y-%m-%d')
df = yf.download(tickers,
                start = start_day,
                end = end_day)["Adj Close"]
print("Data início: ",start_day, "\nData fim: ", end_day)

df.index = pd.to_datetime(df.index)

# %%
plt.figure(figsize=(16,8))
plt.title("Adj. Close Price")
plt.xlabel("Date")
plt.ylabel("US$ Price")
plt.plot(df)
plt.legend(df.columns,loc='upper right')
plt.show()
