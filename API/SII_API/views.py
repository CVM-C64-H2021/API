from django.shortcuts import render
from django.http import HttpResponse
# from brooker.brooker_apiv1 import *
# Create your views here.

def getSensorJSon():
    sensor_data = [{
        'data1':'data1',
        'data2':'data2',
        'data3':'data3',
        'data4':'data4',
    }]
    return sensor_data

def test (request):
    return HttpResponse('<h1>HELLO WORLD!</h1>')

def sensors(request):
    ctx = {
        'datas': getSensorJSon()
    }
    return render(request, 'SII_API/sensors.html', ctx)