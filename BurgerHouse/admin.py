from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Order, Foydalanuvchi, Category, Product, OrderProduct

# OrderProduct Inline admini
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1  # Yangi qatorda qo'shish imkoniyati

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # Yangi qatorda qo'shish imkoniyati

# Order admini
class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('owner', 'status_icon', 'status_text', 'address')
    search_fields = ('owner__full_name', 'status', 'address')
    list_filter = ('status', 'owner')
    inlines = [OrderProductInline]  # OrderProductni inline qo'shish

    def status_icon(self, obj):
        """Holatga qarab ikonka chiqarish"""
        if obj.status == 'delivered':
            return format_html('<span style="color: green;">✔️</span>')  # Yashil tekshirish belgisi
        elif obj.status == 'waiting':
            return format_html('<span style="color: orange;">⏳</span>')  # Sariq soat belgilari
        elif obj.status == 'received':
            return format_html('<span style="color: blue;">🛍️</span>')  # Moviy paket belgilari
        elif obj.status == 'preparing':
            return format_html('<span style="color: yellow;">🔨</span>')  # Sariq o'zgartirish belgisi
        elif obj.status == 'delivering':
            return format_html('<span style="color: red;">🚚</span>')  # Qizil yuk tashish belgisi
        elif obj.status == 'new':
            return format_html('<span style="color: gray;">🆕</span>')  # Kulrang yangi belgisi
        return "-"

    def status_text(self, obj):
        """Holatni matnli shaklda chiqarish"""
        status_dict = {
            'waiting': 'Kutilmoqda',
            'received': 'Qabul qilindi',
            'preparing': 'Tayyorlanmoqda',
            'delivering': 'Yetkazilmoqda',
            'delivered': 'Yetkazib berildi',
            'new': 'Yangi',
        }
        return status_dict.get(obj.status, "-")

    status_icon.short_description = "Holat Ikonkasi"
    status_text.short_description = "Holat"

# Foydalanuvchi admini
@admin.register(Foydalanuvchi)
class FoydalanuvchiAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('telegram_id', 'full_name', 'username', 'phone_number')

# Kategoriya admini
@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'image')
    inlines = [ProductInline]  # Productni inline qo'shish

# Mahsulot admini
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product_name_uz', 'product_name_ru', 'price', 'status', 'discount', 'category')

# Order modelini ro'yxatdan o'tkazish
admin.site.register(Order, OrderAdmin)