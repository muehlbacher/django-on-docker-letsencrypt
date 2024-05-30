from django.urls import path
from . import views
#from .views import get_new_coordinates


urlpatterns = [
    path('', views.index, name='index'),
    #path('new-coordinates/', get_new_coordinates, name='new-coordinates'),

]
