from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#COEXION A MYSQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "tarea"
mysql = MySQL(app)

#CONFIGURACIONES
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente')
    data = cur.fetchall()
    print(data)
    curs = mysql.connection.cursor()
    curs.execute('SELECT * FROM producto')
    dat = curs.fetchall()
    print(dat)
    curso = mysql.connection.cursor()
    curso.execute('SELECT * FROM pedido')
    uwu = curso.fetchall()
    print(uwu)
    return render_template('index.html', clientes = data, productos = dat, pedidos = uwu)


#ingreso de datos a las distintas tablas------------------
@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        flash('Cliente Ingresado Correctamente')
        cur.execute('INSERT INTO cliente (cedula, nombres, apellidos, direccion) VALUES (%s, %s, %s,%s)',
        (cedula, nombres, apellidos,direccion))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO producto (nombre, precio) VALUES (%s, %s)',
        (nombre, precio))
        flash('Producto Ingresado Correctamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/add_pedido', methods=['POST'])
def add_pedido():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        producto = request.form['producto']
        cantidad = request.form['cantidad']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO pedido (id_cliente,producto,cantidad) VALUES (%s, %s, %s)',
        (id_cliente, producto, cantidad))
        flash('Pedido Ingresado Correctamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))
        
#ACTUALIZACIONES EN LAS TABLAS------------------------------------------------------

@app.route('/edit_Cliente/<cedula>')
def get_cliente(cedula):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE cedula = {0}'.format(cedula))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-Cliente.html', cliente = data[0])


@app.route("/delete_Cliente/<string:cedula>")
def delete_cliente(cedula):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cliente WHERE cedula = {0}'.format(cedula))
    mysql.connection.commit()
    flash('Cliente eliminado correctamente')
    return redirect(url_for('Index'))

@app.route('/edit_Producto/<id_producto>')
def get_producto(id_producto):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE id_produto = %s', (id_producto))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-Producto.html', producto = data[0])

@app.route("/delete_Producto/<id_producto>")
def delete_producto(id_producto):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM producto WHERE id_produto = {0}'.format(id_producto))
    mysql.connection.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('Index'))

@app.route('/edit_Pedido/<id_pedido>')
def get_pedido(id_pedido):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pedido WHERE id_pedido = %s', (id_pedido))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-Pedido.html', pedido = data[0])

@app.route("/delete_Pedido/<id_pedido>")
def delete_pedido(id_pedido):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pedido WHERE id_pedido = {0}'.format(id_pedido))
    mysql.connection.commit()
    flash('Pedido eliminado correctamente')
    return redirect(url_for('Index'))

#-----------------------------------------------------------------------
@app.route('/update_Cliente/<cedula>', methods = ['POST'])
def update_cliente(cedula):
    if request.method == 'POST':   
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        direccion = request.form['direccion']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE cliente
            SET nombres = %s,
            apellidos = %s,
            direccion = %s
            WHERE cedula = %s
        """, (nombres, apellidos, direccion, cedula))
        mysql.connection.commit()
        flash('Cliente actualizado exitosamente')
        return redirect(url_for('Index'))

@app.route('/update_Producto/<id_producto>', methods = ['POST'])
def update_producto(id_producto):
    if request.method == 'POST':   
        nombre = request.form['nombre']
        precio = request.form['precio']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE producto
            SET nombre = %s,
            precio = %s
            WHERE id_produto = %s
        """, (nombre, precio, id_producto))
        mysql.connection.commit()
        flash('Producto actualizado exitosamente')
        return redirect(url_for('Index'))
        
if __name__ == '__main__':
    app.run(port = 3000, debug = True)