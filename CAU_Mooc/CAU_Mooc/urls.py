from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin


urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^login/$', TemplateView.as_view(template_name="login.html"), name="login"),
]
