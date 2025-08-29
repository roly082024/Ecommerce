import streamlit as st
import os
from datetime import datetime
import time
import stripe
from payment_utils import create_stripe_checkout_session

# Verificar si el usuario está logueado
if 'login' not in st.session_state:
    st.switch_page('app.py')

# --- CONFIGURACIÓN INICIAL ---
# Cargar estilos CSS
with open("estilos/css_catalogo.html", "r") as file:
    st.markdown(file.read(), unsafe_allow_html=True)

# --- FUNCIONES PRINCIPALES ---
def get_products():
    """Obtiene 20+ productos de moda desde Firestore o crea muestra inicial"""
    try:
        products_ref = st.session_state.db.collection('products')
        docs = products_ref.stream()
        
        products = []
        for doc in docs:
            product = doc.to_dict()
            product['id'] = doc.id
            products.append(product)
        
        # Si no hay productos, creamos 20+ de ejemplo
        if not products:
            sample_products = [
                # 1. VESTIDOS (4 productos)
                {
                    "name": "Vestido Negro Elegante",
                    "price": 89.99,
                    "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8",
                    "description": "Perfecto para ocasiones especiales",
                    "category": "vestidos",
                    "stock": 15
                },
                {
                    "name": "Vestido Floral Veraniego",
                    "price": 65.50,
                    "image": "https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03",
                    "description": "Ideal para días soleados",
                    "category": "vestidos",
                    "stock": 20
                },
                {
                    "name": "Vestido Corto de Fiesta",
                    "price": 75.25,
                    "image": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b",
                    "description": "Brillante y con detalles dorados",
                    "category": "vestidos",
                    "stock": 8
                },
                {
                    "name": "Vestido Largo Casual",
                    "price": 55.99,
                    "image": "https://images.unsplash.com/photo-1495385794356-15371f348c31",
                    "description": "Cómodo para el día a día",
                    "category": "vestidos",
                    "stock": 12
                },
                
                # 2. BLUSAS/TOPS (4 productos)
                {
                    "name": "Blusa de Seda Blanca",
                    "price": 45.99,
                    "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c",
                    "description": "Suave y elegante",
                    "category": "blusas",
                    "stock": 25
                },
                {
                    "name": "Top Básico Negro",
                    "price": 29.99,
                    "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27",
                    "description": "Esencial para cualquier armario",
                    "category": "blusas",
                    "stock": 30
                },
                {
                    "name": "Camisa a Cuadros",
                    "price": 39.99,
                    "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10",
                    "description": "Estilo casual y moderno",
                    "category": "blusas",
                    "stock": 18
                },
                {
                    "name": "Top Deportivo",
                    "price": 34.50,
                    "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633",
                    "description": "Perfecto para entrenar",
                    "category": "blusas",
                    "stock": 15
                },
                
                # 3. PANTALONES (4 productos)
                {
                    "name": "Jeans Slim Fit Azul",
                    "price": 79.99,
                    "image": "https://images.unsplash.com/photo-1542272604-787c3835535d",
                    "description": "Ajuste perfecto",
                    "category": "pantalones",
                    "stock": 30
                },
                {
                    "name": "Pantalón Formal",
                    "price": 89.50,
                    "image": "https://plus.unsplash.com/premium_photo-1689977493146-ed929d07d97e",
                    "description": "Para looks profesionales",
                    "category": "pantalones",
                    "stock": 12
                },
                {
                    "name": "Shorts Denim",
                    "price": 49.99,
                    "image": "https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9",
                    "description": "Cómodos para el verano",
                    "category": "pantalones",
                    "stock": 20
                },
                {
                    "name": "Pantalón Cargo Verde",
                    "price": 65.25,
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80",
                    "description": "Con múltiples bolsillos",
                    "category": "pantalones",
                    "stock": 10
                },
                
                # 4. ZAPATOS (4 productos)
                {
                    "name": "Zapatos Tacón Nude",
                    "price": 95.99,
                    "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2",
                    "description": "Elegancia para eventos",
                    "category": "zapatos",
                    "stock": 12
                },
                {
                    "name": "Sneakers Urbanos",
                    "price": 75.00,
                    "image": "https://images.unsplash.com/photo-1600269452121-4f2416e55c28",
                    "description": "Estilo y comodidad",
                    "category": "zapatos",
                    "stock": 18
                },
                {
                    "name": "Botines de Cuero",
                    "price": 110.50,
                    "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772",
                    "description": "Ideales para invierno",
                    "category": "zapatos",
                    "stock": 8
                },
                {
                    "name": "Sandalias Playa",
                    "price": 45.75,
                    "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5",
                    "description": "Cómodas y ligeras",
                    "category": "zapatos",
                    "stock": 25
                },
                
                # 5. ACCESORIOS (4 productos)
                {
                    "name": "Bolso de Mano Premium",
                    "price": 65.99,
                    "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62",
                    "description": "Elegante y espacioso",
                    "category": "accesorios",
                    "stock": 18
                },
                {
                    "name": "Gafas de Sol Aviador",
                    "price": 49.99,
                    "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083",
                    "description": "Protección UV400",
                    "category": "accesorios",
                    "stock": 22
                },
                {
                    "name": "Reloj Minimalista",
                    "price": 89.99,
                    "image": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49",
                    "description": "Diseño atemporal",
                    "category": "accesorios",
                    "stock": 8
                },
                {
                    "name": "Bolso de Moda",
                    "price": 35.50,
                    "image": "https://images.unsplash.com/photo-1559563458-527698bf5295",
                    "description": "Luce genial",
                    "category": "accesorios",
                    "stock": 15
                }
            ]
            
            # Verificar que tenemos suficientes productos
            if len(sample_products) < 20:
                st.error(f"⚠️ Error: Solo hay {len(sample_products)}/20 productos")
            else:
                st.success(f"✅ Se crearán {len(sample_products)} productos de muestra")
            
            # Guardar en Firestore
            for product in sample_products:
                st.session_state.db.collection('products').add(product)
            
            return sample_products
        
        return products
    
    except Exception as e:
        st.error(f"❌ Error al obtener productos: {str(e)}")
        return []

