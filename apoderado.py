from flask import jsonify, request
import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rutpy import validate

def cargar_apoderado(conexion, xlsx_df):
    cursor = conexion.connection.cursor()
    json_str = xlsx_df.to_json(orient='records', force_ascii=False)
    listaApoderados = json.loads(json_str)

    for apoderado in listaApoderados:
        # if not validate(apoderado['RUT']):
        #     raise ValueError(f'RUT invalido encontrado: {apoderado["RUT"]}')
        
        sql = """INSERT INTO `user` (`rut`, `nom`, `appat`, `apmat`, `mail`, `password`, `rol`, `isActive`, `fechaCreacion`) 
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', 'apoderado', TRUE, NOW());""".format(apoderado['RUT'], apoderado['Nombre'], apoderado['Apellido Paterno'], apoderado['Apellido Materno'], apoderado['Correo Electrónico'], apoderado['Contraseña'])
        
        cursor.execute(sql)
       
    return 