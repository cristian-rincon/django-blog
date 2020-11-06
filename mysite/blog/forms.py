from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """
    Clase para el manejo de los datos enviados
    a través del formulario para emails.

    Hereda de la chase base Form. Se pueden usar
    tipos de datos para validar los campos como
    sea necesario.

    Referencia: https://docs.djangoproject.com/en/3.0/ref/forms/fields/

    Se puede probar usando:
    make shell

    from django.core.mail import send_mail
    send_mail('Django mail', 'This e-mail was sent with Django',
    'cristian.o.rincon.b@gmail.com', ['cristian.o.rincon.b@gmail.com'], fail_silently=False)

    Si el mensaje es 1, entonces se envió de manera correcta el correo.
    """

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    name.widget.attrs.update({"class": "form-control"})
    email.widget.attrs.update({"class": "form-control"})
    to.widget.attrs.update({"class": "form-control"})
    comments.widget.attrs.update({"class": "form-control"})


class CommentForm(forms.ModelForm):
    """
    Handle comments form
    """

    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }
