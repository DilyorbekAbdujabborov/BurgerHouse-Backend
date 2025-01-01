from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Category, Product, Order, Foydalanuvchi
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, FoydalanuvchiSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.decorators import api_view
from django.http import JsonResponse

class OrderList(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_order(request):
    data = request.data

    telegram_id = data.get('owner')
    try:
        owner = Foydalanuvchi.objects.get(telegram_id=telegram_id)
    except Foydalanuvchi.DoesNotExist:
        return JsonResponse({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

    products_data = data.get('products', [])
    products = []
    for product_data in products_data:
        try:
            product = Product.objects.get(id=product_data['product_id'])
            products.append(product)
        except Product.DoesNotExist:
            return JsonResponse({"detail": f"Mahsulot {product_data['product_id']} topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

    additional_phone = data.get('additional_phone', '')
    note = data.get('note', '')
    latitude = data.get('latitude', 0.0)
    longitude = data.get('longitude', 0.0)
    address =  data.get('address', '')
    status_order = data.get('status', 'new')

    order = Order.objects.create(
        owner=owner,
        additional_phone=additional_phone,
        note=note,
        latitude=latitude,
        longitude=longitude,
        status=status_order,
        address=address
    )
    order.products.set(products)
    order.save()

    return JsonResponse({
        "id": order.id,
        "owner": order.owner.telegram_id,
        "address": order.address,
        "status": order.status,
        "additional_phone": order.additional_phone,
    }, status=status.HTTP_201_CREATED)


class CustomRefreshToken(RefreshToken):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['telegram_id'] = user.telegram_id

    @classmethod
    def for_user(cls, user):
        token = cls(user)
        return token

class ProductRetrieve(APIView):
    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

class NotificationAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            waiting_orders = Order.objects.filter(status='Waiting')
            serializer = OrderSerializer(waiting_orders, many=True)
            return Response({
                'message': "Waiting buyurtmalar ro'yxati",
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except InvalidToken:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterUser(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        username = request.data.get('username')
        phone_number = request.data.get('phone_number')
        telegram_id = request.data.get('telegram_id')

        if not full_name or not username:
            return Response({"detail": "Ism va username kiriting."}, status=status.HTTP_400_BAD_REQUEST)

        if Foydalanuvchi.objects.filter(username=username).exists():
            return Response({"detail": "Bu username allaqachon mavjud."}, status=status.HTTP_409_CONFLICT)

        if phone_number and Foydalanuvchi.objects.filter(phone_number=phone_number).exists():
            return Response({"detail": "Bu telefon raqami allaqachon ro'yxatdan o'tgan."}, status=status.HTTP_400_BAD_REQUEST)

        user = Foydalanuvchi.objects.create(
            full_name=full_name,
            telegram_id=telegram_id,
            username=username,
            phone_number=phone_number
        )

        serializer = FoydalanuvchiSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductsByCategory(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"detail": "Kategoriya topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(category=category)
        if not products.exists():
            return Response({"detail": "Ushbu kategoriya uchun mahsulotlar topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        if not categories.exists():
            return Response({"detail": "Kategoriya topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        if not products.exists():
            return Response({"detail": "Mahsulotlar topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
