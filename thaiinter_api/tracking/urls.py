from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:qr_code_id>/', views.track_roof, name='track_roof'),
    path('<str:qr_code_id>/add_process_name/', views.add_process_name, name='add_process_name'),
]