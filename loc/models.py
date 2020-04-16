from django.db import models

# Create your models here.


class Site(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Building(models.Model):
    name = models.CharField(max_length=200)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return self.name
