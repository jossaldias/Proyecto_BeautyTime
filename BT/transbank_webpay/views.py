import random
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
from datetime import datetime as dt
from datetime import timedelta
from core.models import Order, OrderItem

# Create your views here.
#FUNCIÓN QUE INICIA TRANSACCIÓN DE PRUEBA CON TRANSBANK
@login_required
def webpay_plus_create(request):
    order = Order.objects.filter(user=request.user).first()
    session_token = request.session.session_key

    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.session.session_key
    amount = str(order.get_precio_total())
    return_url = 'http://127.0.0.1:8000/webpay-plus/commit'

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = (Transaction()).create(buy_order, session_id, amount, return_url)

    print(response)

    return render(request, 'webpay-plus/create.html', {'request': create_request, 'response': response})


#FUNCIÓN QUE DEVUELVE TOKEN DE TRANSACCIÓN DE PRUEBA 
@login_required
def webpay_plus_commit(request):
    token = request.GET.get("token_ws")
    
    if token is None:
        print("Transacción cancelada por el usuario")

        order = Order.objects.filter(user=request.user).first()
        if order:
            # Obtener los ítems de la orden mediante OrderItem
            items = OrderItem.objects.filter(orden=order)  # Accede a los ítems de la orden

            # Reagregar productos al inventario
            for item in items:
                producto = item.item  # Accede al Item (producto o servicio)
                
                # Si el producto tiene cantidad, actualiza el inventario
                if hasattr(producto, 'cantidad'):  # Solo los productos tienen el campo 'cantidad'
                    cantidad = item.cantidad  # Cantidad del producto
                    producto.cantidad += cantidad  # Aumenta el stock en la cantidad ordenada
                    producto.save()  # Guarda los cambios del producto

            order.delete()  # Elimina la orden después de reponer los productos
            print("Orden eliminada de la base de datos")

        return render(request, 'order/pedidoTransbankCancelado.html')
    
    try:
        # Confirmar la transacción con el token
        response = Transaction().commit(token)
        
        # Extraer los detalles de la respuesta
        buy_order = response['buy_order']  # Orden de compra
        authorization_code = response['authorization_code']  # Código de autorización
        transaction_date = response['transaction_date']  # Fecha de la transacción
        card_last_digits = response['card_detail']['card_number']  # Últimos dígitos de la tarjeta
        amount = response['amount']  # Monto de la transacción

        print("Transacción confirmada")
        print("Detalles de la transacción:", response)

        # Pasar los datos al template de confirmación
        return render(request, 'order/pedidoTransbankListo.html', {
            'buy_order': buy_order,
            'authorization_code': authorization_code,
            'transaction_date': transaction_date,
            'card_last_digits': card_last_digits,
            'amount': amount,
        })
    
    except TransbankError as e:
        print(f"Error en la transacción: {e}")
        return render(request, 'order/pedidoTransbankCancelado.html')
