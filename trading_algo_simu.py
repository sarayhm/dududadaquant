import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from dotenv import load_dotenv
# Importing hidden API Key.
load_dotenv()
api_key = os.getenv("API_KEY")



ts = TimeSeries(key = api_key, output_format = "pandas")
data, meta_data = ts.get_intraday(symbol='MSFT',interval='60min', outputsize='full')

print(data.head(100))