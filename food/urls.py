from django.urls import path
from . import views
from . views import CheckoutView

urlpatterns = [
    path('',views.index, name='index'),
    path('menu',views.menu, name='menu'),
    path('details/<str:id>',views.details, name='details'),
    path('contact',views.contact, name='contact'),
    path('about',views.about, name='about'),
    path('signout',views.signout,name='signout'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('profile',views.profile, name='profile'),
    path('services',views.services, name='services'),
    path('profile_update',views.profile_update,name='profile_update'),
    path('password',views.password,name='password'),
    path('shopcart',views.shopcart, name='shopcart'),
    path('displaycart',views.displaycart, name='displaycart'),
    path('deleteitem',views.deleteitem, name='deleteitem'),
    path('increase',views.increase, name='increase'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('pay', views.pay , name='pay'),
    path('callback', views.callback , name='callback'),
]
