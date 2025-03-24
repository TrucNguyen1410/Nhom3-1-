from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Vì MongoDB lưu password hash

    class Meta:
        db_table = "users"  # Tên collection MongoDB
