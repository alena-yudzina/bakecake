from django.contrib import admin
from django.db.models import Count

from .models import (
    CakeLevel,
    CakeForm,
    Topping,
    Berry,
    Decor,
    Cake,
    Order,
    CancellationOrder,
    PromoCode,
    OrderSummary,
    CancellationOrderSummary
)

@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/order_summary_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        response.context_data['summary'] = (Order.objects
            .values('status')
            .annotate(total=Count('status'))
        )

        return response


@admin.register(CancellationOrderSummary)
class CancellationOrderSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/cancellation_order_summary_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        response.context_data['summary'] = {
            'orders': Order.objects.count,
            'cancelled_orders': CancellationOrder.objects.count
        }

        return response


admin.site.register([CakeLevel,
                     CakeForm,
                     Topping,
                     Berry,
                     Decor,
                     Cake,
                     Order,
                     CancellationOrder,
                     PromoCode])
