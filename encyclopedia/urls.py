from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path('create/', views.create , name = "create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random/", views.randomEntry , name="random"),
    path("search/", views.search, name="search")
]
