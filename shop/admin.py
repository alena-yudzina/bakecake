from django.contrib import admin

from django.db.models import Count
from django.http.response import HttpResponse

from django.template.response import TemplateResponse

from my_stat import models

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

import collections

@admin.register(models.MyStat)
class MyStatAdmin(admin.ModelAdmin):
    # list_display = ('upper_case_name',)
    change_list_template = 'admin/bakecake_statistics.html'

    def get_model_perms(self, request):
        return {'view': True}

    # def changelist_view(self, request):
        # context = {
        #     'orders': self.model.objects.count(),
        # }
        # return TemplateResponse(request, self.change_list_template, context)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        statuses = collections.Counter(
                order.get_status_display() for order in Order.objects.only('status')
            ).items()

        response.context_data['summary'] = {
            'orders': self.model.objects.count(),
            'statuses': statuses,
            'clients': self.model.client.field.related_model.objects.filter(
                is_staff=False
            ).count(),
            'topping': dict(
                Cake.objects.values_list('topping__name').annotate(total=Count('id'))
            )
        }

        return response

    

    # def upper_case_name(self, obj):
    #     return self.model.objects.all().count()
    # upper_case_name.short_description = 'Всего заказов'



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
