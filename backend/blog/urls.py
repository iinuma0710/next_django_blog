from django.urls import path

from blog import views


urlpatterns =[
    path("new/", views.article_new, name="article_new"),
    path("<int:article_id>/", views.article_detail, name="article_detail"),
    path("<int:article_id>/edit/", views.article_edit, name="article_edit"),
]