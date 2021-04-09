from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test-django'),
    path('sensors/', views.sensors, name='sensors'),
]