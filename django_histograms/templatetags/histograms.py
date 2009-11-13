from django_histograms.utils import Histogram
from django import template
from django.db.models import get_model

try:
    from coffin import template
except ImportError:
    pass

register = template.Library()

def histogram_for(model, attname, months=2, day_labels=True):
    if isinstance(model, basestring):
        model = get_model(*model.split('.'))
    return Histogram(model, str(attname), months=months).render(css=True, day_labels=day_labels)
register.simple_tag(histogram_for)

def histogram_for_days(model, attname, days=31, day_labels=True):
    if isinstance(model, basestring):
        model = get_model(*model.split('.'))
    return Histogram(model, str(attname), days=days).render(css=True, day_labels=day_labels)
register.simple_tag(histogram_for_days)
