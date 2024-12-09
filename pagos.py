from flask import jsonify, request

def get_pagos(conexion):
    try:
        id_param = request.args.get('id')

        if(id_param):
            cursor=conexion.connection.cursor()
            sql="SELECT * FROM pago WHERE id = '{0}' ".format(id_param)
            cursor.execute(sql)
            datos=cursor.fetchall()
            pagos=[]
            for fila in datos:
                pago={'id':fila[0], 'montoPago':fila[1], 'nroTarjeta':fila[2], 'fecVen':fila[3], 'cvv':fila[4]}
                pagos.append(pago)
            return jsonify({'pagos': pagos, 'mensaje': 'Pagos listados'})
        else:
            cursor=conexion.connection.cursor()
            sql='SELECT * FROM pago'
            cursor.execute(sql)
            datos=cursor.fetchall()
            pagos=[]
            for fila in datos:
                pago={'id':fila[0], 'montoPago':fila[1], 'nroTarjeta':fila[2], 'fecVen':fila[3], 'cvv':fila[4]}
                pagos.append(pago)
            return jsonify({'pagos': pagos, 'mensaje': 'Pagos listados'})
    except Exception as ex:
        return 'Error'