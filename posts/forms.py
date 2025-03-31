from django import forms

from posts.models import PostReview, Post


class PostReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = PostReview
        fields = ('stars_given', 'comment')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'post_picture']