from django.urls import path

from . import views


urlpatterns = [
    # INICIO
    path("", views.home, name="home"),
    path("logout/", views.exit, name="exit"),
    path("registration/register", views.register, name="register"),
    path("registration/login", views.login, name="login"),
    # PAGINAS
    path("paginas/perfil", views.perfil, name="perfil"),
    path("paginas/editarPerfil", views.editarPerfil, name="editarPerfil"),
    path("paginas/usuarios", views.usuarios, name="usuarios"),
    path("paginas/agregarUsuario", views.agregarUsuario, name="agregarUsuario"),
    path("paginas/eliminarUsuario", views.eliminarUsuario, name="eliminarUsuario"),
    path("paginas/editarUsuario", views.editarUsuario, name="editarUsuario"),

    path("paginas/servicios", views.servicios, name="servicios"),
    path("paginas/productos", views.productos, name="productos"),
    path('verDetalle/<str:tipo>/<int:id>/', views.verDetalle, name='verDetalle'),
]
