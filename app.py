from flask import Flask, jsonify, request, send_file
from flask_mysqldb import MySQL
import pagos, alumnos, seguros, cursos, paquetes, viaje, login, apoderado
import pandas as pd 
import os
from config import config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config['development'])

conexion = MySQL(app)

CORS(app)
CORS(app, resources={r"/login": {"origins": "http://127.0.0.1:5501"}})


# Crear la carpeta de almacenamiento si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/login', methods=['POST'])
def login_get():
    return login.login()

@app.route('/validar', methods=['POST'])
def verificartoken():
    return login.validar()

@app.route('/home')
def home():
    return jsonify({"message":"Bienvenido a mi BackEnd finallll"})

# Ruta para listar pagos
@app.route('/pagos', methods=['GET'])
def listar_pagos():
    return pagos.get_pagos(conexion) # Llama al método en el módulo pagos para obtener los datos de pagos

# Ruta para listar alumnos    
@app.route('/alumnos', methods=['GET'])
def lista_alumnos():
    id_param = request.args.get('id')
    if id_param:
        # Llama a la función obtener_alumno_por_id con el ID proporcionado
        alumno = alumnos.obtener_alumno_por_id(conexion, id_param)
        if alumno:
            return jsonify({'alumno': alumno})
        else:
            return jsonify({'error': 'Alumno no encontrado'}), 404
    else:
        # Si no se proporciona el ID, devuelve todos los alumnos
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

        if 'Planilla' not in request.files:
            return jsonify({'error': 'No se ha enviado un archivo'}), 400
        if 'contrato' not in request.files:
            return jsonify({'error': 'No se ha cargado contrato'}), 400 

        Planilla = request.files['Planilla']
        contrato = request.files['contrato']
        alumnos_df = pd.read_excel(Planilla, sheet_name='Alumnos')
        apoderado_df = pd.read_excel(Planilla, sheet_name='Apoderados')
        nomCurso = request.form.get('nomCurso')
        nomColegio = request.form.get('nomColegio')
        paqueteTuristico = request.form.get('paqueteTuristico')
        seguro = request.form.get('seguro')
        cantAlumnos = len(alumnos_df)
        fechaViaje = request.form.get('fechaViaje')

        apoderado.cargar_apoderado(conexion=conexion, xlsx_df=apoderado_df)

        cursoId = cursos.post_curso(conexion, contrato, nomCurso ,nomColegio ,paqueteTuristico ,seguro ,cantAlumnos, app, fechaViaje)
        valorPaqueteAlumno = paquetes.valor_paquete(conexion, paqueteTuristico, cantAlumnos)
        valorSeguroAlumno = seguros.valor_seguro(conexion, seguro, cantAlumnos)
        valorCuotaAlumno = (valorPaqueteAlumno + valorSeguroAlumno)
        listaAlumnos = alumnos.cargar_alumnos(conexion=conexion, cursoId=cursoId, xlsx_df=alumnos_df, valorCuotaAlumno=valorCuotaAlumno)

        conexion.connection.commit()

        return f'Se ha creado el curso {nomCurso}, se han cargado {len(listaAlumnos)} alumnos'
    except ValueError as e:
        conexion.connection.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        conexion.connection.rollback()
        return 'Error en la carga de Datos, favor validar datos a cargar o archivo Excel'
          

#ruta para traer los datos de los pdf
@app.route('/archivos', methods=['GET'])
def lista_doc():
    cursoId = request.args.get('cursoId')
    cursor=conexion.connection.cursor()
    sql = "SELECT * FROM archivo where curso = '{0}'".format(cursoId)
    cursor.execute(sql)
    datos = cursor.fetchall()
    archivos = []
    for fila in datos:
        fila = {'id':fila[0],
                'curso':fila[1],
                'nombre':fila[2]}
        archivos.append(fila)
    return jsonify({'archivos':archivos})

@app.route('/get_pdf/<filename>', methods=['GET'])
def get_pdf(filename):
    file_path = os.path.join('uploads', filename)
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado'}), 404
    
@app.route('/archivoCarga', methods=['GET'])
def send_xlsx():
    file_path = os.path.join('assets\\archivo_carga.xlsx')
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'mensaje':'Error con el envio del archivo'}), 404

