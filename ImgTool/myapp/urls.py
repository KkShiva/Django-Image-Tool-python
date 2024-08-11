from django.urls import path
from . import views
from .views import image_filter_view, display_filtered_image

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("cats/", views.cats, name="cats"),
    path('cat/', views.cataas, name='random_cat'),
    path('cat/gif/', views.cataas, name='cat_gif'),
    path('cat/<str:tag>/', views.cataas, name='cat_by_tag'),
    path('cat/says/<str:text>/', views.cataas, name='cat_says'),
    path('cat/says/<str:text>/<str:fontSize>/<str:fontColor>/', views.cataas, name='cat_says_styled'),
    path('dog/', views.random_dog, name='random_dog'),
    path('dog/<str:breed>/', views.random_dog_by_breed, name='random_dog_by_breed'),
    path("Dogs/", views.Dogs, name="Dogs"),
    path('image-filter/', image_filter_view, name='image_filter'),
    path('display-image/<str:image_name>/', display_filtered_image, name='display_filtered_image'),
]