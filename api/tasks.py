import time

from celery import shared_task
from django.http import JsonResponse

from .model import Model
import pandas as pd

@shared_task
def train_model(data):
    num_cols = ['Open Time', 'Open', 'High', 'Low', 'Close']

    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                     'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                     'Taker Buy Quote Asset Volume', 'Ignore'])[num_cols]
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df.dropna(inplace=True)
    time.sleep(10)
    model = Model(df)
    data = {
        'Open': model.prediction.flatten().tolist()[0],
        'High': model.prediction.flatten().tolist()[1],
        'Low': model.prediction.flatten().tolist()[2],
        'Close': model.prediction.flatten().tolist()[3],
    }
    return data


