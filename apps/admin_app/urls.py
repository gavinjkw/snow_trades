from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'home$', views.login),
    url(r'login_admin$', views.login_admin),
    url(r'logout$', views.logout_admin),
    url(r'items$', views.items),
    url(r'users$', views.users),
    url(r'orders$', views.orders),
    url(r'delete_item$', views.delete_item),
    url(r'delete_order$', views.delete_order),
    url(r'delete_user$', views.delete_user),
]
