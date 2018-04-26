from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.home), 
    url(r'^sendtosuccess$', views.process),
    url(r'^welcome$',views.validation),
    url(r'^login$',views.login),
    url(r'^supplier$',views.supplier),
    url(r'^process_add$',views.addSupplier),
    url(r'^senddetails$',views.send_details),
    url(r'^findVolunteer$',views.find_volunteer),
    url(r'^volunteers$',views.volunteer_home),
    url(r'^volunteer_join$',views.volunteer_add),
    url(r'^shelter$',views.shelter),
    url(r'^place$', views.place)
]