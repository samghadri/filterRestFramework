from django.conf.urls import url
from . import views


urlpatterns =[
    url(r'^person/(?P<person_id>\d+)', views.PersonDetailView.as_view(), name='single_person'),
    url(r'^person', views.PersonListView.as_view(), name='person'),
    
]
