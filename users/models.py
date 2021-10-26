from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    
    firstname = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    lastname = models.CharField(
        verbose_name='Фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
    )
    social_network = models.CharField(
        'Ссылка на соцсеть',
        max_length=100,
        blank=True,
    )
    address = models.CharField(
        'Адрес',
        max_length=200,
    ) 

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
