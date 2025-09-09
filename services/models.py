from django.db import models
from users.models import ProviderProfile


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    

class ProviderService(models.Model):
# Links a ProviderProfile to a specific subservice and stores provider price
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="services")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="provider_services")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="مثلاً ایاب و ذهاب")


    def __str__(self):
        return f"{self.provider.user.username}: {self.subcategory.name} - {self.price}"

