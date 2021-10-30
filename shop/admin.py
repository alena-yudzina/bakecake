from django.contrib import admin
from django.db.models import Count
from django.http.response import HttpResponse

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
                     CancellationOrder,
                     PromoCode])

import csv

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow(
                [getattr(obj, field) for field in field_names]
        )

        return response
    
    export_as_csv.short_description = "Export Selected"
