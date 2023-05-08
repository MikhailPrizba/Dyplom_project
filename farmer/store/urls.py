from django.urls import path

from . import views

app_name = "store"
urlpatterns = [
    path("like/", views.product_like, name="like"),
    path("rating/", views.rating, name="rating"),
    path('search/', views.Search.as_view(), name='search'),
    path("", views.home, name="home"),
    path("profile/<int:id>/", views.sellerprofile, name="profile"),
    path("<slug:category_slug>/", views.home, name="product_list_by_category"),
    path("<slug:slug>/<int:id>/", views.product_detail, name="product_detail"),
    path(
        "<slug:slug>/<int:id>/comment/",
        views.CommentCreateView.as_view(),
        name="comment-add",
    ),
    path(
        "comment/<int:pk>/update",
        views.CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    
]
