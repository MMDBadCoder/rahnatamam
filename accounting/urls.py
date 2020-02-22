from django.conf.urls import url
from django.urls import path

from accounting import views

urlpatterns = [
    url('set-destination/', views.set_destination, name='set-destination'),
    url('signup/', views.signup, name='signup'),
    url('panel/', views.panel, name='panel'),
    url('add-new-relative/', views.add_relative_human, name='add-new-relative'),
    path('delete-relative/<int:human_id>', views.delete_relative, name='delete-relative'),
    url('login/', views.login_view, name='login'),
    url('logout/', views.logout_view, name='logout'),
    url('activate/', views.activate, name='activate'),
    url('delete-account/', views.delete_account, name='delete-account'),
]
