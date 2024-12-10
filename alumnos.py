from flask import jsonify, request
import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rutpy import validate

def get_alumnos(conexion):
    id_param = request.args.get('id')
    apoderado_param = request.args.get('apoderado')
    rut_param = request.args.get('rut')
    curso_param = request.args.get('curso')

    if(id_param):
        cursor=conexion.connection.cursor()
        sql = """SELECT al.id, 
                        concat(us.nom,' ',us.appat,' ',us.apmat) as apoderado,
                        al.rut, 
                        al.nom, 
                        al.appat, 
                        al.apmat, 
                        cu.nomCurso,
                        cu.id
                FROM alumno al
                INNER JOIN user us
                    ON (al.apoderado = us.id)
                INNER JOIN curso cu
                    ON (al.curso = cu.id)
                WHERE al.id = '{0}' """.format(id_param)
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno ={'id': fila[0], 
                    'apoderado': fila[1],
                    'rut':fila[2],
                    'nom':fila[3],
                    'appat':fila[4],
                    'apmat':fila[5],
                    'curso': fila[6],
                    'idCurso': fila[7]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Carga Ok', 'codigo': 200})
    elif(apoderado_param):
        cursor = conexion.connection.cursor()
        sql = """SELECT  al.id, 
                        concat(us.nom,' ',us.appat,' ',us.apmat) as apoderado,
                        al.rut, 
                        al.nom, 
                        al.appat, 
                        al.apmat, 
                        cu.nomCurso,
                        cu.id
                FROM alumno al
                INNER JOIN user us
                    ON (al.apoderado = us.id)
                INNER JOIN curso cu
                    ON (al.curso = cu.id)
                WHERE al.apoderado = '{0}' """.format(apoderado_param)
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno ={'id': fila[0], 
                    'apoderado': fila[1],
                    'rut':fila[2],
                    'nom':fila[3],
                    'appat':fila[4],
                    'apmat':fila[5],
                    'curso': fila[6],
                    'idCurso': fila[7]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Carga Ok'}), 200
    elif(rut_param):
        return 'hola'
    elif(curso_param):
        return 'hola'
    else:
        cursor=conexion.connection.cursor()
        sql = """SELECT  al.id, 
                        concat(us.nom,' ',us.appat,' ',us.apmat) as apoderado,
                        al.rut, 
                        al.nom, 
                        al.appat, 
                        al.apmat, 
                        cu.nomCurso,
                        cu.id
                FROM alumno al
                INNER JOIN user us
                    ON (al.apoderado = us.id)
                INNER JOIN curso cu
                    ON (al.curso = cu.id)"""
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno ={'id': fila[0], 
                    'apoderado': fila[1],
                    'rut':fila[2],
                    'nom':fila[3],
                    'appat':fila[4],
                    'apmat':fila[5],
                    'curso': fila[6],
                    'idCurso': fila[7]}
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Carga Ok'}), 200
    
def cargar_alumnos(conexion, cursoId, xlsx_df, valorCuotaAlumno):
    cursor=conexion.connection.cursor()
    json_str = xlsx_df.to_json(orient='records', force_ascii=False)
    listaAlumnos = json.loads(json_str)
    for alumno in listaAlumnos:
        # if not validate(alumno['RUT']):
        #     raise ValueError(f"RUT invalido encontrado: {alumno['RUT']}")
        sql = "INSERT INTO alumno (apoderado, rut, nom, appat, apmat, curso) values ((SELECT id FROM user where rut = '{0}'),'{1}','{2}','{3}','{4}','{5}')".format(alumno['Apoderado'],alumno['RUT'],alumno['Nombre'],alumno['Apellido Paterno'],alumno['Apellido Materno'],cursoId)
        cursor.execute(sql)
        alumnoId = cursor.lastrowid
        fechaCuota = datetime.now()
        fechaVenc = fechaCuota + relativedelta(months=1)
        for i in range(1,9):
            fechaCuotaFor = fechaCuota.strftime('%Y-%m-%d %H:%M:%S')
            fechaVencFor = fechaVenc.strftime('%Y-%m-%d %H:%M:%S')
            sql = "INSERT INTO cuota (alumnoCuota, fechaCuota, fechaVenc, valorCuota, pagado, vencido) VALUES ('{0}', '{1}', '{2}', '{3}', 0, 0)".format(alumnoId, fechaCuotaFor, fechaVencFor, valorCuotaAlumno)

            cursor.execute(sql)
            
            fechaVenc = fechaVenc + relativedelta(months=1)
            fechaCuota = fechaCuota + relativedelta(months=1)
        
    return listaAlumnos
    

def obtener_alumno_por_id(conexion, id_param):
    cursor = conexion.connection.cursor()
    sql = """SELECT al.id, 
                    concat(us.nom,' ',us.appat,' ',us.apmat) as apoderado,
                    al.rut, 
                    al.nom, 
                    al.appat, 
                    al.apmat, 
                    cu.nomCurso,
                    cu.id
            FROM alumno al
            INNER JOIN user us ON (al.apoderado = us.id)
            INNER JOIN curso cu ON (al.curso = cu.id)
            WHERE al.id = %s"""
    cursor.execute(sql, (id_param,))
    datos = cursor.fetchone()

    if datos:
        alumno = {
            'id': datos[0],
            'apoderado': datos[1],
            'rut': datos[2],
            'nom': datos[3],
            'appat': datos[4],
            'apmat': datos[5],
            'curso': datos[6],
            'idCurso': datos[7]}
        return alumno
    else:
        return None
