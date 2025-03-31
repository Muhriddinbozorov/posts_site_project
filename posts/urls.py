from django.urls import path
from posts.views import PostsView, PostDetailView, AddReviewView, EditReviewView, PostsHomeView,\
    ConfirmDeleteReview, DeleteReviewView, PostCreate

app_name = "posts"
urlpatterns = [
    path("", PostsView.as_view(), name="list"),
    path('home/', PostsHomeView.as_view(), name='home'),
    path("<int:id>/", PostDetailView.as_view(), name="detail"),
    path("<int:id>/reviews/", AddReviewView.as_view(), name = "reviews"),
    path("<int:post_id>/reviews/<int:review_id>/edit/", EditReviewView.as_view(), name = "edit-review"),
    path("<int:post_id>/reviews/<int:review_id>/delete/confirm/",
         ConfirmDeleteReview.as_view(), name="confirm-delete-review"
         ),
    path("<int:post_id>/reviews/<int:review_id>/delete/",
         DeleteReviewView.as_view(), name="delete-review"
         ),
    path('create/', PostCreate.as_view(), name="create"),
]