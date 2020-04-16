
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('site/<int:site_id>/', views.site, name='site'),
    path('building/<int:building_id>/', views.building, name='building'),
]
