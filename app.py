import os
from flask import Flask, render_template, redirect, request, flash
from flask import Response, session, url_for, jsonify
from flask_mysqldb import MySQL
import bcrypt #para el hashing del password
import hashlib
import re

app = Flask(__name__)

MONEDA = 'S/. '
KEY_TOKEN = 'APR.wqc-354*'
app.secret_key = 'user54321'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "alpamayo"

mysql = MySQL(app)

def generate_token(id):
    token = f"{id}{KEY_TOKEN}"
    return hashlib.sha1(token.encode()).hexdigest()

def verify_token(id, token):
    return generate_token(id) == token

# ------------------ Rutas para el usuario ------------------

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario, usuario, password, id_rol FROM usuarios WHERE usuario = %s", (usuario,))
        cuenta = cur.fetchone()
        if cuenta:
            hashed_password = cuenta[2]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                session['id_rol'] = cuenta[3]
                if session['id_rol'] == 2: #Verificamos que sea cliente
                    session['logueado'] = True
                    session['id_usuario'] = cuenta[0]
                    flash("Ingreso exitoso.", "success")
                    session['nombre_completo'] = f"{cuenta[1]}"
                    cur.execute("SELECT id_producto, cantidad FROM carrito WHERE id_cliente = %s", (cuenta[0],))
                    carrito = cur.fetchall()
                    session['carrito'] = [{'producto_id': item[0], 'cantidad': item[1]} for item in carrito]
                    return redirect(url_for('catalogo'))
                else: 
                    flash("Ingreso exclusivo para usuarios.", "danger")
                    
            else:
                flash("Usuario o contraseña incorrectos.", "danger")
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
        cur.close()
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        datos = {
            'nombres': request.form['nombres'],
            'apellidos': request.form['apellidos'],
            'email': request.form['email'],
            'telefono': request.form['telefono'],
            'dni': request.form['dni'],
            'usuario': request.form['usuario'],
            'password': request.form['password'],
            'repassword': request.form['repassword']
        }

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', datos['nombres']):
            flash("El campo 'Nombres' no puede contener números ni caracteres especiales.", "danger")
            return render_template('registro.html', datos=datos)

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', datos['apellidos']):
            flash("El campo 'Apellidos' no puede contener números ni caracteres especiales.", "danger")
            return render_template('registro.html', datos=datos)

        if datos['password'] != datos['repassword']:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template('registro.html', datos=datos)

        cur = mysql.connection.cursor()
        
        cur.execute("SELECT * FROM usuarios WHERE usuario = %s", [datos['usuario']])
        if cur.fetchone():
            flash("El nombre de usuario ya está en uso.", "danger")
            return render_template('registro.html', datos=datos)

        cur.execute("SELECT * FROM usuarios WHERE email = %s", [datos['email']])
        if cur.fetchone():
            flash("El email ya está en uso.", "danger")
            return render_template('registro.html', datos=datos)

        hashed_password = bcrypt.hashpw(datos['password'].encode('utf-8'), bcrypt.gensalt())
        
        datos_finales = (
            datos['nombres'], datos['apellidos'], datos['email'], datos['telefono'], 
            datos['dni'], 1, 'CURRENT_TIMESTAMP', datos['usuario'], hashed_password
        )

        cur.execute(
            "INSERT INTO usuarios (nombres, apellidos, email, telefono, dni, estatus, fecha_atta, usuario, password) "
            "VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)", 
            datos_finales
        )
        mysql.connection.commit()
        cur.close()

        flash("Registro exitoso. Puedes iniciar sesión ahora.", "success")
        return redirect(url_for('login'))  
    
    datos = {
        'nombres': '',
        'apellidos': '',
        'email': '',
        'telefono': '',
        'dni': '',
        'usuario': '',
        'password': '',
        'repassword': ''
    }
    return render_template('registro.html', datos=datos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/mi_cuenta')
def mi_cuenta():
    if 'logueado' not in session: 
        flash('Debes iniciar sesión para ver tu cuenta.', 'warning')
        return redirect(url_for('login'))
    id_usuario = session['id_usuario']
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombres, apellidos, email, telefono, usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    cliente = cur.fetchone()
    cur.close()

    if cliente:
        info_cliente = {
            'nombres': cliente[0],
            'apellidos': cliente[1],
            'email': cliente[2],
            'telefono': cliente[3],
            'usuario': cliente[4],
        }
        return render_template('mi_cuenta.html', cliente=info_cliente)
    else:
        flash('No se encontro información de tu cuenta', 'danger')
        return redirect(url_for('index'))

def validar_datos_cuenta(nombres, apellidos, email, telefono, usuario):
    errores = {}

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombres):
        errores['nombres'] = "El nombre solo puede contener letras y espacios."

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellidos):
        errores['apellidos'] = "El apellido solo puede contener letras y espacios."
    
    if '@' not in email or '.' not in email or email.startswith('@') or email.endswith('@'):
        errores['email'] = "El email no es válido."
    
    if telefono and (not telefono.isdigit() or len(telefono) < 8 or len(telefono) > 15):
        errores['telefono'] = "El teléfono debe contener entre 8 y 15 dígitos numéricos."
    
    if not all(c.isalnum() or c == '_' for c in usuario):
        errores['usuario'] = "El usuario solo puede contener letras, números y guiones bajos."
    
    if not nombres or not apellidos or not email or not usuario:
        errores['vacio'] = "Todos los campos son obligatorios."

    return errores

