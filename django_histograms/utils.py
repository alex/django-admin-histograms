import calendar
import datetime

from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


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
    def __init__(self, model, attname, queryset=None, months=None, days=None):
        # `queryset` exists so it can work with the admin (bad idea?)
        self.model = model
        self.attname = attname
        self._queryset = None
        assert months or days, 'You must pass either months or days, not both.'
        self.months = months
        self.days = days
    
    def render(self, css=False, day_labels=True):
        context = self.get_report()
        context['day_labels'] = day_labels
        if css:
            context['css'] = HISTOGRAM_CSS
        return render_to_string("histograms/report.html", context)
    
    def get_query_set(self):
        return self._queryset or self.model.objects.all()
    
    def get_css(self):
        return mark_safe(HISTOGRAM_CSS)
    
    def get_report(self):
        months = {}
        if self.months:
            this_month = datetime.date.today().replace(day=1)
            last_month = this_month
            for m in xrange(self.months):
                cutoff = last_month
                months['%s.%s' % (last_month.month, last_month.year)] = [
                    last_month,
                    ([0] * calendar.monthrange(last_month.year, last_month.month)[1]),
                    0
                ]
                last_month = (last_month - datetime.timedelta(days=1)).replace(day=1)
            grouper = lambda x: '%s.%s' % (x.month, x.year)
            day_grouper = lambda x: x.day-1
        elif self.days:
            cutoff = datetime.datetime.now() - datetime.timedelta(days=self.days)
            grouper = lambda x: None
            day_grouper = lambda x: (datetime.datetime.now() - x).days
            months[None] = ['Last %s Days' % (self.days), ([0] * self.days), 0]
            
        qs = self.get_query_set().values(self.attname).annotate(
            num=Count("pk")
        ).filter(**{"%s__gt" % str(self.attname): cutoff})
        
        for data in qs.iterator():
            idx = grouper(data[self.attname])
            months[idx][1][day_grouper(data[self.attname])] += data["num"]
            months[idx][2] += data["num"]

        total = sum(o for m in months.itervalues() for o in m[1])
        max_num = max(o for m in months.itervalues() for o in m[1])
        if not (total and max_num):
            ratio = 0
        else:
            ratio = total / max_num * 100

        return {
            "results": months.values(),
            "total": total,
            "ratio": ratio
        }
