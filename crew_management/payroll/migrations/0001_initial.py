# Generated by Django 5.1.2 on 2024-11-19 21:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=10)),
                ('account_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('housing_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('transport_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gross_pay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_deduction', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pension_deduction', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_pay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayrollPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PaySlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_on', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='payslips/')),
            ],
        ),
    ]
