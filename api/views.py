from datetime import datetime, timedelta
import requests
from django.http import JsonResponse
import pandas as pd
from .model import Model

def predict(request, symbol):
    interval = request.GET.get('interval')
    end_time = datetime.now()
    if interval == '3m':
        start_time = end_time - timedelta(days=1)
    elif interval == '30m':
        start_time = end_time - timedelta(days=10)
    elif interval == '1h':
        start_time = end_time - timedelta(days=20)
    elif interval == '1d':
        start_time = end_time - timedelta(days=480)
    else:
        return JsonResponse({
            'error': 'Invalid interval parameter'
        })

    end_time_ms = int(end_time.timestamp() * 1000)
    start_time_ms = int(start_time.timestamp() * 1000)

    # Формирование URL запроса
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={start_time_ms}&endTime={end_time_ms}'

    # Выполнение запроса
    response = requests.get(url)
    data = response.json()
    num_cols = ['Open Time', 'Open', 'High', 'Low', 'Close']

    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])[num_cols]
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df.dropna(inplace=True)
    print(df)
    model = Model(df)
    predict = model.prediction.flatten()
    print(predict)
    return JsonResponse({
        'predict': float(predict[0]),  # Преобразуем предсказание в список
    })