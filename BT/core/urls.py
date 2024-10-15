from django.urls import path
from django.contrib.auth.decorators import login_required

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

    path('paginas/inventario', views.inventarioProducto, name="inventario"),
    path("paginas/verInventario/", views.verInventario.as_view(), name="verInventario"),

    path('paginas/agregarProducto', views.agregarProducto, name="agregarProducto"),
    path('paginas/editarProducto', views.editarProducto, name="editarProducto"),
    path('paginas/eliminarProducto', views.eliminarProducto, name="eliminarProducto"),

    path('paginas/calendario', views.calendario, name='calendario'),
    path('paginas/reservar/', views.reservar_cita, name='reservar_cita'),
    path('paginas/reservaexitosa/', views.reserva_exitosa, name='reserva_exitosa'),
    path('obtener_reservas/', views.obtener_reservas, name='obtener_reservas'),
    path('eliminar_cita/<int:id>/', views.eliminar_cita, name='eliminar_cita'),
    path('editar_cita/<int:id>/', views.editar_cita, name='editar_cita'),
    path('obtener_servicios/', views.obtener_servicios, name='obtener_servicios'),
    path('obtener_reserva/<int:id>/', views.obtener_reserva, name='obtener_reserva'),
]
