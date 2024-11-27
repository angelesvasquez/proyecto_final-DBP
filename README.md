# Proyecto Flask: Sistema de Compras

Este proyecto es una plataforma de compras donde los usuarios pueden registrarse, iniciar sesión, gestionar su cuenta, ver productos y agregar artículos a su carrito de compras.

## Funcionalidades del Cliente

### 1. **Registro de Usuario**
Los usuarios pueden registrarse en la plataforma proporcionando:
- Nombres
- Apellidos
- Email
- Teléfono
- DNI
- Usuario
- Contraseña (y confirmación de contraseña)

Validaciones:
- Los campos de nombres y apellidos solo pueden contener letras y espacios.
- Las contraseñas deben coincidir.
- El email y el nombre de usuario deben ser únicos.
- Los datos se guardan de manera segura con hashing en la base de datos.

### 2. **Inicio de Sesión**
Los usuarios pueden iniciar sesión proporcionando su nombre de usuario y contraseña:
- Si la contraseña es correcta, el sistema verifica si el usuario es un cliente (rol 2).
- Si es cliente, se almacena en la sesión su ID y rol.
- También se carga el carrito de compras del usuario, si tiene productos.

### 3. **Mi Cuenta**
Los usuarios pueden acceder a su cuenta para ver su información personal (nombres, apellidos, email, teléfono, usuario). Si no están logueados, se les redirige a la página de inicio de sesión.

### 4. **Edición de Cuenta**
Los usuarios pueden editar su información personal, como nombres, apellidos, email, teléfono y usuario:
- Se validan los nuevos datos antes de actualizar en la base de datos.
- Si el email o el usuario ya están registrados en otro perfil, se muestra un mensaje de error.

### 5. **Catálogo de Productos**
Los usuarios pueden ver una lista de productos disponibles con:
- Nombre
- Precio
- Descuento (si aplica)
- Imagen (si existe)

Cada producto tiene un enlace que lleva a su detalle individual.

### 6. **Detalles del Producto**
Los usuarios pueden ver los detalles de cada producto, incluyendo:
- Nombre
- Descripción
- Precio base
- Precio final
- Descuento
- Imagen

### 7. **Carrito de Compras**
Los usuarios pueden gestionar su carrito de compras:
- Ver los productos en el carrito, junto con el precio total.
- Agregar productos al carrito.
- Eliminar productos del carrito.
- Actualizar la cantidad de productos en el carrito.

### 8. **Cierre de Sesión**
Los usuarios pueden cerrar sesión en cualquier momento, lo que limpia los datos de la sesión y los redirige a la página principal.
