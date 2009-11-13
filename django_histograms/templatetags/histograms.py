from django_histograms.utils import Histogram
from django import template
from django.db.models import get_model

register = template.Library()

def histogram_for(model, attname):
    if isinstance(model, basestring):
        model = get_model(*models.split('.'))
    return Histogram(model, attname).render(css=True)
register.simple_tag(histogram_for)

try:
    from coffin import template
except ImportError:
    pass
else:
    register = template.Library()
    register.object(histogram_for)