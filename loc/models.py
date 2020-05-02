'''Model definition for the `loc` application.'''

from django.db import models


class Plan(models.Model):
    '''Model of a plan'''

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
        '''Get the plan of the next lower floor.'''

        try:
            return self.parent.floor_set.filter(level__lt=self.level).order_by('-level')[0]
        except IndexError:
            return None


    @property
    def upper_floor(self):
        '''Get the plan of the next upper floor.'''

        try:
            return self.parent.floor_set.filter(level__gt=self.level).order_by('level')[0]
        except IndexError:
            return None


    @property
    def sub_plans(self):
        '''Return the sub plans for this plan. E.g. returns the floors or a building or
        the buildings of a site.'''

        return self.plan_set.order_by('name')


    def __str__(self):
        if self.name:
            return self.name

        return str(self.level)


class Teleport(models.Model):
    '''A teleport represents a link from a location in a plan to another plan.'''

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
        related_name='+',
        null=True)

    class Meta:
        ordering = ('text', )
