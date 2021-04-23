from SII_API import views
from django.urls import path



urlpatterns = [
    path('sensors/', views.sensors),
    path('sensor/id/', views.sensors_id),
    path('alerts/', views.alerts),
    path('sensor/id/alerts/', views.sensors_id_alerts),
    path('newdata/', views.new_data),
]