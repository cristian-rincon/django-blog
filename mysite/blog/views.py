from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post



# VISTA BASADA EN FUNCIONES
def post_list(request):
    """
    Lista de posts
    """
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts por página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, retorna la página 1
        posts = paginator.page(1)
    except EmptyPage:
        # Si la pagina está fuera de rango, entrega la última página de resultados
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    """
    Un solo post
    """
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


# VISTA BASADA EN CLASE (CLASS-BASED-VIEWS) https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/
class PostListView(ListView):
    """
    docstring
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
