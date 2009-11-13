from django_histograms.utils import Histogram
from django import template

register = template.Library()

def histogram_for(model, attname):
    return Histogram(model, attname).render(css=True)
register.simple_tag(histogram_for)

try:
    from coffin import template
except ImportError:
    pass
else:
    register = template.Library()
    register.object(histogram_for)