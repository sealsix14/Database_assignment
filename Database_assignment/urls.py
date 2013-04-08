from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView
import banking.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^$', banking.views.home, name="Home"),
    # url(r'^Database_assignment/', include('Database_assignment.foo.urls')),
    url(r'^accounts/add_account/',banking.views.add_account, name="new account"),
    url(r'^accounts/add_check/',banking.views.add_check, name="new check"),
    url(r'^accounts/login/',banking.views.login, name="login"),
    url(r'^accounts/add_expense/',banking.views.add_expense,name="new expense"),
    url(r'^accounts/overview/',banking.views.overview,name="overview"),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
