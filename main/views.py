from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def main(request):
    coins = settings.COINS
    return render(request, 'main/index.html', {'coins': coins})

def coin_view(request, coin):
    end_time = datetime.now()
    time = request.GET   ['time'] or None
    if time == None or time == '7d':
        interval = '30m'
        start_time = end_time - timedelta(days=7)
    elif time == '1d':
        interval = '3m'
        start_time = end_time - timedelta(days=1)
    elif time == '20d':
        interval = '1h'
        start_time = end_time - timedelta(days=20)
    else:
        return JsonResponse({'error': 'Invalid time'})

    symbol = coin    + 'USDT'
    end_time_ms = int(end_time.timestamp() * 1000)
    start_time_ms = int(start_time.timestamp() * 1000)

    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={start_time_ms}&endTime={end_time_ms}'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        timestamps = [entry[0] for entry in data]
        close_prices = [float(entry[4]) for entry in data]

        dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, close_prices, marker='o', linestyle='-', color='b', label='Цена закрытия')
        plt.xlabel('Дата и время')
        plt.ylabel('Цена закрытия (USDT)')
        plt.title('График цены закрытия')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()


        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Конвертация в Base64
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        return render(request, 'main/coin_page.html', {'coin': coin, 'image_base64': image_base64, 'time':'1d'})
    return JsonResponse({'error': 'Coin not found'})