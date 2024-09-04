from django.urls import path
from . import views

urlpatterns = [
    path('', views.calcular_economia, name='consumer_list'),
    path('create/', views.create_consumer, name='create_consumer'),
    path('import-consumers/', views.import_consumers, name='import_consumers'),
]
