from django.apps import AppConfig


class MyStatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_stat'
    verbose_name = 'Статистика по магазину'