def sync_cart_with_firestore():
    """Guarda el carrito en Firestore"""
    try:
        if 'usuario' in st.session_state:
            user_id = st.session_state['usuario']['uid']
            cart_ref = st.session_state.db.collection('carts').document(user_id)
            
            if 'cart' in st.session_state:
                cart_ref.set({
                    'user_id': user_id,
                    'items': st.session_state.cart,
                    'updated_at': datetime.now()
                }, merge=True)
                    
    except Exception as e:
        st.error(f"❌ Error al guardar carrito: {str(e)}")

def add_to_cart(product):
    """Añade un producto al carrito"""
    try:
        if 'cart' not in st.session_state:
            st.session_state.cart = []
            
        # Verificar si el producto ya está en el carrito
        existing_item = next((item for item in st.session_state.cart if item['product_id'] == product['id']), None)
        
        if existing_item:
            existing_item['quantity'] += 1
        else:
            st.session_state.cart.append({
                'product_id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': 1
            })
        
        sync_cart_with_firestore()
        st.toast(f"✅ {product['name']} añadido al carrito!")
        return True
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return False

def prepare_order_data(session_id, status):
    """Prepara los datos de la orden para Firestore"""
    try:
        if not st.session_state.get('cart'):
            return None
            
        total = sum(item['price'] * item['quantity'] for item in st.session_state.cart)
        
        order_data = {
            'user_id': st.session_state['usuario']['uid'],
            'user_name': st.session_state['usuario']['nombre'],
            'user_email': st.session_state['usuario']['email'],
            'items': st.session_state.cart,
            'total': total,
            'status': status,
            'session_id': session_id,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        if status == 'completed':
            order_data['completed_at'] = datetime.now()
            order_data['order_number'] = f"ORD-{int(time.time())}"
        
        return order_data
        
    except Exception as e:
        st.error(f"Error al preparar datos de orden: {str(e)}")
        return None


# --- INTERFAZ PRINCIPAL ---
st.markdown('<div class="main-header"><h1>🛍️ Fashion Store</h1><p>Bienvenido/a a tu tienda de moda</p></div>', unsafe_allow_html=True)

# Sidebar - Carrito
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['usuario']['nombre']}")
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🛒 Tu Carrito")
    
    if 'cart' in st.session_state and st.session_state.cart:
        total = 0
        for item in st.session_state.cart:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="cart-item">
                    <strong>{item['name']}</strong><br>
                    ${item['price']:.2f} x {item['quantity']}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"remove_{item['product_id']}"):
                    st.session_state.cart = [i for i in st.session_state.cart if i['product_id'] != item['product_id']]
                    sync_cart_with_firestore()
                    st.rerun()
            
            total += item['price'] * item['quantity']
        
        st.markdown(f"**Total: ${total:.2f}**")

        if st.button("💳 Pagar con Stripe", use_container_width=True, type="primary"):
            #try:
            checkout_url = create_stripe_checkout_session(
                st.session_state.db,
                st.session_state.cart,
                st.session_state.usuario
            )
            # st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{checkout_url}\'">', unsafe_allow_html=True)
            st.markdown(f'<a href="{checkout_url}" target="_blank">Haz clic aquí para continuar al checkout</a>', unsafe_allow_html=True)
            #except Exception as e:
            #    st.error(f"Error: {str(e)}")
    else:
        st.info("Tu carrito está vacío")

# Catálogo Principal
st.markdown("## 🛍️ Catálogo de Productos")

# Filtros
selected_category = st.selectbox(
    "Filtrar por categoría:",
    ["todos", "vestidos", "blusas", "pantalones", "zapatos", "accesorios"],
    index=0
)

# Mostrar productos
products = get_products()

if selected_category != "todos":
    products = [p for p in products if p.get('category') == selected_category]

if not products:
    st.warning("No hay productos disponibles en esta categoría")
else:
    # Mostrar 3 productos por fila
    cols = st.columns(3)
    
    for idx, product in enumerate(products):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{product['image']}" alt="{product['name']}" style="width:100%; height:200px; object-fit:cover; border-radius:10px;">
                <h3 style="margin:1rem 0 0.5rem 0; color:#333;">{product['name']}</h3>
                <p style="color:#666; margin-bottom:1rem;">{product['description']}</p>
                <div class="price-tag">${product['price']:.2f}</div>
                <p style="color:#999; font-size:0.9rem;">Stock: {product['stock']} unidades</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🛒 Añadir al carrito", key=f"add_{product['id']}", use_container_width=True):
                if add_to_cart(product):
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:2rem;">
    <p>🛍️ Fashion Store - Tu estilo, nuestra pasión</p>
</div>
""", unsafe_allow_html=True)
