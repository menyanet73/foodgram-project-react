# Generated by Django 2.2.16 on 2022-06-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20220601_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='item_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
