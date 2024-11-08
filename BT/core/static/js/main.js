function editarProducto(id, costo, descuento) {
    document.getElementById('id_producto_editar').value = id;
    document.getElementById('costo_editar').value = costo;
    document.getElementById('descuento_editar').value = descuento;

    $('#EditarProductoModal').modal('show');

}


function editarPerfil(id, username, first_name, last_name, email, direccion, region, comuna, telefono, fecha_nac, password) {
    document.getElementById('id_perfil_editar').value = id;
    document.getElementById('username_editar').value = username;
    document.getElementById('nombre_editar').value = first_name;
    document.getElementById('apellido_editar').value = last_name;
    document.getElementById('email_editar').value = email;
    document.getElementById('direccion_editar').value = direccion;
    document.getElementById('region_editar').value = region;
    document.getElementById('comuna_editar').value = comuna;
    document.getElementById('telefono_editar').value = telefono;
    document.getElementById('fecha_nac_editar').value = fecha_nac;
    document.getElementById('password_editar').value = password;
}

function editarUsuario(id, username, first_name, last_name, email, direccion, region, comuna, telefono, fecha_nac, tipo_user, password) {
    document.getElementById('id_usuario_editar').value = id;
    document.getElementById('username_editar').value = username;
    document.getElementById('nombre_editar').value = first_name;
    document.getElementById('apellido_editar').value = last_name;
    document.getElementById('email_editar').value = email;
    document.getElementById('direccion_editar').value = direccion;
    document.getElementById('region_editar').value = region;
    document.getElementById('comuna_editar').value = comuna;
    document.getElementById('telefono_editar').value = telefono;
    document.getElementById('fecha_nac_editar').value = fecha_nac;
    document.getElementById('tipo_user_editar').value = tipo_user;
    document.getElementById('password_editar').value = password;

}

function eliminarUsuario(id) {
    document.getElementById('id_usuario_eliminar').value = id;
}

function editarOrden(id, estado_orden) {
    document.getElementById('id_compra_editar').value = id;
    document.getElementById('estado_editar').value = estado_orden;

}


function editarEnvio(id, estado_envio) {
    document.getElementById('id_envio_editar').value = id;
    document.getElementById('envio_editar').value = estado_envio;

}

