from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Review
from .serializers import ProductSerializers
from .filters import ProductFilter
from decimal import Decimal
from django.db.models import Avg
# Create your views here.

@api_view()
def products(request):
    products = Product.objects.all().order_by('id')
    filterset = ProductFilter(request.GET, queryset=products)

    pageNum = 10
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, id):
    user = request.user
    product = get_object_or_404(Product, pk=id) 
    data = request.data
    review = product.reviews.filter(user=user)
    
    # To Ensure user give rate between 1 : 5
    if data['rating'] <= 0 or data['rating'] >= 6:
        return Response({'Error': "Please Rate between 1 to 5"}, status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review = {'rating': data['rating'], 'comment': data['comment']}
        review.update(**new_review)

        # Calculate Avg Rating for product
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.rateings = rating['avg_ratings']
        product.save()
        return Response({'details': 'Review Updated Successfully'}, status=status.HTTP_200_OK)
    else:
        Review.objects.create(
            product = product,
            user = user,
            comment = data['comment'],
            rating = data['rating']   
        )
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.rateings = rating['avg_ratings']
        product.save()
        return Response({'details': 'Review Created Successfully'}, status=status.HTTP_200_OK)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delate_review(request, id):
    user = request.user
    product = get_object_or_404(Product, pk=id) 
    review = product.reviews.filter(user=user)

    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
            product.rateings = rating['avg_ratings']
            product.save()
            return Response({'details': 'Review Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'you are not authrized to delete this review'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Review Not found'}, status=status.HTTP_400_BAD_REQUEST)