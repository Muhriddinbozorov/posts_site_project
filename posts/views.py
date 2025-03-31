from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views import View
from posts.forms import PostReviewForm, PostForm
from posts.models import Post, PostReview, PostAuthor, Author


class PostCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.created_at = now()
                post.save()

                author, created = Author.objects.get_or_create(
                    email=request.user.email,
                    defaults={"first_name": request.user.first_name, "last_name": request.user.last_name}
                )

                if not PostAuthor.objects.filter(post=post, author=author).exists():
                    PostAuthor.objects.create(post=post, author=author)

                return redirect('posts:list')
        else:
            form = PostForm()

        return render(request, 'posts/create.html', {'form': form})

    # def post(self, request):
    #     form = PostForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #
    #         author, created = Author.objects.get_or_create(
    #             email=request.user.email,
    #             defaults={"first_name": request.user.first_name, "last_name": request.user.last_name}
    #         )
    #         PostAuthor.objects.create(post=self.post, author=author)
    #
    #         return redirect('posts:list')
    #     return render(request, 'posts/create.html', {'form': form})



class PostsView(View):

    def get(self, request):
        posts = Post.objects.filter(is_approved=True).order_by('-created_at')
        return render(request, "posts/list.html", {'posts': posts})


class PostsHomeView(View):
    def get(self, request):
        new_posts = Post.objects.filter(is_approved=True).order_by('-created_at') [:5]
        most_viewed_posts = Post.objects.filter(is_approved=True).order_by('-views_count') [:5]
        one_week_ago = timezone.now() - timedelta(days=7)
        recent_viewed_posts = Post.objects.filter(is_approved=True, last_viewed_at__gte=one_week_ago).order_by('-last_viewed_at') [:5]

        context = {
            'new_posts': new_posts,
            'most_viewed_posts': most_viewed_posts,
            'recent_viewed_posts': recent_viewed_posts,
        }
        return render(request, 'posts/home.html', context)


class PostDetailView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        review_form = PostReviewForm()
        return render(request, "posts/detail.html", {"post": post, "review_form": review_form} )

    def get(self, request, id,):
        post = get_object_or_404(Post, id = id)
        post.views_count += 1
        post.last_viewed_at = timezone.now()
        post.save()
        return render(request, 'posts/detail.html', {'post':post})

class AddReviewView( LoginRequiredMixin, View):
    def post(self, request, id):
        post = Post.objects.get(id=id)
        reviews_form = PostReviewForm(data=request.POST)

        if reviews_form.is_valid():
            PostReview.objects.create(
                post = post,
                user = request.user,
                stars_given = reviews_form.cleaned_data['stars_given'],
                comment = reviews_form.cleaned_data['comment']
            )
            return redirect(reverse('posts:detail', kwargs = {'id': post.id}))

        return render(request, "posts/detail.html", {"post": post, "review_form": reviews_form})

class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        review = post.postreview_set.get(id=review_id)
        review_form = PostReviewForm(instance=review)

        return render(request, "posts/edit_review.html", {"post": post, "review": review, "review_form": review_form})

    def post(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        review = post.postreview_set.get(id=review_id)
        review_form = PostReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("posts:detail", kwargs={'id':post_id}))

        return render(request, "posts/edit_review.html", {"post": post, "review": review, "review_form": review_form})

class ConfirmDeleteReview(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        review = post.postreview_set.get(id=review_id)
        return render(request, "posts/confirm_delete_review.html", {"post":post, "review":review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        review = post.postreview_set.get(id=review_id)
        review.delete()
        # messages.success(request, "You have successfully deleted this review")

        return redirect(reverse("posts:detail", kwargs={'id': post_id}))
