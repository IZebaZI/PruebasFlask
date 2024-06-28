from flask import Flask, request, render_template, jsonify, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdmedicos'
app.secret_key = 'your_secret_key'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/formulario_medicos")
def formMedicos():
    return render_template("formMedicos.html")

@app.route("/lista_medicos")
def listMedicos():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from medicos')
        listaMedicos = cursor.fetchall()
        return render_template('listaMedicos.html', medicos = listaMedicos)
    except Exception as e:
        print(e)

@app.route("/guardar_medicos", methods=['POST'])
def insertMedicos():
    if request.method == 'POST':
        rfc = request.form['txtRFC']
        nombre = request.form['txtNombre']
        cedula = request.form['txtCedula']
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        rol = request.form['txtRol']
        numeroConsultorio = request.form['intNumeroConsultorio']
        
        print(rfc, nombre, cedula, correo, password, rol, numeroConsultorio)
        
        cursor = mysql.connection.cursor()
        cursor.execute('insert into medicos(rfc, nombre, cedula, correo, password, rol, numeroConsultorio) values(%s, %s, %s, %s, %s, %s, %s)', (rfc, nombre, cedula, correo, password, rol, numeroConsultorio))
        mysql.connection.commit()
        
        flash('')
        
    return redirect(url_for('formMedicos'))

@app.errorhandler(404)
def paginaerror(e):
    return 'Revisa tu sintaxis: No encontré la página especificada'

if __name__ == '__main__':
    app.run(port=3000, debug=True)