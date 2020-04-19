
import logging

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# Create your models here.


class Site(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Building(models.Model):
    name = models.CharField(max_length=200)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    @property
    def floors(self):
        return self.floor_set.order_by('level')


    def __str__(self):
        return self.name


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    name = models.CharField(default='', max_length=200)

    image = models.ImageField(
        null=True,
        blank=True)

    @property
    def lower_floor(self):
        try:
            return self.building.floor_set.filter(level__lt=self.level).order_by('-level')[0]
        except IndexError:
            return None

    @property
    def upper_floor(self):
        try:
            return self.building.floor_set.filter(level__gt=self.level).order_by('level')[0]
        except IndexError:
            return None


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['building', 'level'], name='unique_level')
        ]

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.level)
        #return '{f.name} ({f.level})'.format(f=self)
