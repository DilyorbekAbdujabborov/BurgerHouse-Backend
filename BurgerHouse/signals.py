from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderProduct
from .utils import send_telegram_message, send_telegram_location
from core.settings import WORK_GROP_ID

# Buyurtma haqida xabar matnini yaratish
def create_order_message(order):
    products_info = []
    total_count = 0

    # OrderProductlar bo'yicha mahsulotlarni olish
    for order_product in order.order_products.all():  # 'order_products' orqali bog'langan mahsulotlarni olish
        products_info.append(f"{order_product.product.product_name_uz} - {order_product.order_count} ta")
        total_count += order_product.order_count

    # Buyurtma haqida xabar matnini yaratish
    message = (
        f"Buyurtma ID: {order.id}\n"
        f"Manzil: {order.address.full_address if order.address else 'Manzil ko\'rsatilmagan'}\n"
        f"Buyurtma holati: {order.status}\n"
        f"Mahsulotlar:\n"
        f"{chr(10).join(products_info)}\n"
        f"Jami mahsulotlar soni: {total_count} ta\n"
    )
    return message

# Yangi buyurtma holati o'zgarganda signal
@receiver(post_save, sender=Order)
def send_order_status_update(sender, instance, created, **kwargs):
    if created:  # Yangi buyurtma yaratildi
        # WORK_GROP_ID ga buyurtma ma'lumotlarini yuborish
        message = create_order_message(instance)  # Buyurtma haqida xabar yaratish
        send_telegram_message(WORK_GROP_ID, message)  # WORK_GROP_ID ga xabar yuborish

        # Manzil mavjud bo'lsa, lokatsiya yuborish
        if instance.address:
            send_telegram_location(WORK_GROP_ID, instance.address.latitude, instance.address.longitude)  # Lokatsiya yuborish

    else:  # Buyurtma holati o'zgarganda
        # ORDER holati o'zgarganda xabar yuborish
        message = f"Buyurtma holati yangilandi!\nBuyurtma ID: {instance.id}\n" \
                  f"Yangi holat: {instance.get_status_display()}"
        send_telegram_message(WORK_GROP_ID, message)
        # Lokatsiyani yuborish, agar manzil bo'lsa
        if instance.address:
            send_telegram_location(WORK_GROP_ID, instance.address.latitude, instance.address.longitude)  # Lokatsiya yuborish
