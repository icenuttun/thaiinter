from django.urls import path
from . import views

app_name = 'qrcodes'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_roof, name='add_roof'),
    path('add/roof_color/', views.add_roof_color, name='add_roof_color'),
    path('add/roof_type/', views.add_roof_type, name='add_roof_type'),
    path('add/roof_size/', views.add_roof_size, name='add_roof_size'),
    path('<int:roof_id>/', views.roof_detail, name='roof_detail'),
    path('<uuid:qr_code_id>/', views.qr_code_detail, name='qr_code_detail'),
    path('print/<str:qr_code_id>/', views.print_qr_code, name='print_qr_code'),
    path('download_and_redirect/<str:qr_code_id>/', views.download_and_redirect, name='download_and_redirect'),
]