@app.route('/editar_cuenta', methods=['GET', 'POST'])
def editar_cuenta():
    id_usuario = session['id_usuario']
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        
        # Validar los datos
        errores = validar_datos_cuenta(nombres, apellidos, email, telefono, usuario)

        if errores:
            for error in errores.values():
                flash(error, 'danger')
            return render_template('editar_cuenta.html', cliente=request.form)

        # Verificar si el correo ya está registrado en la BD
        cur.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s AND id_usuario != %s", (email, id_usuario))
        email_existente = cur.fetchone()[0]

        if email_existente > 0:
            flash('Este correo electrónico ya está registrado en otra cuenta.', 'danger')
            return render_template('editar_cuenta.html', cliente=request.form)
        
        #Verificar si el usuario ya esta registrado en la BD
        cur.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = %s AND id_usuario != %s", (usuario, id_usuario))
        existe_usuario = cur.fetchone()[0]
        if existe_usuario > 0:
            flash("El nombre de usuario ya está registrado. Por favor, elige otro.", "danger")
            return render_template('editar_cuenta.html', cliente=request.form)
        
        cur.execute("""
            UPDATE usuarios 
            SET nombres = %s, apellidos = %s, email = %s, telefono = %s, usuario = %s, fecha_modifica = CURRENT_TIMESTAMP
            WHERE id_usuario = %s
        """, (nombres, apellidos, email, telefono, usuario, id_usuario))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('mi_cuenta'))

    cur.execute("SELECT nombres, apellidos, email, telefono, usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    cliente = cur.fetchone()
    cur.close()

    if cliente:
        info_cliente = {
            'nombres': cliente[0],
            'apellidos': cliente[1],
            'email': cliente[2],
            'telefono': cliente[3],
            'usuario': cliente[4],
        }
        return render_template('editar_cuenta.html', cliente=info_cliente)
    else:
        flash('No se encontró información de tu cuenta', 'danger')
        return redirect(url_for('index'))
    

# ------------------ Catalogo de productos ------------------

@app.route('/catalogo')
def catalogo():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, precio_base, precio_final, descuento  FROM productos WHERE activo = 1")
    resultados = cur.fetchall()
    MONEDA = 'S/.'
    productos = []

    for row in resultados:
        id = row[0]
        nombre = row[1]
        precio_base = row[2]
        precio_final = row[3]
        descuento = row[4]
        imagen = f"img/productos/{id}/item.png"
        imagen_path = os.path.join('static', imagen)
        if not os.path.exists(imagen_path):
            imagen = "img/no-imagen.jpg"
        token = generate_token(id)
        productos.append({'id': id, 'nombre': nombre, 'precio_base': precio_base, 'precio_final': precio_final, 'descuento': descuento, 'imagen': imagen, 'token': token })
    cur.close()

    return render_template('catalogo.html', productos=productos, MONEDA=MONEDA )

@app.route('/producto/<int:id>/<token>')
def detalles_producto(id, token):
    if not verify_token(id, token):
        flash("Error al procesar la petición", "danger")
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, descripcion, precio_base, precio_final, descuento FROM productos WHERE id = %s AND activo = 1 LIMIT 1", (id,))
    row = cur.fetchone()

    if row:
        nombre = row[1]
        descripcion = row[2]
        precio_base = row[3]
        precio_final = row[4]
        descuento = row[5]
        imagen = f"img/productos/{id}/item.png"
        imagen_path = os.path.join('static', imagen)
        if not os.path.exists(imagen_path):
            imagen = "img/no-imagen.jpg"
    else:
        flash("Producto no encontrado", "warning")
        return redirect(url_for('catalogo'))

    cur.close()
    
    return render_template('detalles_producto.html', MONEDA=MONEDA, nombre=nombre, precio_final=precio_final, precio_base=precio_base, descuento=descuento, descripcion=descripcion, imagen=imagen, id=id)

# ------------------ Rutas para el carrito ------------------

@app.route('/carrito')
def mostrar_carrito():
    if 'logueado' not in session:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('login'))
    id_usuario = session['id_usuario']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_producto, cantidad FROM carrito WHERE id_cliente = %s", (id_usuario,))
    productos_carrito = cur.fetchall()
    carrito = []
    total_carrito = 0
    for producto_carrito in productos_carrito:
        id_producto = producto_carrito[0]
        cantidad = producto_carrito[1]
        cur.execute("SELECT id, nombre, precio_final FROM productos WHERE id = %s", (id_producto,))
        producto = cur.fetchone()
        if producto:
            total = producto[2] * cantidad
            carrito.append({
                'id': producto[0],
                'nombre': producto[1],
                'precio_final': producto[2],
                'cantidad': cantidad,
                'total': total
            })
            total_carrito += total
    cur.close()
    return render_template('carrito.html', carrito=carrito, total_carrito=total_carrito, MONEDA=MONEDA)

