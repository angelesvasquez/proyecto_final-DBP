# Proyecto Flask: Sistema de Compras

Este proyecto es una plataforma de compras donde los usuarios pueden registrarse, iniciar sesión, gestionar su cuenta, ver productos y agregar artículos a su carrito de compras. Además de tener un panel de administrador para gestionar productos, usuarios y ver pedidos.

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

---
## Funcionalidades para el Administrador

### 1. **Inicio de Sesión del Administrador**
Los administradores inician sesión proporcionando su nombre de usuario y contraseña:
- Si las credenciales son correctas y el rol es `id_rol = 1`, se establece una sesión activa.
- El administrador puede acceder al panel de administración.

### 2. **Panel de Administración**
Acceso exclusivo para administradores. Desde este panel, el administrador puede:
- **Gestionar productos**: Agregar, modificar o eliminar productos.
- **Gestionar usuarios**: Modificar o eliminar usuarios.
- **Ver pedidos**: Ver todos los pedidos realizados por los usuarios.

### 3. **Gestión de Productos**
El administrador puede:
- Agregar productos con nombre, descripción, precio, estado, descuento y una imagen.
- Modificar productos existentes.
- Eliminar productos de la base de datos.

### 4. **Gestión de Usuarios**
El administrador puede:
- Modificar datos de usuarios (email, teléfono).
- Eliminar usuarios, eliminando también su carrito de compras.

### 5. **Visualización de Pedidos**
El administrador puede ver todos los pedidos realizados en la plataforma.
- Productos comprados
- Cliente que realizo la compra
- Fecha del pedido
- Precio Total

---
