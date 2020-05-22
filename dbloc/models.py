'''Model definition for the `loc` application.'''

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _


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

        # we can only manage floors if we have a parent. Otherwise we do not
        # know which floors belong to the same building.
        if (not self.parent) or (not self.level):
            return None

        return Plan.objects\
            .filter(
                parent=self.parent,
                level__lt=self.level)\
            .order_by('level')\
            .first()


    @property
    def upper_floor(self):
        '''Get the plan of the next upper floor.'''

        # we can only manage floors if we have a parent. Otherwise we do not
        # know which floors belong to the same building.
        if (not self.parent) or (not self.level):
            return None

        return Plan.objects\
            .filter(
                parent=self.parent,
                level__gt=self.level)\
            .order_by('-level')\
            .first()


    @property
    def sub_plans(self):
        '''Return the sub plans for this plan. E.g. returns the floors or a building or
        the buildings of a site.'''

        return self.plan_set.order_by('name')


    def __str__(self):
        if self.name:
            return self.name

        return str(self.level)


    def get_absolute_url(self):
        '''Get the URL of a Plan instance.'''

        return reverse('dbloc:plan', args=[self.id])


    def get_root_path(self):
        if hasattr(self, '_root_path'):
            return self._root_path

        '''Returns a list of plans from the top level plan to this plan'''
        plans = [self]
        plan = self
        while plan.parent is not None:
            plan = plan.parent
            plans.append(plan)

        plans.reverse()

        self._root_path = plans

        return plans


def validate_coord(value):
    '''Validate that coordinate values are in range from 0.0 to 1.0.'''

    if (value < 0.0) or (value > 1.0):
        raise ValidationError(
            _('%(value)s is our of range for coordinates (required 0.0-1.0).'),
            params={'value': value})


class Teleport(models.Model):
    '''A teleport represents a link from a location in a plan to another plan.'''

    x = models.FloatField(default=0.0, validators=[validate_coord])
    y = models.FloatField(default=0.0, validators=[validate_coord])

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

    def __str__(self):
        return self.text


    def get_image_x(self):
        '''Return the absolute x coordinate of this teleport (i.e. scaled to the image
        size of the plan).

        '''

        if not self.src:
            return 0

        return int(self.src.image.width * self.x)


    def get_image_y(self):
        '''Return the absolute y coordinate of this teleport (i.e. scaled to the image
        size of the plan).

        '''

        if not self.src:
            return 0

        return int(self.src.image.height * self.y)
