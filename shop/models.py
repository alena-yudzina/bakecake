from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.base import Model


User = get_user_model()


class CakeLevel(models.Model):
    level = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()


class CakeForm(models.Model):
    type = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()


class Topping(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()


class Berry(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()


class Decor(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()


class Cake(models.Model):
    # Вопрос - должны ли оставаться в базе заказы клиента при удалении аккаунта?
    client = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name='клиент')
    level = models.ForeignKey(to=CakeLevel,
                              on_delete=models.SET_NULL,
                              null=True,
                              verbose_name='уровень')
    topping = models.ManyToManyField(to=Topping,
                                     verbose_name='топпинги')
    berry = models.ManyToManyField(to=Berry,
                                   verbose_name='ягоды')
    decor = models.ManyToManyField(to=Decor,
                                   verbose_name='декор')
    caption_on_cake = models.CharField(blank=True,
                                       verbose_name='надпись на торте')


class Order(models.Model):
    # Вопрос - один заказ - один торт?
    cake = models.ForeignKey(to=Cake,
                             on_delete=models.SET_NULL,
                             null=True,
                             verbose_name='торт')
