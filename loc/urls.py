
from django.urls import path

from . import views

app_name = 'loc'

urlpatterns = [
    path('', views.index, name='index'),
    path('site/view/<int:pk>/', views.site, name='site'),
    path('site/edit_meta/<int:pk>/', views.site_edit_meta, name='site_edit_meta'),

    path('building/view/<int:pk>/', views.building, name='building'),
    path('building/edit_meta/<int:pk>/', views.building_edit_meta, name='building_edit_meta'),

    path('floor/view/<int:pk>/', views.floor, name='floor'),
]
