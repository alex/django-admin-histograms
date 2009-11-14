from django.conf.urls.defaults import url, patterns
from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext

class HistogramAdmin(admin.ModelAdmin):
    histogram_field = None
    histogram_months = 2
    histogram_days = None
    histogram_day_labels = True
    
    def get_urls(self):
        urlpatterns = patterns("",
            url(r"^report/$", self.admin_site.admin_view(self.report_view),
                name="%s_report" % self.model._meta.object_name)
        )
        return urlpatterns + super(HistogramAdmin, self).get_urls()
    
    def report_view(self, request):
        assert self.histogram_field is not None, "Set histogram_field you idiot"

        histogram = Histogram(self.model, self.histogram_field,
            self.queryset(request), months=self.histogram_months,
            days=histogram_days, day_labels=histogram_day_labels)
        
        context = {
            'title': "Histogram for %s" % self.model._meta.object_name,
            'histogram': histogram,
        }

        return render_to_response("admin/report.html", context,
            context_instance=RequestContext(request, current_app=self.admin_site.name))
