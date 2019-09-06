from django.urls import path

from . import views
app_name = 'vouchers'
urlpatterns = [
    path('', views.index, name='index'),
    path('consume', views.consume, name='consume'),
    path('success/<str:voucher_code>', views.success, name='success'),
    path('error/<int:error_code>', views.error, name='error')
]