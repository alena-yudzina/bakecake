from shop.models import Order


class MyStat(Order):
    class Meta:
        proxy = True
        verbose_name_plural = 'Статистика'
