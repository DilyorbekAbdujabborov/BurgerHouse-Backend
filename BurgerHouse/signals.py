from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderProduct
from .utils import send_telegram_message, send_telegram_location
from core.settings import WORK_GROP_ID

# Buyurtma haqida xabar matnini yaratish
def create_order_message(order):
    products_info = []
    total_count = 0

    for order_product in order.order_products.all():
        products_info.append(f"{order_product.product.product_name_uz} - {order_product.order_count} ta")
        total_count += order_product.order_count

    message = (
        f"Buyurtma ID: {order.id}\n"
        f"Manzil: {order.address if order.address else 'Manzil ko\'rsatilmagan'}\n"
        f"Buyurtma holati: {order.get_status_display()}\n"
        f"Mahsulotlar:\n"
        f"{chr(10).join(products_info)}\n"
        f"Jami mahsulotlar soni: {total_count} ta\n"
    )
    return message

# Yangi buyurtma holati o'zgarganda signal
@receiver(post_save, sender=Order)
def send_order_status_update(sender, instance, created, **kwargs):
    if created:
        message = create_order_message(instance)
        send_telegram_message(WORK_GROP_ID, message)
        if instance.latitude and instance.longitude:
            send_telegram_location(WORK_GROP_ID, instance.latitude, instance.longitude)
    else:
        message = f"Buyurtma holati yangilandi!\nBuyurtma ID: {instance.id}\n" \
                  f"Yangi holat: {instance.get_status_display()}"
        send_telegram_message(WORK_GROP_ID, message)
        if instance.latitude and instance.longitude:
            send_telegram_location(WORK_GROP_ID, instance.latitude, instance.longitude)