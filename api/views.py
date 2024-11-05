from datetime import datetime, timedelta
import requests
from django.http import JsonResponse
import pandas as pd
from .tasks import train_model
from celery.result import AsyncResult


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


    prediction_task = train_model.delay(data)

    return JsonResponse({'status': 'training started', 'task_id': prediction_task.id})


def result(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == 'PENDING':
        return JsonResponse({
            'status': 'training',
        })
    elif task_result.state == 'SUCCESS':
        return JsonResponse({
            'status': 'success',
            'result': task_result.result,
        })
    else:
        return JsonResponse({
            'status': 'unsuccessful',
            'error': str(task_result.info)
        })