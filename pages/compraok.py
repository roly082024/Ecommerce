import streamlit as st
from datetime import datetime

# --- VERIFICACIÓN DE SEGURIDAD ---
# 1. Asegurarse de que el usuario está logueado
if 'login' not in st.session_state or not st.session_state.login:
    st.switch_page('app.py')

# 2. Asegurarse de que venimos de un pago exitoso
# Esta lógica ahora funciona correctamente. Se ejecuta al inicio de cada recarga del script.
if 'processed_order_id' not in st.session_state:
    st.warning("No hay ninguna compra confirmada para mostrar.")
    if st.button("Volver al catálogo"):
        st.switch_page("pages/catalogo.py")
    st.stop() # Detiene la ejecución si no hay una orden que mostrar.

# --- CARGA DE ESTILOS Y DATOS ---
try:
    with open("estilos/css_compra.html", "r") as file:
        st.markdown(file.read(), unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("No se encontró el archivo de estilos 'estilos/css_compra.html'.")

# Obtener el ID del pedido desde la sesión
order_id = st.session_state.processed_order_id
order_data = None

try:
    if 'db' in st.session_state:
        order_ref = st.session_state.db.collection('orders').document(order_id)
        order_doc = order_ref.get()
        if order_doc.exists:
            order_data = order_doc.to_dict()
        else:
            st.error("Error: No se pudo encontrar tu orden. Por favor, contacta a soporte.")
            st.stop()
    else:
        st.error("La conexión con la base de datos no está disponible.")
        st.stop()
except Exception as e:
    st.error(f"Ocurrió un error al recuperar tu orden: {e}")
    st.stop()

# --- LIMPIEZA DEL CARRITO ---
def clear_cart_in_firestore():
    try:
        if 'db' in st.session_state and 'usuario' in st.session_state:
            user_id = st.session_state['usuario']['uid']
            cart_ref = st.session_state.db.collection('carts').document(user_id)
            cart_ref.set({'items': []}, merge=True)
    except Exception as e:
        st.warning(f"No se pudo limpiar el carrito en la base de datos: {e}")

st.session_state.cart = []
clear_cart_in_firestore()

# --- INTERFAZ DE CONFIRMACIÓN ---
if order_data:
    st.balloons()
    
    st.markdown(f"""
    <div class="confirmation-container">
        <div class="confirmation-header">
            <h1>¡Gracias por tu compra, {st.session_state.get('usuario', {}).get('nombre', 'Cliente').split()[0]}!</h1>
            <p>Tu pedido ha sido confirmado y está siendo procesado.</p>
        </div>
        <div class="order-summary">
            <h2>Resumen del Pedido</h2>
            <p><strong>Número de Pedido:</strong> {order_data.get('order_number', 'N/A')}</p>
            <p><strong>Fecha:</strong> {order_data.get('completed_at').strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p><strong>Total Pagado:</strong> <span class="total-price">${order_data.get('total', 0.0):.2f}</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Ver detalles de los productos"):
        for item in order_data.get('items', []):
            st.markdown(f"""
            <div class="product-item-summary">
                <img src="{item['image']}" width="70" onerror="this.onerror=null;this.src='https://placehold.co/70x70/EFEFEF/333333?text=Img';">
                <div class="product-details">
                    <strong>{item['name']}</strong><br>
                    <span>Cantidad: {item['quantity']}</span><br>
                    <span>Precio: ${item['price']:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("🛍️ Seguir Comprando", use_container_width=True, type="primary"):
        # 1. Limpiamos el ID del pedido procesado
        if 'processed_order_id' in st.session_state:
            del st.session_state.processed_order_id
        
        # 2. Redirigimos INMEDIATAMENTE al catálogo
        st.switch_page("pages/catalogo.py")

