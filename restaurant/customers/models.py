from django.db import models
from accounts.models import User, Restaurant_owner
# Create your models here.


Delete_STATUS = (
    ('Active', 'Active'),
    ('Away', 'Away')
)

class Customer_detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant_owner, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField(max_length=200)
    status  = models.CharField(max_length=50, default='Active', choices=Delete_STATUS)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table='Employee Details'