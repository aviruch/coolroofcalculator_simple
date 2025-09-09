"""coolRoofCalculator URL Configuration"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # main app views
    path('coolroofcalculator/', views.testindex, name='coolroofcalculator'),
    path('insertdb/', views.insertdb, name='insertdb'),
    path('', views.index, name='index'),  # root URL
    path('index/', views.index, name='index'),
    path('result/', views.displayResult, name='result'),
    path('glossary/', views.glossary, name='glossary'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
