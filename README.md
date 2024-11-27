## Flujo del Proceso de Inicio de Sesión

### 1. Ruta para Administradores (`/admin`)

- Los administradores deben acceder al sistema a través de la ruta `/admin`.
- En la ruta `/admin`, los administradores ingresan su **usuario** y **contraseña**.
- El sistema valida las credenciales contra la base de datos y verifica que el usuario sea un **administrador**.
- Si las credenciales son correctas, el administrador es redirigido al panel de administración (`/admin/dashboard`).
- Si las credenciales son incorrectas o el usuario no es un administrador, se muestra un mensaje de error.

### 2. Ruta para Clientes (Login Normal)

- Los clientes acceden al sistema mediante la página de inicio de sesión en la ruta principal.
- En esta página, los clientes ingresan su **usuario** y **contraseña**.
- El sistema valida las credenciales y verifica que el usuario no sea un administrador.
- Si las credenciales son correctas y el usuario es un cliente, se redirige al panel de clientes (`/client/dashboard`).
- Si el usuario es un administrador, el inicio de sesión es rechazado y se muestra un mensaje de error.
