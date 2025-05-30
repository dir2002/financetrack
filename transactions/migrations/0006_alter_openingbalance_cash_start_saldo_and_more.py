# Generated by Django 5.1.7 on 2025-04-18 06:43

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_category_alter_subcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openingbalance',
            name='cash_start_saldo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, verbose_name='Сумма денежных средств в наличии'),
        ),
        migrations.AlterField(
            model_name='openingbalance',
            name='deposit_start_saldo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, verbose_name='Сумма денег на депозитных счетах'),
        ),
        migrations.AlterField(
            model_name='openingbalance',
            name='investment_start_saldo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, verbose_name='Сумма денег в инвестиционных активах'),
        ),
        migrations.AlterField(
            model_name='openingbalance',
            name='long_debt_start_saldo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, verbose_name='Сумма долгов с возвратом в течение более 12 мес'),
        ),
        migrations.AlterField(
            model_name='openingbalance',
            name='short_debt_start_saldo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, verbose_name='Сумма долгов с возвратом в течение 12 мес'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сумма транзакции'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Дата транзакции'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.subcategory', verbose_name='Подкатегория'),
        ),
    ]
