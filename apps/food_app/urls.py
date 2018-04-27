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
    url(r'^thankyou$', views.thankyou),
    url(r'^about$', views.about),
    url(r'^about_suppliers$', views.about_suppliers),
    url(r'^about_volunteers$', views.about_volunteers),
    url(r'^about_shelters$', views.about_shelters),
    url(r'^about_team$', views.about_team),
    url(r'^contact_us$', views.contact_us),
    url(r'^home$', views.go_home),
    url(r'^logout$', views.logout),
    url(r'^contact_us$',views.contact),
    url(r'^send_message$',views.sendMessage),
    url(r'^unjoin$',views.unjoin)

]