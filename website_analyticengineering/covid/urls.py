from django.urls import path
from . import views

urlpatterns=[
        path('<str:state>/',views.COVIDstateanaly, name='COVID_STATE_ANALYSIS'),
        ]

