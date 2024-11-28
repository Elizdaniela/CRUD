from flask import Flask
from flask_cors import CORS #permite el acceso desde  APIs externas
from flask import jsonify, request #manejar respuestas en formato JSON y recibir solicitudes
import pymysql # libreria para conectar la base de datos MYSQL

app=Flask(__name__) #inicia la app flask

CORS (app) #permite las solicitudes y accesos de otros dominios
def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4') #establece la conexion
    return conn

# ruta para consultar todos los registros 
@app.route("/")
def consulta_general():

    try:
        #conexion a la base de datos
        conn=conectar('localhost', 'root', '','gestor_contrasena')
        cur = conn.cursor() #cursor para ejecutar consultas
        cur.execute(""" SELECT * FROM baul """)
        datos = cur.fetchall() #obtenemos los resultados de la consulta # extraer datos
        data=[]
    #obtenemos los datos y formateamos en un diccionario
        for row in datos:
            dato={'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave' :row[3]}
            data.append(dato) #agregamos cada registro a la lista data

        cur.close() #cerramos cursor
        conn.close() #cerramos conexion a la base de datos
        return jsonify({'baul': data, 'mensaje': 'Baul de contraseñas'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.get("/consulta_individual/<codigo>")
def consulta_individual(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_contrasena')
        cur = conn.cursor()
        #ejecutamos la consulta SQL para obtener un registro
        cur.execute(""" SELECT * FROM baul where id_baul='{0}' """.format(codigo))

        datos=cur.fetchone() #obtenemos un solo registro
        cur.close()
        conn.close()
    #si encontramos un registro lo devolvemos
        if datos!= None:
            dato={'id_baul':datos[0], 'Plataforma':datos[1], 'usuario':datos[2], 'clave':datos[3]}
            return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:

        return jsonify({'mensaje': 'Error'})

@app.post("/registro/")
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        query = "insert into baul (Plataforma, usuario, clave) values \
            ('{0}', '{1}', '{2}')".format(request.json['Plataforma'], request.json['usuario'], request.json['clave'])
        x=cur.execute(query)
        conn.commit() #confirmamos la insercion de los datos a la base 
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@app.delete("/eliminar/<codigo>")
def eliminar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        x=cur.execute(""" delete from baul where id_baul={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:

        print(ex)

        return jsonify({'mensaje': 'Error'})

@app.put("/actualizar/<codigo>")
def actualizar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        query = query = "update baul set Plataforma='{0}', usuario='{1}',clave='{2}' where id_baul={3}""".format(request.json['Plataforma'], request.json['usuario'], request.json['clave'], codigo)
        x=cur.execute(query)

        conn.commit() #confirmamos la actualizacion de los datos
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})

    except Exception as ex:

        print(ex)

        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    app.run(debug=True) #iniciamos el servidor en modo de depuracion