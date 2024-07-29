from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import (
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
    CreateView,
    View,
    FormView,
)
from django.views.generic.detail import SingleObjectMixin
from .models import Article
from django.urls import reverse_lazy, reverse
from .forms import CommentForm

# Create your views here.


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles.html'


class GetFromArticleDetail(DetailView):
    model = Article
    template_name = 'detail_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostFromArticleDetail(SingleObjectMixin, FormView):
    model = Article
    template_name = "detail_article.html"
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = GetFromArticleDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostFromArticleDetail.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'edit_article.html'
    fields = [
        'title',
        'body',
    ]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles')
    template_name = 'delete_article.html'

    # this is for UserPassesTestMixin
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'create_article.html'
    fields = (
        'title',
        'body'
    )

    # this is for UserPassesTestMixin
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
