from django.db import models

# Create your models here.
class Buyer(models.Model):
    name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    age = models.IntegerField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    size = models.DecimalField(max_digits=20, decimal_places=3)
    description = models.TextField()
    age_limited = models.BooleanField(default=False)
    buyer = models.ManyToManyField(Buyer, related_name='buyers')

    def __str__(self):
        return self.title


class BasketItem():
    def __init__(self, title: str, cost: float, age_limited: bool = False, count: int = 1):
        self.title = title
        self.checked = ''
        self.sum = 0
        self.cost = cost
        self.count = count
        self.age_limited = age_limited


    def __str__(self):
        return self.title

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == 'count' or key == 'checked':
            self.sum = self.count * self.cost if self.checked == 'checked' else 0
