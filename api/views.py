from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from api.filters import InStockFilter, OrderFilter, ProductFilter
from api.models import Order, Product
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilter,
    ]
    search_fields = ["=name", "description"]
    ordering_fields = ["price", "name"]
    pagination_class = LimitOffsetPagination

    # pagination_class.page_size = 2
    # pagination_class.page_query_param = "page_number"
    # pagination_class.page_size_query_param = "size"
    # pagination_class.max_page_size  = 5

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]


# @api_view(['GET'])
# def product_detail(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found."}, status=404)

#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]


# @api_view(['GET'])
# def order_list(request):
#     order = Order.objects.prefetch_related('items', 'items__product').all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items__product").all()
#     serializer_class = OrderSerializer


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items__product").all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]  # Add appropriate permissions

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)


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
        serializer = self.get_serializer(
            {
                "products": products,
                "count": products.count(),
                "max_price": (
                    max(product.price for product in products) if products else 0
                ),
            }
        )
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        return qs


    @action(
        detail=False,
        methods=["GET"],
        url_path="user-orders",
        permission_classes=[IsAuthenticated],
    )
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
