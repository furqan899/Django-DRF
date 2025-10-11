from rest_framework.response import Response
from api.models import Product, Order
from api.serializers import ProductInfoSerializer, ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer

# @api_view(['GET'])
# def product_detail(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found."}, status=404)
    
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

# @api_view(['GET'])
# def order_list(request):
#     order = Order.objects.prefetch_related('items', 'items__product').all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    
    
# @api_view(['GET'])
# def product_detail(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#                                         "products": products,
#         "count": products.count(),
#         "max_price": max(product.price for product in products) if products else 0
#     })
#     return Response(serializer.data)

class ProductDetailInfoAPIView(APIView):
    serializer_class = ProductInfoSerializer

    def get(self, request):
        products = Product.objects.all()
        serializer = self.get_serializer({
            "products": products,
            "count": products.count(),
            "max_price": max(product.price for product in products) if products else 0
        })
        return Response(serializer.data)