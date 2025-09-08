from django.db import models

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

class SubCategory(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provider = models.ForeignKey("users.ProviderProfile", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
