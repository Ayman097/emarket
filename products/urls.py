from django.urls import path
from . import views

urlpatterns = [
    path('products',  views.products, name='products'),
    path('products/<int:id>',  views.product_detail, name='product'),
    path('products/new',  views.new_product, name='new_product'),
    path('products/edit/<int:id>',  views.edit_product, name='edit_product'),
    path('products/delete/<int:id>',  views.delete_product, name='delete_product'),
    path('products/<int:id>/review',  views.add_review, name='add_review'),
    path('products/<int:id>/dreview',  views.delate_review, name='delate_review'),
]