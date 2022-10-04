from django.contrib import admin
from django.urls import path, include
from spkapp import views

urlpatterns = [
    path('', views.dologin, name="dologin"),
    path('dohome/', views.dohome, name="dohome"),
    path('dologout/', views.dologout, name="dologout"),
    path('neworder/', views.newOrder, name="neworder"),
    path('formorder/', views.formorder, name="newform"),
    path('approveorder/', views.approveOrder, name="approveorder"),
    path('editorder/<order_id>', views.editOrder, name="editorder"),
    path('orderdetails/', views.orderDetails, name="orderdetails"),
    path('vieworder/', views.viewOrder, name="vieworder"),
    path('report/', views.viewReport, name="report"),
    path('registration/', views.userRegistration, name="registration"),


    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX

]
