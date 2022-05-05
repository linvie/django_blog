from django.shortcuts import render

# Create your views here.
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import re
from pure_pagination.mixins import PaginationMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q

def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})


class IndexView(PaginationMixin,ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return (
            super()
            .get_queryset()
            .filter(created_time__year=year, created_time__month=month)
        )

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        return super().get_queryset().filter(category=cate)



class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super().get_queryset().filter(tags=t)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response







