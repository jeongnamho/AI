from django.db import models
from django.utils import timezone

class User(models.Model):
    userid = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    hobby = models.CharField(max_length=20)

    def __str__(self):
        #return self.userid + '/' + self.name + '/' + self.age
        return f"{self.userid}  /  {self.name}  /  {self.age}"