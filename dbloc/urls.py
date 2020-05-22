'''URL / routing definition for the `loc` application.'''

from django.urls import path

from . import views

app_name = 'dbloc'

urlpatterns = [
    path('', views.PlanIndexView.as_view(), name='index'),
    path('plan/<int:pk>/', views.PlanDetailView.as_view(), name='plan'),
    path('plan/<int:pk>/edit_meta/', views.PlanMetaEdit.as_view(), name='plan_edit_meta'),
    path('plan/<int:pk>/add_tp/', views.plan_add_teleport, name='plan_add_tp'),
    path('plan/<int:pk>/select_tp/<str:tp_action>', views.plan_select_tp, name='plan_select_tp'),

    path('tp/<int:pk>/edit/', views.tp_edit, name='tp_edit'),
    path('tp/<int:pk>/delete/', views.tp_delete, name='tp_delete'),
    path('tp/<int:pk>/follow/', views.tp_follow, name='tp_follow'),


    path('search/', views.search, name='search'),

    path('info/', views.info, name='info'),
]
