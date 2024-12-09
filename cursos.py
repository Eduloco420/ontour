from flask import jsonify
import os

def get_curso(conexion):
    cursor=conexion.connection.cursor()
    sql = """SELECT 	c.id,
                        c.nomCurso,
                        c.nomColegio,
                        c.cantAlumnos,
                        p.nomPaquete,
                        s.nomSeguro
                FROM curso c
                INNER JOIN paqueteturistico p 
                    ON (c.paqueteturistico = p.id)
                INNER JOIN seguro s
                    ON (s.id = c.seguro);"""
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursos = []
    for fila in datos:
        fila = {'id':fila[0],
                'nomCurso':fila[1],
                'nomColegio':fila[2],
                'cantAlumnos':fila[3],
                'nomPaquete':fila[4],
                'seguro':fila[5]}
        cursos.append(fila)
    return jsonify({'mensajes':'Consulta Ok', 'Cursos':cursos})
    

def post_curso(conexion, contrato, nomCurso ,nomColegio ,paqueteTuristico ,seguro ,cantAlumnos, app, fechaViaje):
    cursor=conexion.connection.cursor()

    sql = """INSERT INTO curso (nomCurso, nomColegio, paqueteTuristico, seguro, cantAlumnos, fechaViaje) values ('{0}','{1}','{2}','{3}','{4}','{5}');""".format(nomCurso,
                                                                                                                                        nomColegio,
                                                                                                                                        paqueteTuristico,
                                                                                                                                        seguro,
                                                                                                                                        cantAlumnos,
                                                                                                                                        fechaViaje) 

    cursor.execute(sql)
    
    cursoId = cursor.lastrowid
    nombreDoc = f'contrato_curso_{cursoId}.pdf'
    
    sql = "INSERT INTO archivo (curso, ruta) VALUES ('{0}','{1}')".format(cursoId, nombreDoc)
    cursor.execute(sql)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], nombreDoc)
    contrato.save(file_path)
    conexion.connection.commit()
    return cursoId