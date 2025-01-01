from django.apps import AppConfig

class BurgerhouseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "BurgerHouse"
    
    # def ready(self):
    #     import BurgerHouse.signals  # signals.py faylini import qilish
