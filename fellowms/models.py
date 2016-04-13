from django.db import models

MAX_CHAR_LENGHT = 120
MAX_DIGITS = 10

class Fellow(models.Model):
    """Describe a fellow."""
    class Meta:
        app_label = 'fellowms'

    email = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    full_name = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    year = models.IntegerField(blank=False)

    def __str__(self):
        return "{} <{}>".format(self.full_name, self.email)

class Event(models.Model):
    """Describe a event from one fellow."""
    class Meta:
        app_label = 'fellowms'

    fellow = models.ForeignKey('Fellow',
            null=False,
            blank=False)
    url = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False,
            unique=True)
    name = models.CharField(max_length=MAX_CHAR_LENGHT,
            blank=False)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    description = models.TextField(blank=False)
    budget_request = models.DecimalField(max_digits=MAX_DIGITS,
            decimal_places=2,
            blank=False)

    def __str__(self):
        return "{}".format(self.name)