@app.route('/carrito/agregar', methods=['POST'])
def agregar_producto_carrito():
    if 'logueado' not in session:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('login'))
    id_usuario = session['id_usuario']
    id_producto = request.form.get('id_producto')
    cantidad = request.form.get('cantidad', 1)
    cur = mysql.connection.cursor()
    cur.execute("SELECT cantidad FROM carrito WHERE id_cliente = %s AND id_producto = %s", (id_usuario, id_producto))
    producto_en_carrito = cur.fetchone()
    if producto_en_carrito:
        nueva_cantidad = producto_en_carrito[0] + int(cantidad)
        cur.execute("UPDATE carrito SET cantidad = %s WHERE id_cliente = %s AND id_producto = %s", (nueva_cantidad, id_usuario, id_producto))
    else:
        cur.execute("INSERT INTO carrito (id_cliente, id_producto, cantidad) VALUES (%s, %s, %s)", (id_usuario, id_producto, cantidad))
    mysql.connection.commit()
    cur.close()
    flash('Producto agregado al carrito.', 'success')
    return redirect(url_for('catalogo'))

@app.route('/carrito/eliminar/<int:id_producto>', methods=['POST'])
def eliminar_producto_carrito(id_producto):
    if 'logueado' not in session:
        flash('Debes iniciar sesión para modificar tu carrito.', 'warning')
        return redirect(url_for('login'))
    id_usuario = session['id_usuario']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito WHERE id_cliente = %s AND id_producto = %s", (id_usuario, id_producto))
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('mostrar_carrito'))

@app.route('/carrito/actualizar/<int:id_producto>', methods=['POST'])
def actualizar_cantidad_producto_carrito(id_producto):
    if 'logueado' not in session:
        flash('Debes iniciar sesión para modificar tu carrito.', 'warning')
        return redirect(url_for('login'))
    
    nueva_cantidad = request.form.get('nueva_cantidad', type=int)
    
    if nueva_cantidad <= 0:
        flash('La cantidad debe ser mayor que 0.', 'danger')
        return redirect(url_for('mostrar_carrito'))

    id_usuario = session['id_usuario']
    cur = mysql.connection.cursor()

    # Actualizar la cantidad del producto en el carrito
    cur.execute("UPDATE carrito SET cantidad = %s WHERE id_cliente = %s AND id_producto = %s", (nueva_cantidad, id_usuario, id_producto))
    mysql.connection.commit()
    cur.close()

    flash('Cantidad actualizada con éxito.', 'success')
    return redirect(url_for('mostrar_carrito'))

