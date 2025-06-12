from django.urls import path
from apps.movies.views import movies_view,single_movie_view,add_review_view

urlpatterns=[
    path('',movies_view,name='movies'),
    path('single_movie/<str:pk>',single_movie_view,name='single_movie'),
    path('add-review/<int:pk>', add_review_view, name='add_review'),

]