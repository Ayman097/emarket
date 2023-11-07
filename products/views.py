from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers
# Create your views here.

@api_view()
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializers(products, many=True)

    return Response(serializer.data)