#------------ ruta para verificaion final--------------------------
@app.route('/verif_final')
def verif_final():
    if 'logueado' not in session:
        flash('Debes iniciar sesión para proceder con el pago.', 'warning')
        return redirect(url_for('login'))
    
    id_usuario = session['id_usuario']

    # Obtener los datos del cliente
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombres, apellidos, email, telefono FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    cliente = cur.fetchone()

    # Obtener los productos en el carrito
    cur.execute("SELECT id_producto, cantidad FROM carrito WHERE id_cliente = %s", (id_usuario,))
    productos_carrito = cur.fetchall()
    carrito = []
    total_carrito = 0
    for producto_carrito in productos_carrito:
        id_producto = producto_carrito[0]
        cantidad = producto_carrito[1]
        cur.execute("SELECT nombre, precio_final FROM productos WHERE id = %s", (id_producto,))
        producto = cur.fetchone()
        if producto:
            total = producto[1] * cantidad
            carrito.append({
                'nombre': producto[0],
                'precio_final': producto[1],
                'cantidad': cantidad,
                'total': total
            })
            total_carrito += total
    cur.close()

    return render_template('verif_final.html', carrito=carrito, total_carrito=total_carrito, MONEDA=MONEDA, cliente={
        'nombres': cliente[0],
        'apellidos': cliente[1],
        'email': cliente[2],
        'telefono': cliente[3]
    })

@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    if 'logueado' not in session:
        flash('Debes iniciar sesión para realizar el pedido.', 'warning')
        return redirect(url_for('login'))

    id_usuario = session['id_usuario']
    
    # Obtener el carrito del cliente
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_producto, cantidad FROM carrito WHERE id_cliente = %s", (id_usuario,))
    productos_carrito = cur.fetchall()

    # Insertar el pedido en la tabla de pedidos
    for producto_carrito in productos_carrito:
        id_producto = producto_carrito[0]
        cantidad = producto_carrito[1]
        cur.execute("SELECT precio_final FROM productos WHERE id = %s", (id_producto,))
        producto = cur.fetchone()
        if producto:
            total = producto[0] * cantidad
            cur.execute("INSERT INTO pedidos (id_cliente, id_producto, fecha_pedido, total) VALUES (%s, %s, NOW(), %s)", 
                        (id_usuario, id_producto, total))
    mysql.connection.commit()

    # Vaciar el carrito
    cur.execute("DELETE FROM carrito WHERE id_cliente = %s", (id_usuario,))
    mysql.connection.commit()
    cur.close()

    flash('Pedido realizado con éxito.', 'success')
    return redirect(url_for('index'))

# ------------------          Administrador             ------------------
# ------------------ Rutas para la Gestión de Productos ------------------

import os
from werkzeug.utils import secure_filename

@app.route('/admin')
def admin():
    if 'logueado' in session and session.get('id_rol') == 1:
        return render_template('admin.html')
    else:
        flash("Debes iniciar sesión como administrador para acceder al panel.", "warning")
        return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        cur = mysql.connection.cursor()
        # Verificamos si el usuario es un administrador
        cur.execute("SELECT id_usuario, password, id_rol FROM usuarios WHERE usuario = %s", (usuario,))
        admin = cur.fetchone()
        cur.close()
        if admin:
            id_usuario = admin[0]
            hashed_password = admin[1]
            id_rol = admin[2]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')) and id_rol == 1:
                session['logueado'] = True
                session['id_usuario'] = id_usuario
                session['id_rol'] = id_rol
                return redirect(url_for('admin')) 
            else:
                flash("Usuario o contraseña incorrectos o no tienes permisos de administrador.", "danger")
        else:
            flash("Usuario no encontrado.", "danger")

    return render_template('admin_login.html')

