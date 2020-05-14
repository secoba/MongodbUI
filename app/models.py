from django.db import models


# Create your models here.


# class Config(models.Model):
#     cid = models.CharField(max_length=200, unique=True)
#     host = models.CharField(max_length=200)
#     port = models.CharField(max_length=200)
#     database = models.CharField(max_length=200)
#     username = models.CharField(max_length=400)
#     password = models.CharField(max_length=400)
#
#     create_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = "config"
#         db_table = "config"
#         ordering = ["create_time"]
