from django.contrib import admin

from .models import (
    CakeLevel,
    CakeForm,
    Topping,
    Berry,
    Decor,
    Cake,
    Order,
    CancellationOrder,
    PromoCode
)


admin.site.register([CakeLevel,
                     CakeForm,
                     Topping,
                     Berry,
                     Decor,
                     Cake,
                     Order,
                     CancellationOrder,
                     PromoCode])
