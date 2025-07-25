from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.view_calendar, name='view_calendar'),
    path('api/create_slot_rule/', views.create_slot_rule, name='create_slot_rule'),
    path('api/delete_slot_rule/<int:slot_rule_id>/', views.delete_slot_rule, name='delete_slot_rule'),
]
