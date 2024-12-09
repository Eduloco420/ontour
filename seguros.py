from flask import jsonify, request
import math

def get_seguros(conexion):
    cursor=conexion.connection.cursor()
    sql = "SELECT * FROM seguro"
    cursor.execute(sql)
    datos = cursor.fetchall()
    seguros = []
    for fila in datos:
        fila = {'id':fila[0], 
                'empresaSeguro':fila[1],
                'nomSeguro': fila[2],
                'valorSeguro':fila[3],
                'coberturaSeguro':fila[4]}
        seguros.append(fila)
    return jsonify({'mensaje':'Consulta Ok', 'Seguros': seguros}), 200

def valor_seguro(conexion, seguro, cantAlumnos):
    cursor = conexion.connection.cursor()
    sql = "SELECT valorSeguro FROM seguro WHERE id = '{0}'".format(seguro)
    cursor.execute(sql)
    dato = cursor.fetchone()
    valorSeguro = dato[0]
    valorSeguroAlumno = math.ceil((valorSeguro / cantAlumnos) / 8)

    return valorSeguroAlumno
