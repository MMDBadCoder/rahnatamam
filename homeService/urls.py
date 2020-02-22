from django.conf.urls import url
from homeService import views

urlpatterns = [
                  url('', views.home_page, name='home'),
              ]
