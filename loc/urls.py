
from django.urls import path

from . import views

app_name = 'loc'

urlpatterns = [
    path('', views.index, name='index'),
    path('site/<int:site_id>/', views.site, name='site'),
    path('building/<int:building_id>/', views.building, name='building'),
    path('floor/<int:floor_id>/', views.floor, name='floor'),
]
