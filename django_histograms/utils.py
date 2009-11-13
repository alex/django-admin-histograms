import calendar
import datetime

from django.utils.safestring import mark_safe
from django.db.models import Count
from django.template.loader import render_to_string


HISTOGRAM_CSS = """
.histogram ul {
    font-size: 0.75em;
    height: 10em;
  }

.histogram li {
    position: relative;
    float: left;
    width: 1.5em;
    margin: 0 0.1em;
    height: 8em;
    list-style-type: none;
}

.histogram li a {
    display: block;
    height: 100%;
}

.histogram li .label {
    display: block;
    position: absolute;
    bottom: -2em;
    left: 0;
    background: #fff;
    width: 100%;
    height: 2em;
    line-height: 2em;
    text-align: center;
}

.histogram li a .count {
    display: block;
    position: absolute;
    bottom: 0;
    left: 0;
    height: 0;
    width: 100%;
    background: #AAA;
    text-indent: -9999px;
    overflow: hidden;
}

.histogram li:hover {
    background: #EFEFEF;
}

.histogram li a:hover .count {
    background: #2D7BB2;
}"""

class Histogram(object):
    def __init__(self, model, attname, queryset=None):
        # `queryset` exists so it can work with the admin (bad idea?)
        self.model = model
        self.attname = attname
        self._queryset = None
    
    def render(self, css=False):
        context = self.get_report()
        if css:
            context['css'] = HISTOGRAM_CSS
        return render_to_string("histograms/report.html", context)
    
    def get_query_set(self):
        return self._queryset or self.model.objects.all()
    
    def get_css(self):
        return mark_safe(HISTOGRAM_CSS)
    
    def get_report(self):
        this_month = datetime.date.today().replace(day=1)
        last_month = (this_month - datetime.timedelta(days=1)).replace(day=1)
        qs = self.get_query_set().values(self.attname).annotate(
            num=Count("pk")
        ).filter(**{"%s__gt" % self.attname: last_month})
        
        months = [
            [this_month, ([0] * calendar.monthrange(this_month.year, this_month.month)[1]), 0],
            [last_month, ([0] * calendar.monthrange(last_month.year, last_month.month)[1]), 0],
        ]
        
        for data in qs.iterator():
            if (this_month.month == data[self.attname].month and
                this_month.year == data[self.attname].year):
                idx = 0
            elif (last_month.month == data[self.attname].month and
                last_month.year == data[self.attname].year):
                idx = 1
            else:
                continue
            months[idx][1][data[self.attname].day-1] += data["num"]
            months[idx][2] += data["num"]
        
        return {
            "results": months,
            "total": sum(o for m in months for o in m[1]),
        }