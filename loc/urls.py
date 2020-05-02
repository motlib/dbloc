'''URL / routing definition for the `loc` application.'''

from django.urls import path

from . import views

app_name = 'loc'

urlpatterns = [
    path('', views.PlanIndexView.as_view(), name='index'),
    path('plan/<int:pk>/', views.PlanDetailView.as_view(), name='plan'),
    path('plan/<int:pk>/edit_meta/', views.plan_edit_meta, name='plan_edit_meta'),
    path('plan/<int:pk>/add_tp/', views.plan_add_teleport, name='plan_add_tp'),
    path('search/', views.search, name='search'),
    path('info/', views.info, name='info'),
]
