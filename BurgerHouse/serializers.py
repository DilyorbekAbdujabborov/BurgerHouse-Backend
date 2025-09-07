from rest_framework import serializers
from core.settings import APP_URL
from .models import Category, Product, Order, OrderProduct, Foydalanuvchi

class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name_uz', 'product_name_ru', 'product_image', 'price', 'status', 'discount']

    def get_product_image(self, obj):
        request = self.context.get('request')
        if obj.product_image and request:
            return request.build_absolute_uri(obj.product_image.url)
        return f"{APP_URL}{obj.product_image.url}"

class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Foydalanuvchi.objects.all())
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Order
        fields = ['owner', 'products', 'address', 'additional_phone', 'note', 'latitude', 'longitude', 'status']

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return f"{APP_URL}{obj.image.url}"
        return None

class FoydalanuvchiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'order_count']