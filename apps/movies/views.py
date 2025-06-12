from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from apps.movies.models import Movie,Review,Genre
from django.db.models import Avg
from apps.meta.models import MovieView
from datetime import timedelta
from django.utils import timezone
from apps.movies.utils import get_client_ip
from django.core.paginator import Paginator


def movies_view(request):
    query=request.GET.get('q') if request.GET.get('q')!=None else ''
    selected_genre_id=request.GET.get('genre')
    movies=Movie.objects.filter(title__icontains=query)
    if selected_genre_id:
        movies=movies.filter(genre__id=selected_genre_id)
    genres=Genre.objects.all()
    paginator = Paginator(movies, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'movies.html', context={'movies': movies,
                                                   'page_obj': page_obj, 
                                                   'genres':genres,
                                                   'selected_genre_id':int(selected_genre_id)
                                                    if selected_genre_id else None})

def single_movie_view(request,pk):
    movie=get_object_or_404(Movie,pk=pk)
    rating = Review.objects.filter(movie=movie).aggregate(average=Avg('rating'))
    reviews=Review.objects.filter(movie=movie)
    ip_address = get_client_ip(request)
    movie_view = MovieView.objects.filter(ip=ip_address).last()
    if not movie_view or timezone.now() - movie_view.created_at >= timedelta(hours=1):
        new_view = MovieView.objects.create(movie=movie,
                                            ip=ip_address)
        if request.user.is_authenticated:
            new_view.user = request.user
            new_view.save()
    return render(request,'single-movie.html',context={'movie':movie,
                                                       'rating': rating['average'],
                                                       'reviews':reviews,
                                                       'views':movie.views_count})


def add_review_view(request, pk):
    comment = request.POST.get('comment')
    rating = int(request.POST.get('rating'))
    name = request.POST.get('name')
    email = request.POST.get('email')
    movie = Movie.objects.get(id=pk)

    Review.objects.create(comment=comment,
                          rating=rating,
                          name=name,
                          email=email,
                          movie=movie)
   

    return redirect(reverse('single_movie', kwargs={'pk': pk}))







