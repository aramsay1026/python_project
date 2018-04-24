from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^$', views.home), 
	
	url(r'^welcome', views.process)

]