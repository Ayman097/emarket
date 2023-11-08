from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product
from .serializers import ProductSerializers
from .filters import ProductFilter
from decimal import Decimal
# Create your views here.

@api_view()
def products(request):
    products = Product.objects.all().order_by('id')
    filterset = ProductFilter(request.GET, queryset=products)

    pageNum = 3
    paginator = PageNumberPagination()
    paginator.page_size = pageNum

    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializers(queryset, many=True)

    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializers(product)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializers(data=data)
    
    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializers(product)
        return Response({"product": res.data})
    
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if product.user != request.user:
        return Response({'Error': "You can't Update  this product"}, status=status.HTTP_401_UNAUTHORIZED)
    
    product.name = request.data['name']
    product.descreption = request.data['descreption']
    product.price = Decimal(request.data['price'])
    product.rateings = Decimal(request.data['rateings'])  
    product.category = request.data['category']

    product.save()

    serializer = ProductSerializers(product)

    return Response({"product": serializer.data})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if product.user != request.user:
        return Response({'Error': "You can't Update  this product"}, status=status.HTTP_401_UNAUTHORIZED)

    product.delete()

    return Response({"product": 'Deleted Successfully'})