@app.route('/admin/agregar-producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio_base = request.form['precio']
        activo = 1 if 'activo' in request.form else 0
        descuento = request.form['descuento']
        
        # Guardar el producto sin imagen primero para obtener el ID
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (nombre, descripcion, precio_base, activo, descuento) VALUES (%s, %s, %s, %s, %s)", 
                    (nombre, descripcion, precio_base, activo, descuento))
        mysql.connection.commit()
        producto_id = cur.lastrowid  # Obtener el ID del producto recién insertado

        # Verificar si se subió una imagen
        imagen = request.files.get('imagen')
        if imagen and imagen.filename != '':
            # Crear la carpeta para el producto si no existe
            carpeta_producto = os.path.join('static', 'img', 'productos', str(producto_id))
            if not os.path.exists(carpeta_producto):
                os.makedirs(carpeta_producto)
            
            # Guardar la imagen como item.png dentro de la carpeta del producto
            imagen_path = os.path.join(carpeta_producto, 'item.png')
            imagen.save(imagen_path)

        # Actualizar el producto con la ruta de la imagen si se subió
        if imagen:
            cur.execute("UPDATE productos SET imagen = 'item.png' WHERE id = %s", (producto_id,))
            mysql.connection.commit()

        cur.close()
        
        flash("Producto agregado con éxito.", "success")
        return redirect(url_for('agregar_producto'))
    return render_template('agregar_producto.html')

@app.route('/admin/modificar-eliminar-producto', methods=['GET', 'POST'])
def modificar_eliminar_producto():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if 'modificar' in request.form:
            id_producto = request.form['id_producto']
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio_base = request.form['precio']
            activo = 1 if 'activo' in request.form else 0
            descuento = request.form['descuento']

            # Verificar si se subió una nueva imagen
            nueva_imagen = request.files.get('nueva_imagen')
            if nueva_imagen and nueva_imagen.filename != '':
                # Crear la carpeta para el producto si no existe
                carpeta_producto = os.path.join('static', 'img', 'productos', str(id_producto))
                if not os.path.exists(carpeta_producto):
                    os.makedirs(carpeta_producto)
                
                # Guardar la imagen como item.png dentro de la carpeta del producto
                imagen_path = os.path.join(carpeta_producto, 'item.png')
                nueva_imagen.save(imagen_path)

            # Actualizar los datos del producto
            cur.execute("""
                UPDATE productos 
                SET nombre = %s, descripcion = %s, precio_base = %s, activo = %s, descuento = %s
                WHERE id = %s
            """, (nombre, descripcion, precio_base, activo, descuento, id_producto))

            mysql.connection.commit()
            flash("Producto modificado con éxito.", "success")
        elif 'eliminar' in request.form:
            id_producto = request.form['id_producto']
            cur.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
            mysql.connection.commit()
            flash("Producto eliminado con éxito.", "success")

    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()
    return render_template('modificar_eliminar_producto.html', productos=productos)


# ------------------ Rutas para la Gestión de Usuarios ------------------

@app.route('/admin/modificar-eliminar-usuario', methods=['GET', 'POST'])
def modificar_eliminar_usuario():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if 'modificar' in request.form:
            id_usuario = request.form['id_usuario']
            nuevo_email = request.form['nuevo_email']
            nuevo_telefono = request.form['nuevo_telefono']
            cur.execute("UPDATE usuarios SET email = %s, telefono = %s WHERE id_usuario = %s", (nuevo_email, nuevo_telefono, id_usuario))
            mysql.connection.commit()
            flash("Usuario modificado con éxito.", "success")
        elif 'eliminar' in request.form:
            id_usuario = request.form['id_usuario']
            cur.execute("DELETE FROM carrito WHERE id_cliente = %s", (id_usuario,))
            cur.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            mysql.connection.commit()
            flash("Usuario eliminado con éxito.", "success")
    cur.execute("SELECT id_usuario, usuario, email, telefono FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('modificar_eliminar_usuario.html', usuarios=usuarios)

# ------------------ Ruta para Ver Pedidos ------------------

@app.route('/admin/ver-pedidos')
def ver_pedidos():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT pedidos.id, productos.nombre, usuarios.usuario, pedidos.fecha_pedido, pedidos.total 
        FROM pedidos 
        JOIN productos ON pedidos.id_producto = productos.id 
        JOIN usuarios ON pedidos.id_cliente = usuarios.id_usuario
    """)
    pedidos = cur.fetchall()
    cur.close()
    return render_template('ver_pedidos.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(debug=True)
