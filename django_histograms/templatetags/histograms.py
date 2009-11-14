from django_histograms.utils import Histogram
from django import template
from django.db.models import get_model

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model


register = template.Library()


@tag(register, [Model(), Variable(), Optional([Variable(), Variable()])])
def histogram_for(model, attname, months=2, day_labels=True):
    return Histogram(model, attname, months=months).render(css=True, day_labels=day_labels)


@tag(register, [Model(), Variable(), Optional([Variable(), Variable()])])
def histogram_for_days(model, attname, days=31, day_labels=True):
    return Histogram(model, attname, days=days).render(css=True, day_labels=day_labels)
