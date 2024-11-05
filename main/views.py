from django.http import JsonResponse
from django.shortcuts import render

def main(request):
    return JsonResponse({'status':'ok'})