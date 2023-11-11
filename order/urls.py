from django.urls import path
from . import views

urlpatterns = [
    path('orders/new',  views.new_order, name='new_order'),
    path('orders/',  views.list_orders, name='list_orders'),
    path('orders/<int:id>',  views.get_order, name='get_order'),
    path('orders/<int:id>/proccess',  views.update_order, name='update_order'),
    path('orders/<int:id>/delete',  views.delete_order, name='delete_order'),
]