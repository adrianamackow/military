# Generated by Django 2.2.6 on 2019-12-14 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('militaria', '0004_warehouse_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='priority',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], default=2),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='weight',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=3),
        ),
    ]