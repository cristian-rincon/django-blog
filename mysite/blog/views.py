# Descomentar la línea 2 para usar el método post_list
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post  # , Comment
from .forms import EmailPostForm, CommentForm


# VISTA BASADA EN FUNCIONES
# def post_list(request):
#     """
#     Lista de posts
#     """
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3)  # 3 posts por página
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # Si la página no es un número entero, retorna la página 1
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Si la pagina está fuera de rango, entrega la última página de
#         # resultados
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                   {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    """
    Detalle de un post, retorna un solo post.
    """
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the cuttern post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )


# VISTA BASADA EN CLASE (CLASS-BASED-VIEWS)
# https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/
class PostListView(ListView):
    """
    Listado de posts, retorna una pagina por cada 3 posts.
    Este valor de paginación se puede modificar en la variable paginate_by
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_share(request, post_id):
    """
    Método para manejar el formulario de compartir por email.
    # TODO - Cambiar el backend SMTP default por alguno que sí llegue a un correo.
    """
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        # El formulario es enviado
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Los campos de formulario pasan la validación
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "admin@myblog.com", [cd["to"]])
            sent = True
    else:
        # Se muestra un formulario vacío
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
