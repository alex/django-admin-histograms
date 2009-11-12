import calendar
import datetime

from django.conf.urls.defaults import url, patterns
from django.contrib import admin
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext


class HistogramAdmin(admin.ModelAdmin):
    histogram_field = None
    
    def get_urls(self):
        urlpatterns = patterns("",
            url(r"^report/$", self.admin_site.admin_view(self.report_view),
                name="%s_report" % self.model._meta.object_name)
        )
        return urlpatterns + super(HistogramAdmin, self).get_urls()
    
    def report_view(self, request):
        assert self.histogram_field is not None, "Set histogram_field you idiot"
        this_month = datetime.date.today().replace(day=1)
        last_month = (this_month - datetime.timedelta(days=1)).replace(day=1)
        qs = self.queryset(request).values(self.histogram_field).annotate(
            num=Count("pk")
        ).filter(**{"%s__gt" % self.histogram_field: last_month})
        
        months = [
            (this_month, [0] * calendar.monthrange(this_month.year, this_month.month)[1]),
            (last_month, [0] * calendar.monthrange(last_month.year, last_month.month)[1]),
        ]
        
        for data in qs.iterator():
            if (this_month.month == data[self.histogram_field].month and
                this_month.year == data[self.histogram_field].year):
                idx = 0
            elif (last_month.month == data[self.histogram_field].month and
                last_month.year == data[self.histogram_field].year):
                idx = 1
            else:
                continue
            months[idx][1][data[self.histogram_field].day-1] += data["num"]
        
        return render_to_response("admin/report.html", {
            "results": months,
            "total": sum(o for m in months for o in m[1]),
            "title": "Histogram for %s" % self.model._meta.object_name,
        }, context_instance=RequestContext(request, current_app=self.admin_site.name))
