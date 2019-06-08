from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.landing),
    url(r'^register$', views.index),
    url(r'^store$', views.login),
    url(r'^process_reg$', views.process_reg),
    url(r'^login$', views.login_process),
    url(r'^logout$', views.logout),
    url(r'^add_item$', views.add_item),
    url(r'^add_item_process$', views.add_item_process),
    url(r'^add_cart_process$', views.add_cart_process),
    url(r'^cart$', views.shopping_cart),
    url(r'^complete_purchase$', views.complete_purchase),
    url(r'^delete_cart_item$', views.delete_cart_item),
    url(r'^snowboards$', views.snowboards),
    url(r'^skiis$', views.skiis),
    url(r'^boots$', views.boots),
    url(r'^bindings$', views.bindings),
    url(r'^apparel$', views.apparel),
    url(r'^home$', views.home),
    url(r'^account$', views.account),
    url(r'^edit_account$', views.edit_account),
    url(r'^edit_user_process$', views.edit_user_process),
    url(r'^purchase_page$', views.purchase_page),
]
