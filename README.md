
# 🛒 Fashion Store Ecommerce App

Una aplicación de **e-commerce moderna y elegante** desarrollada con **Streamlit**, que ofrece una experiencia de compra premium con autenticación, carrito inteligente y pagos seguros.

🌐 **Aplicación desplegada (Streamlit App):** [Ver app aquí](https://fashion-store-app.streamlit.app)

---

## ✨ Características Principales

- 🔐 **Autenticación OAuth con Google**: Inicio de sesión seguro y sin fricciones.
- 🛒 **Carrito de Compras Inteligente**: Gestión de productos con persistencia en tiempo real.
- 💳 **Procesamiento de Pagos**: Integración con **Stripe API** para pagos seguros.
- 📱 **Diseño Responsive**: Interfaz moderna adaptada a todos los dispositivos.
- 🔥 **Base de Datos Firebase**: Almacenamiento seguro de usuarios, productos y órdenes.
- 📊 **Gestión de Inventario**: Control automático de stock tras cada compra.
- 🎨 **UI/UX Premium**: Estilos personalizados con CSS.

---

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Streamlit + HTML/CSS personalizado
- **Backend**: Python
- **Base de Datos**: Firebase Firestore
- **Autenticación**: Google OAuth 2.0
- **Pagos**: Stripe API
- **Almacenamiento**: Firebase Storage
- **Deployment**: Streamlit Cloud

---

## 📁 Estructura del Proyecto

```
fashion-store/
├── app.py                 # Página principal y autenticación
├── pages/
│   ├── catalogo.py       # Catálogo de productos y carrito
│   └── compraok.py       # Confirmación de compra
├── estilos/
│   ├── css_login.html    # Estilos para login
│   ├── css_catalogo.html # Estilos para catálogo
│   └── css_compra.html   # Estilos para compra
├── serviceAccountKey.json # Credenciales Firebase
├── payment_utils.py       # Lógica de pagos (Stripe)
├── .env                  # Variables de entorno
├── requirements.txt      # Dependencias Python
└── README.md              # Documentación del proyecto
```

---

## 🚀 Instalación y Ejecución Local

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/BootcampXperience/DS_Ecommerce_Web_Platform.git
   cd DS_Ecommerce_Web_Platform
   ```

2. **Crea un entorno virtual e instala las dependencias:**
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configura tu archivo `.env` con las claves necesarias:**
   ```
   GOOGLE_CLIENT_ID=tu_google_client_id
   GOOGLE_SECRET_ID=tu_google_secret_id
   STRIPE_SECRET_KEY=tu_stripe_secret_key
   ```

4. **Configurar Firebase**
   - Descargar `serviceAccountKey.json` desde Google Console
   - Colocar el archivo en la raíz del proyecto
   - Configurar las reglas de Firestore

5. **Ejecuta la aplicación:**
   ```bash
   streamlit run app.py
   ```

---

## 🎯 Funcionalidades

### Autenticación
- Login con Google OAuth 2.0
- Creación automática de usuarios
- Gestión de sesiones segura

### Catálogo
- Visualización de productos con imágenes
- Filtrado por categorías
- Información detallada de stock

### Carrito de Compras
- Agregar/quitar productos
- Persistencia en Firebase
- Cálculo automático de totales

### Procesamiento de Pagos
- Integración con Stripe Checkout
- Manejo de pagos exitosos/cancelados

### Gestión de Órdenes
- Guardado automático en Firebase
- Actualización de inventario
- Número de orden único

## 💳 Simulación de Pagos con Stripe
Esta aplicación emplea una cuenta de prueba de Stripe. Para simular el proceso de pago, se pueden utilizar los siguientes datos en el formulario proporcionado por Stripe:

✅ **Pago Exitoso (Aprobado)**

- **Número de tarjeta:** `4242 4242 4242 4242`
- **Fecha de expiración:** `12/25` (o cualquier fecha futura)
- **CVC:** `123`
- **Nombre:** Cualquier nombre válido
- **País:** Cualquier país válido

❌ **Pago Fallido (Rechazado)**

- **Número de tarjeta:** `4000 0000 0000 0002`
- Los demás campos pueden llenarse igual que en el caso exitoso.

## 🚀 Deployment

### Streamlit Cloud
1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. Subir archivos de configuración
4. Desplegar aplicación

## 🛡️ Seguridad

- ✅ Autenticación OAuth 2.0
- ✅ Validación de datos server-side
- ✅ Encriptación de datos sensibles
- ✅ Manejo seguro de tokens
- ✅ Validación de pagos con Stripe

---

## 📸 Capturas de pantalla

Puedes agregar imágenes aquí para mostrar:
- **Página de inicio / login**
  <img width="1917" height="1070" alt="IMAGEN_2" src="https://github.com/user-attachments/assets/262bfd2b-5097-44e5-9dd0-df22eea28c4f" />

- **Catálogo de productos**
  <img width="1906" height="1066" alt="IMAGEN_3" src="https://github.com/user-attachments/assets/6b5c91ec-cfae-4cb7-93c3-28d63495aa92" />

- **Checkout en Stripe**
  <img width="1904" height="1064" alt="IMAGEN_4" src="https://github.com/user-attachments/assets/4a16ba0f-070d-4213-913c-e4e75b1169b1" />

- **Confirmación de compra**
  <img width="1909" height="1065" alt="IMAGEN_5" src="https://github.com/user-attachments/assets/ca4c34d5-1f54-40ab-9faf-abbdc38084a2" />



---

## 👨‍💼 Autor

**Frans Benavides**

📧 [jjfj2011@gmail.com]

💼 [www.linkedin.com/in/frans-benavides]
