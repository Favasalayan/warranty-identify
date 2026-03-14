from django.db import models


class SearchHistory(models.Model):

    invoice_no = models.CharField(max_length=50)

    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_no


class WarrantyCard(models.Model):

    invoice_no = models.CharField(max_length=50, unique=True)

    customer_name = models.CharField(max_length=200)

    customer_phone = models.CharField(max_length=50)

    printed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_no} - {self.customer_name}"