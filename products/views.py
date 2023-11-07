from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializers
from .filters import ProductFilter
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

