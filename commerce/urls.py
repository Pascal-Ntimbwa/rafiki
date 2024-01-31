from django.urls import path
from . import views



app_name = 'commerce'



urlpatterns = [
    path('', views.index, name='index'),
    # path('add/', views.add, name='add'),
    # path('cart/', views.cart, name='cart'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('clear/', views.clear, name='clear'),
    # path('remove/', views.remove, name='remove'),
    # path('success/', views.success, name='success'),
    # path('update/', views.update, name='update'),
]