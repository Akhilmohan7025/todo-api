from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Todos(models.Model):
    task_name=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    completed_success=models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)
