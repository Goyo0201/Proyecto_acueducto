   
import mysql.connector

try: 
# Configura la conexión
    conexion = mysql.connector.connect(
        host="localhost",  # El host de la base de datos (generalmente "localhost" si está en la misma máquina)
        user="root",  # Tu nombre de usuario de MySQL
        password="",  # Tu contraseña de MySQL
        database="bd_acueducto"  # El nombre de la base de datos a la que deseas conectarte
    )
    print("Conexión exitosa a la base de datos")
    
except Exception as ex:
    print(ex)


