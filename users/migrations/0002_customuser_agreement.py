# Generated by Django 3.2.8 on 2021-10-27 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='agreement',
            field=models.BooleanField(default=True, verbose_name='Согласие на обработку персональных даных'),
            preserve_default=False,
        ),
    ]
