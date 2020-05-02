'''URL / routing definition for the `loc` application.'''

from django.urls import path

from . import views

app_name = 'loc'

urlpatterns = [
    path('', views.index, name='index'),
    path('plan/view/<int:pk>/', views.plan_details, name='plan'),
    path('plan/edit_meta/<int:pk>/', views.plan_edit_meta, name='plan_edit_meta'),
    path('plan/<int:pk>/add_tp/', views.plan_add_teleport, name='plan_add_tp'),
    path('search', views.search, name='search'),
]
