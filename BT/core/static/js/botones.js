
function decrementarCantidad(button) {
    var input = button.parentNode.querySelector('input');
    var valor = parseInt(input.value);
    if (valor > 1) {
        input.value = valor - 1;
    }
}

function incrementarCantidad(button) {
    var input = button.parentNode.querySelector('input');
    var valor = parseInt(input.value);
    if (valor < 10) {
        input.value = valor + 1;
    }
}

function incrementarCantidadC(inputId) {
    var input = document.getElementById(inputId);
    if (parseInt(input.value) < 10) {
        input.value = parseInt(input.value) + 1;
    }
}

function decrementarCantidadC(inputId) {
    var input = document.getElementById(inputId);
    if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
    }
}

function incrementarCantidadC(button) {
    var cantidadField = button.parentNode.previousElementSibling;
    cantidadField.value = parseInt(cantidadField.value) + 1;
}

function decrementarCantidadC(button) {
    var cantidadField = button.parentNode.nextElementSibling;
    var cantidad = parseInt(cantidadField.value);
    if (cantidad > 0) {
        cantidadField.value = cantidad - 1;
    }
}

function incrementarCantidadOC(button) {
    var cantidadField = button.parentNode.previousElementSibling;
    cantidadField.value = parseInt(cantidadField.value) + 1;
}

function decrementarCantidadOC(button) {
    var cantidadField = button.parentNode.nextElementSibling;
    var cantidad = parseInt(cantidadField.value);
    if (cantidad > 0) {
        cantidadField.value = cantidad - 1;
    }
}
