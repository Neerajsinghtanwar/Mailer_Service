from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('about', views.about_us, name='about'),
    path('contact', views.contact_us, name='contact'),
    path('analyze', views.analyze, name='analyze')

]