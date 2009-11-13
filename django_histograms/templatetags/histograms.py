from django_histograms.utils import Histogram
from django import template
from django.db.models import get_model

register = template.Library()

def histogram_for(model, attname, months=2, day_labels=True):
    if isinstance(model, basestring):
        model = get_model(*model.split('.'))
    return Histogram(model, str(attname), months=months).render(css=True, day_labels=day_labels)
register.simple_tag(histogram_for)

# try:
#     from coffin import template
# except ImportError:
#     pass
# else:
#     register = template.Library()
#     register.object(histogram_for)