
import logging

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# Create your models here.


#class AddressObject(models.Model):
#    description = models.TextField(default='', max_length=2000, blank=True)
#    address = models.TextField(default='', max_length=1000, blank=True)
#    url = models.CharField(default='', max_length=1000, blank=True)
#
#    class Meta:
#        abstract = True
#

#class Site(AddressObject):
#    name = models.CharField(max_length=200)
#
#    class Meta:
#        ordering = ('name',)
#
#    def __str__(self):
#        return self.name
#

#class Building(AddressObject):
#    name = models.CharField(max_length=200)
#    image = models.ImageField(null=True, blank=True)
#
#    site = models.ForeignKey(Site, on_delete=models.CASCADE)
#
#    class Meta:
#        ordering = ('name',)
#
#    @property
#    def floors(self):
#        return self.floor_set.order_by('level')
#
#    def __str__(self):
#        return self.name
#

class Plan(models.Model):
    name = models.CharField(default='', max_length=200)
    image = models.ImageField(null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)

    description = models.TextField(default='', max_length=2000, blank=True)
    address = models.TextField(default='', max_length=1000, blank=True)
    url = models.URLField(default='', max_length=1000, blank=True)

    class Meta:
        ordering = ('level',)
        constraints = [
            models.UniqueConstraint(fields=['parent', 'level'], name='unique_level')
        ]

    @property
    def lower_floor(self):
        try:
            return self.parent.floor_set.filter(level__lt=self.level).order_by('-level')[0]
        except IndexError:
            return None

    @property
    def upper_floor(self):
        try:
            return self.parent.floor_set.filter(level__gt=self.level).order_by('level')[0]
        except IndexError:
            return None

    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.level)


class Teleport(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    text = models.CharField(default='', max_length=200)
    src = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='teleports',
        null=True)

    dest = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='+' ,
        null=True)

    class Meta:
        ordering = ('text', )
