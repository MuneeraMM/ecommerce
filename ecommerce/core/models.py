from django.db import models
# Create your models here.
from django.contrib.auth.models import User
class Customer(models.Model):
    user = models.OneToOneField(User,null=False,blank=False,on_delete = models.CASCADE)
    #extra fields will come here
    phone_field = models.CharField(max_length=12,blank=False)

    def __str__(self):
        return self.user.username