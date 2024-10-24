function editarProducto(id, id_producto, nombre, descripcion, costo, cantidad) {
    document.getElementById("id_producto_editar").value = id;
    document.getElementById("producto_editar").value = id_producto;
    document.getElementById("nombre_editar").value = nombre;
    document.getElementById("descripcion_editar").value = descripcion;
    document.getElementById("costo_editar").value = costo;
    document.getElementById("cantidad_editar").value = cantidad;
}

function eliminarProducto(id) {
    document.getElementById("id_producto_eliminar").value = id;
}

function editarPerfil(id, username, first_name, last_name, email, direccion, region, comuna, telefono, fecha_nac) {
    document.getElementById("id_perfil_editar").value = id;
    document.getElementById("username_editar").value = username;
    document.getElementById("nombre_editar").value = first_name;
    document.getElementById("apellido_editar").value = last_name;
    document.getElementById("email_editar").value = email;
    document.getElementById("direccion_editar").value = direccion;
    document.getElementById("region_editar").value = region;
    document.getElementById("comuna_editar").value = comuna;
    document.getElementById("telefono_editar").value = telefono;
    document.getElementById("fecha_nac_editar").value = fecha_nac;
}

function editarUsuario(id, username, first_name, last_name, email, direccion, region, comuna, telefono, fecha_nac, tipo_user) {
    document.getElementById("id_usuario_editar").value = id;
    document.getElementById("username_editar").value = username;
    document.getElementById("nombre_editar").value = first_name;
    document.getElementById("apellido_editar").value = last_name;
    document.getElementById("email_editar").value = email;
    document.getElementById("direccion_editar").value = direccion;
    document.getElementById("region_editar").value = region;
    document.getElementById("comuna_editar").value = comuna;
    document.getElementById("telefono_editar").value = telefono;
    document.getElementById("fecha_nac_editar").value = fecha_nac;
    document.getElementById("tipo_user_editar").value = tipo_user;
}

function eliminarUsuario(id) {
    document.getElementById("id_usuario_eliminar").value = id;
}
