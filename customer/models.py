from django.db import models
from django.contrib.auth.models import *
from django.utils import timezone

# Create your models here.

class Sex(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
        
class User(AbstractUser):
    sex=models.ForeignKey(Sex, on_delete=models.CASCADE, null=True)

    def phoneLastThree(self):
        return self.username[-3:]

#分類
class Classification(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

#素食
class Vegetarian(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

#菜單
class Menu(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    introduce=models.TextField(max_length=500)
    allergy=models.CharField(null=True, max_length=100)
    image = models.ImageField(upload_to='image/', blank=False, null=False)
    listingDate=models.DateField(default=timezone.now())
    isVegetarian=models.ForeignKey(Vegetarian, on_delete=models.CASCADE)
    isSale=models.BooleanField(default=True)
    classification=models.ForeignKey(Classification, on_delete=models.CASCADE)

#留言板
class Comment(models.Model):
    name=models.CharField(max_length=20, null=True)
    commenter=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.TextField(max_length=500)
    uploadTime=models.DateTimeField(null=True, default=timezone.now())

#時段
class Time(models.Model):
    name=models.CharField(max_length=50)
    timeStart=models.TimeField()
    timeEnd=models.TimeField()
    numberOfPeopleMax=models.IntegerField(default=100)
    def __str__(self):
        return f"{self.name} ({self.timeStart.strftime('%H:%M')} ~ {self.timeEnd.strftime('%H:%M')} , 人數上限 {self.numberOfPeopleMax})"

#訂位
class Reserve(models.Model):
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    numberOfPeople=models.IntegerField()
    date=models.DateField()
    time=models.ForeignKey(Time, on_delete=models.CASCADE)
    note=models.TextField(null=True)
    alternate=models.BooleanField(default=False)
    isCome=models.BooleanField(default=False)