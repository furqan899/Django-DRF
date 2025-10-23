from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "in_stock"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["order", "quantity", "product_name", "product_price", "item_subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(item.item_subtotal for item in obj.items.all())

    class Meta:
        model = Order
        fields = ["order_id", "user", "created_at", "status", "items", "total_price"]


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True, read_only=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