@app.route('/pagos', methods=['POST'])
def agregar_pago():
    cursor = conexion.connection.cursor()
    datos = request.get_json()

    nroTarjeta = datos.get('nroTarjeta')
    fecVen = datos.get('fecVec')
    cvv = datos.get('cvv')

    cuotas = datos.get('cuotas', [])
    cuotaStr = str(tuple(cuotas))
    sql = "UPDATE cuota SET pagado = 1 WHERE id in {0}".format(cuotaStr)
    cursor.execute(sql)

    sql = "INSERT INTO pago (montoPago, nroTarjeta, fecVen, cvv) VALUES ((SELECT sum(valorCuota) FROM cuota where id in {0}), '{1}', '{2}', '{3}')".format(cuotaStr, nroTarjeta, fecVen, cvv)
    cursor.execute(sql)

    pagoId = cursor.lastrowid

    for cuota in cuotas:
        sql = "INSERT INTO pagocuota (cuota, pago) VALUES ('{0}','{1}')".format(cuota, pagoId)
        cursor.execute(sql)
    
    conexion.connection.commit()
    return jsonify({"Mensaje":"Pago Ingresado Ok"})
    
@app.route('/alumnos/apoderado', methods=['GET'])
def alumnos_apoderado():

    apoderado = request.args.get('apoderado')

    cursor = conexion.connection.cursor()
    sql = """SELECT 	a.id,
                        c.nomCurso,
                        c.nomColegio,
                        p.ciudad,
                        a.rut
                FROM alumno a
                INNER JOIN curso c
                    ON (a.curso = c.id)
                INNER JOIN paqueteturistico p
                    ON (c.paqueteTuristico = p.id)
                WHERE a.apoderado = '{0}';""".format(apoderado)
    cursor.execute(sql)
    datos = cursor.fetchall()
    alumnos = []
    for fila in datos:
        alumno = {  "alumno":fila[0],
                    "nomCurso":fila[1], 
                    "nomColegio":fila[2], 
                    "ciudad":fila[3], 
                    "rut":fila[4]}
        alumnos.append(alumno)
    return jsonify({'alumnos':alumnos, 'mensaje':'Hola Karlita'})

@app.route('/pefilApode', methods=['GET'])
def info_perfil():

    apoderado = request.json.get('id')
    print("ID recibido:", apoderado)

    cursor = conexion.connection.cursor()
    sql = """SELECT 	u.id,
                u.nom,
                u.mail,
                a.nom,
                a.rut
         FROM user u
         INNER JOIN alumno a ON u.id = a.apoderado
         WHERE a.id = '{0}';""".format(apoderado)

    cursor.execute(sql)
    datos = cursor.fetchall()
    apoderados = []
    for fila in datos:
        fila = {  "id":fila[0],
                    "nom":fila[1], 
                    "mail":fila[2], 
                    "nomAlum":fila[3], 
                    "rutAlum":fila[4]}
        apoderados.append(fila)
        
    return jsonify({'apoderados':apoderados})

@app.route('/paquetes', methods=['GET'])
def obtener_paquetes():
    return paquetes.get_paquetes(conexion)
    
# Ruta para ver la información de viaje
@app.route('/infoViaje', methods=['GET'])
def verInfoViaje():
    return viaje.verInfoViaje(conexion)

@app.route('/cuotas_curso/<int:curso_id>', methods=['GET'])
def cuotas_curso(curso_id):
    try:
        cursor = conexion.connection.cursor()
        sql = """
            SELECT 
                c.id AS cuota_id,
                a.rut AS alumno_rut,
                c.valorCuota,
                c.fechaCuota,
                c.pagado
            FROM cuota c
            INNER JOIN alumno a ON c.alumnoCuota = a.id
            WHERE a.curso = %s"""
        cursor.execute(sql, (curso_id,))
        cuotas = cursor.fetchall()
        
        if not cuotas:
            return jsonify({'mensaje': 'No se encontraron cuotas para este curso', 'estado': 'sin datos'}), 404

        total_cuotas = len(cuotas)
        total_valor = sum(cuota[2] for cuota in cuotas)
        pagadas = [cuota for cuota in cuotas if cuota[4] == 1]
        pendientes = [cuota for cuota in cuotas if cuota[4] == 0]
        total_pagado = sum(cuota[2] for cuota in pagadas)
        total_pendiente = total_valor - total_pagado

        porcentaje_avance = (total_pagado / total_valor) * 100 if total_valor > 0 else 0

        return jsonify({
            'total_valor': total_valor,
            'total_pagado': total_pagado,
            'total_pendiente': total_pendiente,
            'porcentaje_avance': round(porcentaje_avance, 2),
            'detalle_pagadas': [
                {
                    'cuota_id': cuota[0],
                    'alumno_rut': cuota[1],
                    'valor': cuota[2],
                    'fecha_cuota': cuota[3].strftime('%Y-%m-%d')
                } for cuota in pagadas
            ],
            'detalle_pendientes': [
                {
                    'cuota_id': cuota[0],
                    'alumno_rut': cuota[1],
                    'valor': cuota[2],
                    'fecha_cuota': cuota[3].strftime('%Y-%m-%d')
                } for cuota in pendientes
            ],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()