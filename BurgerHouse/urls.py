from django.urls import path
from . import views
from .views import CategoryList, ProductList, OrderList, ProductsByCategory, RegisterUser, NotificationAPIView, ProductRetrieve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Burger House API Hujjatlari",
        default_version='v1',
        description="Burger House loyihasi uchun API hujjatlari",
        contact=openapi.Contact(email="sharqonateamlc@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieve.as_view(), name='product-retrieve'),
    path('category/<int:category_id>/', ProductsByCategory.as_view(), name='products-by-category'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notification/', NotificationAPIView.as_view(), name='notification'),
    path('orders/', views.create_order, name='create_order'),  # create_order ishlatilmoqda
    # path('orders/', OrderList.as_view(), name='order-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

