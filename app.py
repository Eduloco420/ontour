# Importación de bibliotecas necesarias para la aplicación
from flask import Flask, jsonify, request, send_file # Para manejar solicitudes y respuestas HTTP
from flask_mysqldb import MySQL # Para conectar con MySQL
import pagos, alumnos, seguros, cursos, paquetes, viaje, alumnosXapoderado # Módulos personalizados donde tengo métodos
import pandas as pd # Para manejar datos en formato Excel
import os
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

# Inicialización de la conexión con la base de datos MySQL
conexion = MySQL(app)

# Crear la carpeta de almacenamiento si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/home')
def home():
    return jsonify({"message":"Bienvenido a mi BackEnd"})

# Ruta para listar pagos
@app.route('/pagos', methods=['GET'])
def listar_pagos():
    return pagos.get_pagos(conexion) # Llama al método en el módulo pagos para obtener los datos de pagos

# Ruta para listar alumnos    
@app.route('/alumnos', methods=['GET'])
def lista_alumnos():
    return alumnos.get_alumnos(conexion)

# Ruta para listar seguros
@app.route('/seguros', methods=['GET'])
def listar_seguro():
    return seguros.get_seguros(conexion)

# Ruta para listar cursos
@app.route('/cursos', methods=['GET'])
def listar_cursos():
    return cursos.get_curso(conexion)

# Ruta para agregar un nuevo curso
@app.route('/cursos', methods=['POST'])
def agregar_curso():
    try:

        conexion.connection.begin()
        # Verifica que los archivos requeridos estén en la solicitud
        if 'Planilla' not in request.files:
            return jsonify({'error': 'No se ha enviado un archivo'}), 400
        if 'contrato' not in request.files:
            return jsonify({'error': 'No se ha enviado un archivo'}), 400 
        
        # Carga los archivos y datos enviados en la solicitud
        Planilla = request.files['Planilla']
        contrato = request.files['contrato']
        xlsx_df = pd.read_excel(Planilla, sheet_name='Alumnos') # Carga la planilla Excel
        nomCurso = request.form.get('nomCurso')
        nomColegio = request.form.get('nomColegio')
        paqueteTuristico = request.form.get('paqueteTuristico')
        seguro = request.form.get('seguro')
        cantAlumnos = len(xlsx_df) # Cuenta la cantidad de alumnos en la planilla
        fechaViaje = request.form.get('fechaViaje')
        
        # Inserta el curso en la base de datos
        cursoId = cursos.post_curso(conexion, contrato, nomCurso ,nomColegio ,paqueteTuristico ,seguro ,cantAlumnos, app, fechaViaje)
        valorCuotaAlumno = paquetes.valor_paquete(conexion, paqueteTuristico, cantAlumnos)
        listaAlumnos = alumnos.cargar_alumnos(conexion=conexion, cursoId=cursoId, xlsx_df=xlsx_df, valorCuotaAlumno=valorCuotaAlumno)
        # Confirma los cambios en la base de datos
        conexion.connection.commit()

        return f'Se ha creado el curso {nomCurso}, se han cargado {len(listaAlumnos)} alumnos'
    except Exception as e:
        conexion.connection.rollback() # Revierte la transacción en caso de error
        print(e)
        return 'Error en la carga de Datos, por favor validar datos a cargar o archivo Excel'
        
# Ruta para listar documentos
@app.route('/archivos', methods=['GET'])
def lista_doc():
    # Realiza una consulta para obtener los documentos en la base de datos
    cursor=conexion.connection.cursor()
    sql = "SELECT * FROM archivo"
    cursor.execute(sql)
    datos = cursor.fetchall()
    archivos = []
    for fila in datos:
        # Construye un diccionario con los datos de cada archivo
        fila = {'id':fila[0],
                'curso':fila[1],
                'nombre':fila[2]}
        archivos.append(fila)
    return jsonify({'archivos':archivos})

# Ruta para obtener un archivo PDF
@app.route('/get_pdf/<filename>', methods=['GET'])
def get_pdf(filename):
    file_path = os.path.join('uploads', filename) # Construye la ruta del archivo
    try:
        return send_file(file_path, as_attachment=True) # Envía el archivo como descarga
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado'}), 404 # Devuelve un error si el archivo no se encuentra

# Ruta para agregar un pago    
@app.route('/pagos', methods=['POST'])
def agregar_pago():
    cursor = conexion.connection.cursor()
    datos = request.get_json() # Obtiene los datos JSON de la solicitud

    montoPago = datos.get('montoPago')
    nroTarjeta = datos.get('nroTarjeta')
    fecVen = datos.get('fecVen')
    cvv = datos.get('cvv')

    # Procesa las cuotas asociadas
    cuotas = datos.get('cuotas', [])
    cuotas = str(tuple(cuotas)) # Convierte las cuotas a una tupla para la consulta SQL
    sql = "UPDATE cuota SET pagado = 1 WHERE id in {0}".format(cuotas)
    cursor.execute(sql)

    # Inserta el registro del pago en la base de datos
    sql = "INSERT INTO pago (montoPago, nroTarjeta, fecVen, cvv) VALUES ('{0}', '{1}', '{2}', '{3}')".format(montoPago, nroTarjeta, fecVen, cvv)
    cursor.execute(sql)

    pagoId = cursor.lastrowid # Obtiene el ID del último pago insertado

    # Confirma los cambios
    conexion.connection.commit()
    return "hola"


# Ruta para listar alumnos por apoderado
@app.route('/alumnos/apoderado', methods=['GET'])
def alumnos_apoderado():
    return alumnosXapoderado.alumnos_apoderado(conexion)
    
# Ruta para ver la información de viaje
@app.route('/infoViaje', methods=['GET'])
def verInfoViaje():
    return viaje.verInfoViaje(conexion)


# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()