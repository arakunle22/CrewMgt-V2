from django.db import models
from user_management.models import CustomUser
from django.core.validators import MinValueValidator

class EmployeeSalary(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='salary')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    housing_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Salary Structure"

class PayrollPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_date} to {self.end_date}"

class Payroll(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    pension_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.period}"

    def calculate_net_pay(self):
        self.net_pay = self.gross_pay - self.tax_deduction - self.pension_deduction
        self.save()

class BankDetail(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bank_detail')
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=10)  # Nigerian bank account numbers are typically 10 digits
    account_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Bank Details"

class PaySlip(models.Model):
    payroll = models.OneToOneField(Payroll, on_delete=models.CASCADE)
    generated_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='payslips/')

    def __str__(self):
        return f"Pay Slip for {self.payroll}"