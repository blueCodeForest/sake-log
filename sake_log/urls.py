from django.urls import path
from . import views

app_name= 'sake_log'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('edit/<int:pk>/', views.EditDrink.as_view(), name='edit'),
    path('create', views.CreateDrink.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteDrink.as_view(), name='delete'),
    path('count-up', views.count_up, name='count_up'),
    path('count-down', views.count_down, name='count_down'),
    path('status', views.change_status, name='change_status'),
    path('graph', views.DrankAlcoholView.as_view(), name='graph'),
    # path('drank', views.DrankAlcoholView.as_view(), name='drank_list'),
]