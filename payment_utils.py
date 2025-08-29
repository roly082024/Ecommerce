import stripe
import os
from datetime import datetime
import time
from dotenv import load_dotenv
load_dotenv()  # Carga las variables de entorno

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # Configuración esencial

def create_order_in_firestore(db, cart, usuario, status='pending'):
    """Crea registro inicial de orden en Firestore"""
    try:
        order_data = {
            'user_id': usuario['uid'],
            'user_email': usuario['email'],
            'items': cart,
            'total': sum(item['price']*item['quantity'] for item in cart),
            'status': status,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        order_ref = db.collection('orders').document()
        order_ref.set(order_data)
        return order_ref.id
        
    except Exception as e:
        raise Exception(f"Error al crear orden: {str(e)}")

def create_stripe_checkout_session(db, cart, usuario):
    try:
        if not cart:
            raise ValueError("El carrito está vacío")
        
        # 1. Crear orden en Firestore como 'pending'
        order_id = create_order_in_firestore(db, cart, usuario)
        
        # 2. Preparar items para Stripe
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item['name'], 'images': [item['image']]},
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        } for item in cart]

        # 3. Crear sesión en Stripe con metadata
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f"{os.getenv('STRIPE_SUCCESS_URL')}&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=os.getenv("STRIPE_CANCEL_URL"),
            # cancel_url = f"{os.getenv('STRIPE_CANCEL_URL')}&session_id={{CHECKOUT_SESSION_ID}}",
            customer_email=usuario['email'],
            metadata={
                'user_id': usuario['uid'],
                'order_id': order_id,  # ID de Firestore
                'firestore_order_id': order_id  # Compatibilidad
            }
        )
        
        # 4. Actualizar orden con session_id
        db.collection('orders').document(order_id).update({
            'session_id': session.id,
            'updated_at': datetime.now()
        })
        
        return session.url
        
    except Exception as e:
        # Marcar orden como fallida si hay error
        if 'order_id' in locals():
            db.collection('orders').document(order_id).update({
                'status': 'failed',
                'error': str(e),
                'updated_at': datetime.now()
            })

        raise Exception(f"Error en checkout: {str(e)}")







