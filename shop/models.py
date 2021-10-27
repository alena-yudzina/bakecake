from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class CakeLevel(models.Model):
    level_num = models.PositiveSmallIntegerField(
        verbose_name='число уровней торта'
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='цена'
    )

    def __str__(self):
        return f'Число уровней: {self.level_num}'


class CakeForm(models.Model):
    type = models.CharField(max_length=100,
                            verbose_name='тип')
    price = models.PositiveSmallIntegerField(
        verbose_name='цена'
    )

    def __str__(self):
        return self.type


class Topping(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='название')
    price = models.PositiveSmallIntegerField(verbose_name='цена')

    def __str__(self):
        return self.name


class Berry(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='название')
    price = models.PositiveSmallIntegerField(verbose_name='цена')

    def __str__(self):
        return self.name


class Decor(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='название')
    price = models.PositiveSmallIntegerField(
        verbose_name='цена'
    )

    def __str__(self):
        return self.name


class Cake(models.Model):
    level = models.ForeignKey(to=CakeLevel,
                              on_delete=models.SET_NULL,
                              null=True,
                              verbose_name='число уровней')
    topping = models.ManyToManyField(to=Topping,
                                     verbose_name='топпинги')
    berry = models.ManyToManyField(to=Berry,
                                   verbose_name='ягоды')
    decor = models.ManyToManyField(to=Decor,
                                   verbose_name='декор')
    caption_on_cake = models.CharField(blank=True,
                                       max_length=200,
                                       verbose_name='надпись на торте')


class Order(models.Model):

    class OrderStatus(models.IntegerChoices):
        IS_PROCESSING = 1, 'Заявка обрабатывается'
        IS_PREPARING = 2, 'Торт готовится'
        ON_THE_WAY = 3, 'Торт в пути'
        DELIVERED = 4, 'Торт доставлен'
        CANCELLED = 5, 'Заказ отменен'

    status = models.PositiveSmallIntegerField(
        db_index=True,
        choices=OrderStatus.choices,
        default=OrderStatus.IS_PROCESSING,
        verbose_name='статус заказа')

    client = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name='клиент')
    cake = models.OneToOneField(to=Cake,
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='торт')
    comment = models.TextField(blank=True,
                               verbose_name='комментарий к заказу')
    destination = models.CharField(max_length=200)
    delivery_time = models.DateTimeField()

    def __str__(self):
        return f'Заказ {self.client.username} на {self.delivery_time}'


class CancellationOrder(models.Model):
    order = models.OneToOneField(to=Order,
                                 on_delete=models.CASCADE,
                                 verbose_name='отмененный заказ')
    comment = models.TextField(blank=True,
                               verbose_name='комментарий пользователя')
