from . import views
from django.urls import path

urlpatterns=[
    path('',views.index,name='INDEX'),
    path('Mycart/',views.cart,name='CART'),
    path('Register/',views.register,name='REGISTER'),
    path('Login/',views.logi,name='LOGIN'),
    path('Logout/',views.logo,name='LOGOUT'),
    path('Getreview/',views.getreview,name='GETREVIEW'),
    path('Dine/',views.dine,name='DINE'),
    path('activate/<uidb64>/<token>',views.activate.as_view(),name='ACTIVATE'),
    path('deletecart/',views.deletecart,name='DELETECART'),
    path('incquant/',views.incquant,name='INCQUANT'),
    path('decquant/',views.deccquant,name='DECQUANT'),
    path('addcart/',views.addcart,name='ADDCART'),
    path('payment/',views.payment,name='PAYMENT'),
    path('paysf/',views.paysf,name='PAYSF'),
]