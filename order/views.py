from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from products.models import Product

# Create your views here.

@api_view()
@permission_classes([IsAuthenticated, IsAdminUser])
def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)

    return Response({"data": serializer.data})

@api_view()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_order(request, id):
    order = get_object_or_404(Order, pk=id)
    serializer = OrderSerializer(order)

    return Response({"data": serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_order(request, id):
    order = get_object_or_404(Order, pk=id)
    order.status = request.data['status']
    order.save()
    serializer = OrderSerializer(order)

    return Response({"data": serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_order(request, id):
    order = get_object_or_404(Order, pk=id)
    order.delete()
    

    return Response({"data": "Order Deleted"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    order_items = data['order_items']

    if len(order_items) == 0:
        return Response({'error': 'No recived any Order'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum(item['price'] * item['quantity'] for item in order_items)
        order = Order.objects.create(
            user = user,
            city = data['city'],
            zip_code = data['zip_code'],
            street = data['street'],
            state = data['state'],
            country = data['country'],
            phone_no = data['phone_no'],
            total_amount = total_amount
        )
        for o in order_items:
            product = Product.objects.get(id=o['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = o['quantity'],
                price = o['price']
            )
            product.stock -= item.quantity
            product.save()
        
        serializer = OrderSerializer(order)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

