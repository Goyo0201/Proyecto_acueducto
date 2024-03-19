
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QDialog, QMessageBox, QMainWindow
from PyQt5 import QtGui, QtWidgets as qtw


from PyQt5.QtGui import QPixmap, QPainter

from PyQt5.QtPrintSupport import *
import re
#conexion
from ConexionPyodbc import conexion
#Login
from login import *
#Interfaces
from menu_principal import *

from interfaz_puntos import *

from interfaz_recibos import *

from interfaz_oficios import *

from interfaz_gastos import *


#Se crea una clase para el login de los usuarios
class Login(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_login()
        self.ui.setupUi(self)
        
        
        #configuraciones login
        #botones (cerrar, mini...)
        self.ui.bt_cerrar.clicked.connect(self.close)

        #Quitar barra superior
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        #Boton iniciar sesion
        self.ui.bt_ingresar_login.clicked.connect(self.iniciar_sesion)
        
        
        #contra verrrrr
        self.ui.bt_ver.clicked.connect(self.toggle_password_visibility)


    def toggle_password_visibility(self):
        if self.ui.txt_input_contrasea.echoMode() == QtWidgets.QLineEdit.Password:
            self.ui.txt_input_contrasea.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.txt_input_contrasea.setEchoMode(QtWidgets.QLineEdit.Password) 
        

    def iniciar_sesion(self):
        """
        Esta función pide al usuario los datos de ingreso
        """
        #Strip remueve el espacio que haya al principio o final --123--
        usuario = self.ui.txt_input_usuario.text().strip()
        contraseña = self.ui.txt_input_contrasea.text().strip()
        mensaje = QMessageBox(self)
        
        mensaje.setWindowTitle('Mensaje')
        
         # Aplicar hojas de estilo CSS para personalizar la apariencia
        estilo_css = '''
            QMessageBox {
                background-color: #21252b;
                
                color: #ffffff;  /* Color del texto del cuadro de diálogo */
            }
            QLabel, QMessageBox QLabel {
                color: #ffffff;  /* Color del texto del mensaje */
            }
            QPushButton, QMessageBox QPushButton {
                background-color: #21252b;  /* Fondo del botón */
                color: #ffffff;  /* Texto del botón */
                border: 1px solid #ffffff;
                padding: 5px 10px;
            }
            QPushButton:hover, QMessageBox QPushButton:hover {
                background-color: #003399;
            }
        '''


        
        mensaje.setStyleSheet(estilo_css)
        
         #Se valida que haya algo escrito en las cajas de texto
        if len(usuario) and len(contraseña):
            if usuario == 'elhogar' and contraseña == '1234':
                mensaje.setIcon(QMessageBox.Information)
                mensaje.setText('Bienvenido(a) a la interfaz de control de acueducto El Hogar :)')
                
                self.close()
                
                self.ventana = menu_principal()
                self.ventana.show()
                
                

            else:
                mensaje.setIcon(QMessageBox.Warning)
                mensaje.setText('El usuario o la contraseña son incorrectos')
            
        else:
            mensaje.setIcon(QMessageBox.Warning)
            mensaje.setText('Todos los campos son obligatorios')
        mensaje.exec_()
        

#menu principal
class menu_principal(qtw.QMainWindow):
    def __init__(self):
        super(menu_principal, self).__init__()
        self.ui=Ui_menu_principal()
        self.ui.setupUi(self)
        
        #botones superiores (x - [])
        self.ui.bt_restaurar.hide()
        self.click_posicion = None
        self.ui.bt_minimizar.clicked.connect(lambda: self.showMinimized())
        #self.ui.bt_restaurar.clicked.connect(self.control_bt_restaurar)
        #self.ui.bt_maximizar.clicked.connect(self.control_bt_max)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())
        
        #quitar botones predeterminados
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        
        #mover ventana
        self.ui.frame_2.mouseMoveEvent = self.mover_ventana
    
        #botones acciones
        self.ui.bt_usuarios.clicked.connect(self.puntos_agua)
        self.ui.bt_recibos.clicked.connect(self.recibos)
        self.ui.bt_oficios.clicked.connect(self.oficios)
        self.ui.bt_gastos.clicked.connect(self.gastos)
        
        self.ui.bt_cerrar_sesion.clicked.connect(self.boton_cerrar_sesion)
        
        self.mensaje = QMessageBox(self)
    
    def control_bt_restaurar(self):
        self.showNormal()
        self.ui.bt_restaurar.hide()
        self.ui.bt_maximizar.show()
    
    def control_bt_max(self):
        self.showMaximized()
        self.ui.bt_maximizar.hide()
        self.ui.bt_restaurar.show()
           
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        
    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():         
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()
		
        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
           self.showMaximized()
           self.ui.bt_maximizar.hide()
           self.ui.bt_restaurar.show()
        else:
           self.showNormal()
           self.ui.bt_restaurar.hide()
           self.ui.bt_maximizar.show()

       #Interfaz puntos de agua
    def puntos_agua(self):
        self.ui=Ui_interfaz_puntos()
        self.ui.setupUi(self)   
        
        #acciones botones superiores
        self.ui.bt_restaurar.hide()
        self.click_posicion = None
        self.ui.bt_minimizar.clicked.connect(lambda: self.showMinimized())
        self.ui.bt_restaurar.clicked.connect(self.control_bt_restaurar)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_max)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())
        
        #mover ventana
        self.ui.frame_superior.mouseMoveEvent = self.mover_ventana   
        
        #botones de la barra
        self.ui.bt_crear.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_agregar)) 
        self.ui.bt_editar.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_editar)) 
        self.ui.bt_eliminar.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_eliminar))  
        self.ui.bt_consumo.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_consumo))   
        
        self.ui.bt_crear_usuario.clicked.connect(self.agregar_punto)
        
        self.ui.bt_actualizar_datos.clicked.connect(self.actualizar_tabla_editar)
        self.ui.bt_guardar_datos.clicked.connect(self.guardar_tabla_editar)
        
        self.ui.bt_actualizar_tabla.clicked.connect(self.actualizar_tabla_eliminar)
        self.ui.bt_borrar_usuario.clicked.connect(self.borrar_punto_agua)
        
        #botones consumo
        self.ui.bt_consumo.clicked.connect(self.crear_consumo_combo)
        self.ui.bt_agregar_consumo.clicked.connect(self.agregar_consumo)
        self.ui.bt_actualizar_consumo.clicked.connect(self.actualizar_consumo)
        self.ui.bt_editar_consumo.clicked.connect(self.guardar_datos_consumo)
        self.ui.bt_eliminar_consumo.clicked.connect(self.eliminar_consumo)
        
        
        self.ui.bt_regresar.clicked.connect(self.boton_regresar)
        
        
        
    
        
    def agregar_punto(self):
        
        """
        Esta función agrega un punto de agua
        """
        


        numero_cedula = int(self.ui.txt_cedula_agregar.text())
        nombres = self.ui.txt_nombres_agregar.text()
        apellidos = self.ui.txt_apellidos_agregar.text() 
        num_telefono = int(self.ui.txt_tel_agregar.text())
        correo = self.ui.txt_correo_agregar.text()
        direccion_propietario = self.ui.txt_direccion_agregar.text() 
        
        nom_predio = self.ui.txt_nombre_predio.text()
        direccion_predio = self.ui.txt_direccion_predio.text() 
        

        estado = self.ui.combo_estado.currentText()
        
       
        
        try:
            with conexion.cursor() as cursor:
            # Primero, inserta los datos en las tablas propietario y predio
             sql = "INSERT INTO propietario (num_cedula, nombres, apellidos, num_telefono, correo, direccion) VALUES (%s, %s, %s, %s, %s, %s)"
             cursor = conexion.cursor()
             cursor.execute(sql, (numero_cedula, nombres, apellidos, num_telefono, correo, direccion_propietario))

             propietario_id = cursor.lastrowid

             sql = "INSERT INTO predio (nombre_predio, direccion) VALUES (%s, %s)"
             cursor.execute(sql, (nom_predio, direccion_predio))

            # Obtener el ID del predio que acabamos de insertar
             predio_id = cursor.lastrowid

            # Luego, inserta los datos en la tabla predio_propietario
             sql = "INSERT INTO predio_propietario (id_predio, id_propietario) VALUES (%s, %s)"
             cursor.execute(sql, (predio_id, propietario_id))

            # Finalmente, inserta los datos en la tabla punto_agua
             sql = "INSERT INTO punto_agua (estado, num_catastral_predio) VALUES (%s, %s)"
             cursor.execute(sql, (estado, predio_id))
             
            
            #Se limpian los campos luego de ingresar los datos
            self.ui.txt_cedula_agregar.clear()
            self.ui.txt_nombres_agregar.clear()
            self.ui.txt_apellidos_agregar.clear()
            self.ui.txt_tel_agregar.clear()
            self.ui.txt_correo_agregar.clear()
            self.ui.txt_direccion_agregar.clear()
                
            
            self.ui.txt_nombre_predio.clear()
            self.ui.txt_direccion_predio.clear()

           

            if (cursor.execute):
                qtw.QMessageBox.information(self, "Éxito", "Datos almacenados correctamente")
                
                
                    
            else:
                qtw.QMessageBox.critical(self, "Error", "No se almacenaron los datos")
    
        except Exception as ex:
            print(ex)
            
    def actualizar_tabla_editar(self):
        tabla = self.ui.tabla_editar  # Asegúrate de que este sea el nombre correcto de tu tabla

        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT propietario.*, predio.*, punto_agua.num_contador, punto_agua.estado  
                        FROM propietario 
                        JOIN predio_propietario ON propietario.id = predio_propietario.id_propietario 
                        JOIN predio ON predio_propietario.id_predio = predio.num_catastral 
                        JOIN punto_agua ON predio.num_catastral = punto_agua.num_catastral_predio"""
                
                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                usuarios_puntos = cursor.fetchall()

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(usuarios_puntos)
                tabla.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for usuario in usuarios_puntos:
                        # Asegúrate de que los índices estén correctos según la estructura de tus datos
                        tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(usuario[0])))
                        tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(usuario[1])))
                        tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(usuario[2])))
                        tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(usuario[3])))
                        tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(usuario[4])))
                        tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(usuario[5])))
                        tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(usuario[6])))
                        tabla.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(usuario[7])))
                        tabla.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(usuario[8])))
                        tabla.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(usuario[9])))
                        tabla.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(str(usuario[10])))
                        
                         # Crear y agregar ComboBox a la celda (fila 8)
                        combo_box = QtWidgets.QComboBox()
                        combo_box.addItems([str(usuario[11]),"Activo", "Fuera de servicio", "En reparación", "En prueba", "En espera"])
                        tabla.setCellWidget(tablerow, 11, combo_box)
                        
                        # Aplicar estilo CSS al QComboBox
                        combo_box.setStyleSheet("""
                            QComboBox {
                                background-color: white;
                                color: darkblue;
                                border: 1px solid darkblue;
                                padding: 2px;
                                selection-background-color: blue;
                                font: 10pt "Segoe UI";
                            }

                            QComboBox QAbstractItemView {
                                background-color: lightgray;
                                border: 1px solid darkgray;
                                selection-background-color: #0074c3;  /* Color cuando la opción está seleccionada */
                                selection-color: white;
                            }

                            QComboBox QAbstractItemView::item:first {
                                background-color: lightgreen;  /* Color para el primer elemento */
                        }
                    """)
                        
                      
                        
                        tabla.item(tablerow, 0).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla.item(tablerow, 1).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla.item(tablerow, 7).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla.item(tablerow, 10).setFlags(QtCore.Qt.ItemIsEnabled)
                        
                        tablerow += 1
                else:
                    self.mensaje.setText("No existen usuarios en el sistema")
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.exec()

        except Exception as ex:
            print(ex)
            
    def guardar_tabla_editar(self):
        tabla = self.ui.tabla_editar

        try:
            with conexion.cursor() as cursor:
                # Itera sobre las filas de la tabla y realiza la actualización en la base de datos
                for fila in range(tabla.rowCount()):
                    id = int(tabla.item(fila, 0).text()) 
                    num_cedula = int(tabla.item(fila, 1).text()) 
                    nombres = str(tabla.item(fila, 2).text()) 
                    apellidos = str(tabla.item(fila, 3).text()) 
                    num_telefono = int(tabla.item(fila, 4).text()) 
                    correo = str(tabla.item(fila, 5).text()) 
                    direccion_pro = str(tabla.item(fila, 6).text())
                    
                    num_catastral = int(tabla.item(fila, 7).text()) 
                    nombre_predio = str(tabla.item(fila, 8).text()) 
                    direccion_pre = str(tabla.item(fila, 9).text()) 
                    
                    num_contador = int(tabla.item(fila, 10).text()) 
                    estado = str(tabla.cellWidget(fila, 11).currentText()) 
                   

                    # Realiza la actualización en la base de datos
                    sql_propietario = """UPDATE propietario
                    SET num_cedula=%s, nombres = %s, apellidos = %s, num_telefono = %s, correo = %s, direccion = %s
                    WHERE id = %s;"""

                    sql_predio = """UPDATE predio
                    SET nombre_predio = %s, direccion = %s
                    WHERE num_catastral = %s;"""

                    sql_punto_agua = """UPDATE punto_agua
                    SET estado = %s
                    WHERE num_contador =  %s;"""

                    cursor.execute(sql_propietario, (num_cedula, nombres, apellidos, num_telefono, correo, direccion_pro, id))
                    
                    cursor.execute(sql_predio, (nombre_predio, direccion_pre, num_catastral))
                    cursor.execute(sql_punto_agua, (estado, num_contador))

            # Confirma los cambios en la base de datos
            conexion.commit()

            # Muestra un mensaje de éxito
            QMessageBox.information(self, "Éxito", "Los datos se han guardado correctamente.")

        except Exception as ex:
            # Muestra un mensaje de error si hay algún problema
            print(ex)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error al guardar los datos.")
    
    
    
    def actualizar_tabla_eliminar(self):
        tabla = self.ui.tabla_eliminar  # Asegúrate de que este sea el nombre correcto de tu tabla

        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT propietario.id, propietario.num_cedula, propietario.nombres, propietario.apellidos, predio.nombre_predio, 
                        predio.direccion AS direccion_predio, punto_agua.estado FROM propietario 
                        JOIN predio_propietario ON propietario.id = predio_propietario.id_propietario 
                        JOIN predio ON predio_propietario.id_predio = predio.num_catastral 
                        JOIN punto_agua ON predio.num_catastral = punto_agua.num_catastral_predio"""
                
                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                usuarios_puntos = cursor.fetchall()

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(usuarios_puntos)
                tabla.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for usuario in usuarios_puntos:
                        # Asegúrate de que los índices estén correctos según la estructura de tus datos
                        tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(usuario[0])))
                        tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(usuario[1])))
                        tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(usuario[2])))
                        tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(usuario[3])))
                        tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(usuario[4])))
                        tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(usuario[5])))
                        tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(usuario[6])))
                                          
                        
                        tabla.item(tablerow, 0).setFlags(QtCore.Qt.ItemIsEnabled)
                        
                        tablerow += 1
                else:
                    self.mensaje.setText("No existen usuarios en el sistema")
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.exec()

        except Exception as ex:
            print(ex)
            
    def borrar_punto_agua(self):
        
        id_propietario = self.ui.txt_id_eliminar.text()
        
        try:
            with conexion.cursor() as cursor:
                # Consulta para eliminar el usuario por su ID
                sql = "DELETE FROM propietario WHERE id = %s"
                cursor = conexion.cursor()
                cursor.execute(sql, (id_propietario,))

                if cursor.rowcount > 0:
                    qtw.QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                else:
                    qtw.QMessageBox.warning(self, "Advertencia", "No se encontró un usuario con ese ID")

        except Exception as ex:
            qtw.QMessageBox.critical(self, "Error", f"Error en la operación: {str(ex)}")
            
            
    def boton_regresar(self):
        self.close()
                
        self.ventana = menu_principal()
        self.ventana.show()
        
        
        
    def boton_cerrar_sesion (self):
        
         # Cerrar la ventana actual
        self.close()

        # Mostrar la ventana de inicio de sesión
        login = Login()
        login.show()
        
    
    #Gastos punto de agua
    def crear_consumo_combo(self):
        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT pr.nombre_predio AS NombrePredio, p.nombres AS NombrePropietario, p.apellidos AS ApellidoPropietario, 
                pa.num_contador AS NumeroContador FROM propietario p JOIN predio_propietario pp ON p.id = pp.id_propietario JOIN predio pr 
                ON pp.id_predio = pr.num_catastral JOIN punto_agua pa ON pr.num_catastral = pa.num_catastral_predio

                """

                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas
                cursor.execute(sql)

                # Obtener todos los resultados de la consulta
                resultados = cursor.fetchall()

                # Limpiar el contenido actual del ComboBox
                self.ui.combo_num_contador.clear()

                # Iterar sobre los resultados y agregar al ComboBox
                for resultado in resultados:
                    nombre_predio = resultado[0]
                    nombre_propietario = resultado[1]
                    apellido_propietario = resultado[2]
                    numero_contador = resultado[3]

                    # Crear la cadena que se mostrará en el ComboBox
                    display_text = f"{nombre_predio}-{nombre_propietario} {apellido_propietario}-Cont {numero_contador}"

                    # Agregar la cadena al ComboBox
                    self.ui.combo_num_contador.addItem(display_text)

        except Exception as ex:
            print(ex)
            
            
            
    def agregar_consumo(self):
        
        metros_cubicos = int(self.ui.txt_consumo.text())
        num_contador_punto_agua = self.ui.combo_num_contador.currentText()  
    
        # Utilizar expresiones regulares para extraer el número del contador
        numero_contador = re.search(r'Cont (\d+)', num_contador_punto_agua)
        
        if numero_contador:
            numero_contador = int(numero_contador.group(1))
            
            try:
                with conexion.cursor() as cursor:
                    # Insertar datos en la tabla consumo
                    sql = "INSERT INTO consumo (metros_cubicos, num_contador_punto_agua) VALUES (%s, %s)"
                    cursor.execute(sql, (metros_cubicos, numero_contador))
                    
                    # Confirmar los cambios en la base de datos
                    conexion.commit()
                    
                    # Mostrar un mensaje de éxito
                    qtw.QMessageBox.information(self, "Éxito", "Datos de consumo almacenados correctamente.")
                    
            except Exception as ex:
                # Mostrar un mensaje de error si hay algún problema
                print(ex)
                qtw.QMessageBox.critical(self, "Error", "Ha ocurrido un error al almacenar los datos de consumo.")
        else:
            qtw.QMessageBox.warning(self, "Advertencia", "No se pudo extraer el número del contador del ComboBox.")
            
            
            
    def actualizar_consumo(self):
        tabla_consumo = self.ui.tableWidget
        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT c.cod_consumo AS CodigoConsumo, pr.nombre_predio AS NombrePredio, 
                p.nombres AS NombresPropietario, p.apellidos AS ApellidosPropietario, c.metros_cubicos AS MetrosCubicos, 
                pa.num_contador AS NumeroContador FROM consumo c 
                JOIN punto_agua pa ON c.num_contador_punto_agua = pa.num_contador 
                JOIN predio pr ON pa.num_catastral_predio = pr.num_catastral 
                JOIN predio_propietario pp ON pr.num_catastral = pp.id_predio 
                JOIN propietario p ON pp.id_propietario = p.id"""
                
                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                consumo_agua = cursor.fetchall()

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla_consumo is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(consumo_agua)
                tabla_consumo.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for usuario in consumo_agua:
                        # Asegúrate de que los índices estén correctos según la estructura de tus datos
                        tabla_consumo.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(usuario[0])))
                        tabla_consumo.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(usuario[1])))
                        tabla_consumo.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(usuario[2])))
                        tabla_consumo.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(usuario[3])))
                        tabla_consumo.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(usuario[4])))
                        tabla_consumo.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(usuario[5])))
                                              
                        tabla_consumo.item(tablerow, 0).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla_consumo.item(tablerow, 1).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla_consumo.item(tablerow, 2).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla_consumo.item(tablerow, 3).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla_consumo.item(tablerow, 5).setFlags(QtCore.Qt.ItemIsEnabled)
                        
                        tablerow += 1
                else:
                    self.mensaje.setText("No existen consumos en el sistema")
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.exec()

        except Exception as ex:
            print(ex)


        
    def guardar_datos_consumo(self):
        tabla_consumo = self.ui.tableWidget

        try:
            with conexion.cursor() as cursor:
                # Itera sobre las filas de la tabla y realiza la actualización en la base de datos
                for fila in range(tabla_consumo.rowCount()):
                    metros_cubicos = int(tabla_consumo.item(fila, 4).text()) 
                    num_contador_punto_agua = int(tabla_consumo.item(fila, 5).text()) 
                    cod_consumo = str(tabla_consumo.item(fila, 0).text()) 
                    
                    # Realiza la actualización en la base de datos
                    sql_consumo = """UPDATE consumo
                    SET metros_cubicos = %s, num_contador_punto_agua = %s
                    WHERE cod_consumo = %s;"""

                    cursor.execute(sql_consumo, (metros_cubicos, num_contador_punto_agua, cod_consumo))
                    
            # Confirma los cambios en la base de datos
            conexion.commit()

            # Muestra un mensaje de éxito
            QMessageBox.information(self, "Éxito", "Los datos se han guardado correctamente.")
        except Exception as ex:
            print(ex)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error al guardar los datos.")



        
    def eliminar_consumo(self):
        
        codi_consumo = self.ui.txt_cod_consumo.text()
        
        try:
            with conexion.cursor() as cursor:
                # Consulta para eliminar el usuario por su ID
                sql = "DELETE FROM consumo WHERE cod_consumo = %s"
                cursor = conexion.cursor()
                cursor.execute(sql, (codi_consumo,))

                if cursor.rowcount > 0:
                    qtw.QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                else:
                    qtw.QMessageBox.warning(self, "Advertencia", "No se encontró un usuario con ese ID")

        except Exception as ex:
            qtw.QMessageBox.critical(self, "Error", f"Error en la operación: {str(ex)}") 
    
    
    #INTERFAZ RECIBOS
           #Interfaz puntos de agua
    def recibos(self):
        self.ui=Ui_interfaz_recibos()
        self.ui.setupUi(self)   
        
        #acciones botones superiores
        self.ui.bt_restaurar.hide()
        self.click_posicion = None
        self.ui.bt_minimizar.clicked.connect(lambda: self.showMinimized())
        self.ui.bt_restaurar.clicked.connect(self.control_bt_restaurar)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_max)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())
        
        #mover ventana
        self.ui.frame_superior.mouseMoveEvent = self.mover_ventana   
        
        #botones de la barra
        self.ui.bt_crear_recibo.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_recibos)) 
        
        self.ui.bt_imprimir_recibo.clicked.connect(self.imprimir_recibo)
        self.ui.bt_guardar_recibo.clicked.connect(self.guardar_recibo)
        
        self.ui.bt_crear_recibo.clicked.connect(self.crear_recibo_combo)
        
        self.ui.bt_buscar_recibo.clicked.connect(self.llenar_recibo)
        
        self.ui.bt_regresar.clicked.connect(self.boton_regresar)
        
    
    def imprimir_recibo(self):
         # Captura solo el contenido del QFrame
        frame_content = self.ui.frame_recibo.grab()
        
        # Convierte la captura en un QPixmap
        pixmap = QPixmap(frame_content)

        # Configura el diálogo de impresión
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Inicia el proceso de impresión
            painter = QPainter(printer)
            
            # Dibuja la imagen en la página de impresión
            painter.drawPixmap(0, 0, pixmap)

            # Finaliza el proceso de impresión
            painter.end()
            
    def guardar_recibo(self):
        # Captura solo el contenido del QFrame
        frame_content = self.ui.frame_recibo.grab()

        # Convierte la captura en un QPixmap
        pixmap = QPixmap(frame_content)

        # Guarda el QPixmap como imagen
        pixmap.save("C:/Users/User/Desktop/recibo2.png")
        
        
        
        fecha_recibo = self.ui.txt_fecha_recibo.text()
        lectura_anterior = self.ui.txt_lectura_ant_recibo.text()
        
        if lectura_anterior:
            lectura_anterior = int(lectura_anterior)
        else:
            lectura_anterior = 0
        
        consumo = int(self.ui.txt_metros_recibo.text())
        costo_servicio = int(self.ui.txt_costo_servicio_recibo.text())
        inas_asamblea = self.ui.txt_inas_asamblea_recibo.text()
        
        if inas_asamblea:
            inas_asamblea = int(inas_asamblea)
        else:
            inas_asamblea = 0
            
        contribucion = self.ui.txt_contribucion_recibo.text()
        
        if contribucion:
            contribucion = int(contribucion)
        else:
            contribucion = 0
        
        otros = self.ui.txt_otros_recibo.text()
        if otros:
            otros = int(otros)
        else:
            otros = 0
        
        total_recibo = int(self.ui.txt_total_recibo.text())
        numero_recibo = int(self.ui.txt_num_recibo.text())
        
        
        
        
        #self.ui.check_01 = ui.QCheckBox('01-02-03', self)
        #self.ui.check_04 = ui.QCheckBox('04-05-06', self)
        #self.ui.check_07 = ui.QCheckBox('07-08-09', self)
        #self.ui.check_10 = ui.QCheckBox('10-11-12', self)
        
        if self.ui.check_01.isChecked():
            check = ('01-02-03')  
        elif self.ui.check_04.isChecked():
            check = ('04-05-06')
        elif self.ui.check_07.isChecked():
            check = ('07-08-09')
        elif self.ui.check_10.isChecked():
            check = ('10-11-12')
        else:
            print("Ningún checkbox marcado.")
        
        
        try:
            with conexion.cursor() as cursor:
               
                    # Realiza la actualización en la base de datos
                    sql_recibo = """UPDATE recibo SET fecha_limite = %s, servicio = %s, lectura_anterior = %s, consumo = %s, 
                    costo_servicio = %s, inasistencia_asamblea = %s, contribucion = %s, otros = %s, total_pagar = %s WHERE num_recibo = %s;"""

                    cursor.execute(sql_recibo, (fecha_recibo, check, lectura_anterior, consumo, costo_servicio, 
                                                inas_asamblea, contribucion, otros, total_recibo, numero_recibo))
                    
            # Confirma los cambios en la base de datos
            conexion.commit()

            # Muestra un mensaje de éxito
            QMessageBox.information(self, "Éxito", "Los datos se han guardado correctamente.")
        except Exception as ex:
            print(ex)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error al guardar los datos.")
        
        
        
            
            
            
            
    
        
    
    #INTERFAZ RECIBO
     #Gastos punto de agua
    def crear_recibo_combo(self):
        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT recibo.num_recibo, predio.nombre_predio, propietario.nombres, propietario.apellidos FROM recibo 
                JOIN propietario ON recibo.id_propietario = propietario.id JOIN predio_propietario ON propietario.id = predio_propietario.id_propietario 
                JOIN predio ON predio_propietario.id_predio = predio.num_catastral

                """

                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas
                cursor.execute(sql)

                # Obtener todos los resultados de la consulta
                resultados = cursor.fetchall()

                # Limpiar el contenido actual del ComboBox
                self.ui.combo_usuario_recibo.clear()

                # Iterar sobre los resultados y agregar al ComboBox
                for resultado in resultados:
                    numero_recibo = resultado[0]
                    nombre_predio = resultado[1]
                    nombre_propietario = resultado[2]
                    apellido_propietario = resultado[3]
                    

                    # Crear la cadena que se mostrará en el ComboBox
                    display_text = f"{numero_recibo}-{nombre_predio}-{nombre_propietario} {apellido_propietario}"

                    # Agregar la cadena al ComboBox
                    self.ui.combo_usuario_recibo.addItem(display_text)

        except Exception as ex:
            print(ex)
        
        
        
    

    def llenar_recibo(self):
        # Obtener el número de recibo seleccionado en el ComboBox
        num_recibo_texto = self.ui.combo_usuario_recibo.currentText()

        # Utilizar expresiones regulares para extraer el número del recibo
        recibo_match = re.search(r'(\d+)-', num_recibo_texto)

        if recibo_match:
            num_recibo = int(recibo_match.group(1))

            try:
                with conexion.cursor() as cursor:
                    # Obtener datos del recibo actual
                    sql_actual = """SELECT recibo.num_recibo, recibo.nombres, recibo.apellidos, recibo.lectura_anterior, recibo.lectura_actual FROM recibo WHERE recibo.num_recibo = %s ;"""
                    cursor.execute(sql_actual, (num_recibo,))
                    resultados = cursor.fetchone()

                    if resultados:
                        self.ui.txt_num_recibo.setText(str(resultados[0]))
                        self.ui.txt_nombre_recibo.setText(f"{resultados[1]} {resultados[2]}")

                        lectura_anterior = resultados[3]
                        lectura_actual = resultados[4]

                        if lectura_actual:
                            self.ui.txt_lectura_ant_recibo.setText(str(lectura_anterior))
                            self.ui.txt_lectura_act_recibo.setText(str(lectura_actual))

                            resta_metros = lectura_actual - lectura_anterior

                            self.ui.txt_metros_recibo.setText(str(resta_metros))

                            # Actualizar la lectura anterior del próximo recibo
                            sql_siguiente = """UPDATE recibo SET lectura_anterior = %s WHERE num_recibo > %s ORDER BY num_recibo LIMIT 1;"""
                            cursor.execute(sql_siguiente, (lectura_actual, num_recibo))
                            
                        elif lectura_anterior:
                            self.ui.txt_lectura_ant_recibo.setText(str(lectura_anterior))
                            self.ui.txt_lectura_act_recibo.setText(str(lectura_actual))

                            resta_metros = lectura_actual - lectura_anterior

                            self.ui.txt_metros_recibo.setText(str(resta_metros))

                            # Actualizar la lectura anterior del próximo recibo
                            sql_siguiente = """UPDATE recibo SET lectura_anterior = %s WHERE num_recibo > %s ORDER BY num_recibo LIMIT 1;"""
                            cursor.execute(sql_siguiente, (lectura_actual, num_recibo))
                            
                        elif lectura_anterior is None:
                            self.ui.txt_lectura_act_recibo.setText(str(lectura_actual))
                            self.ui.txt_lectura_ant_recibo.setText("0")  # Asegúrate de configurar la lectura_anterior correctamente
                            self.ui.txt_metros_recibo.setText(str(lectura_actual))

                       
                            
                            

            except Exception as ex:
                # Mostrar un mensaje de error al usuario
                qtw.QMessageBox.critical(self, "Error", f"Error al obtener datos de consumo: {str(ex)}")
        else:
            qtw.QMessageBox.warning(self, "Advertencia", "No se pudo extraer el número de recibo del ComboBox.")


    #INTERFAZ OFICIOS
    def oficios(self):

        self.ui=Ui_interfaz_oficios()
        self.ui.setupUi(self)


        #acciones botones superiores
        self.ui.bt_restaurar.hide()
        self.click_posicion = None
        self.ui.bt_minimizar.clicked.connect(lambda: self.showMinimized())
        self.ui.bt_restaurar.clicked.connect(self.control_bt_restaurar)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_max)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())
        
        #mover ventana
        self.ui.frame_superior.mouseMoveEvent = self.mover_ventana   
        
        #botones de la barra
        self.ui.bt_crear_oficios.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_oficios)) 
        
        self.ui.bt_crear_oficios.clicked.connect(self.llenar_combo_oficios)

        self.ui.bt_imprimir_oficio.clicked.connect(self.imprimir_oficio)
        self.ui.bt_guardar_recibo.clicked.connect(self.guardar_oficio)

        self.ui.bt_buscar_oficio.clicked.connect(self.llenar_oficio)        

        self.ui.bt_regresar.clicked.connect(self.boton_regresar)
        
    
    def imprimir_oficio(self):
         # Captura solo el contenido del QFrame
        frame_content = self.ui.frame_oficios.grab()
        
        # Convierte la captura en un QPixmap
        pixmap = QPixmap(frame_content)

        # Configura el diálogo de impresión
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Inicia el proceso de impresión
            painter = QPainter(printer)
            
            # Dibuja la imagen en la página de impresión
            painter.drawPixmap(0, 0, pixmap)

            # Finaliza el proceso de impresión
            painter.end()
            
    def guardar_oficio(self):

        fecha = self.ui.txt_fecha.text()
        asunto = str(self.ui.txt_asunto.text())
        descripcion = str(self.ui.txt_descripcion.toPlainText())
        contador = self.ui.combo_usuario_oficio.currentText()

        #utilizar expresiones regulares para extraer el numero del contador
        numero_contador = re.search(r'(\d+)', contador)

        if numero_contador:
            numero_contador = int(numero_contador.group(1))
            
            try:
                with conexion.cursor() as cursor:
                    # Insertar datos en la tabla consumo
                    sql = "INSERT INTO oficio (asunto, descripcion, fecha) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (asunto, descripcion, fecha))

                    id_tipo_gastos = cursor.lastrowid


                    sql = "INSERT INTO propietario_oficio (id_oficio, id_propietario) VALUES (%s, %s)"
                    cursor.execute(sql, (id_tipo_gastos, numero_contador))

                    #FUNCION PARA GUARDAR OFICIO COMO IMAGEN

                    # Captura solo el contenido del QFrame
                    frame_content = self.ui.frame_oficios.grab()

                    # Convierte la captura en un QPixmap
                    pixmap = QPixmap(frame_content)

                    # Guarda el QPixmap como imagen
                    pixmap.save("C:/Users/Admin/Desktop/recibo2.png")
                    
                    # No necesitas cerrar la aplicación aquí, ya que esto podría cerrarla inmediatamente
                    # sys.exit(app.exec_())"""
                    
                    #Se limpian los campos luego de ingresar los datos
                    self.ui.txt_fecha.clear()
                    self.ui.txt_asunto.clear()
                    self.ui.txt_descripcion.clear()
                    self.ui.txt_dirigido.clear()
                    

                    if (cursor.execute):
                        qtw.QMessageBox.information(self, "Éxito", "Datos almacenados correctamente")
                            
                    else:
                        qtw.QMessageBox.critical(self, "Error", "No se almacenaron los datos")
    
                    
            except Exception as ex:
                # Mostrar un mensaje de error si hay algún problema
                print(ex)
                qtw.QMessageBox.critical(self, "Error", "Ha ocurrido un error al almacenar los datos de consumo.")
        else:
            qtw.QMessageBox.warning(self, "Advertencia", "No se pudo extraer el número del contador del ComboBox.")  
 

    
    def llenar_combo_oficios(self):
        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT propietario.id AS id_propietario, propietario.nombres, propietario.apellidos, predio.nombre_predio
                            FROM propietario
                            JOIN predio_propietario ON propietario.id = predio_propietario.id_propietario
                            JOIN predio ON predio_propietario.id_predio = predio.num_catastral;
                """

                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas
                cursor.execute(sql)

                # Obtener todos los resultados de la consulta
                resultados = cursor.fetchall()

                # Limpiar el contenido actual del ComboBox
                self.ui.combo_usuario_oficio.clear()

                # Iterar sobre los resultados y agregar al ComboBox
                for resultado in resultados:
                    id_propietario = resultado[0]
                    nombre_predio = resultado[1]
                    nombre_propietario = resultado[2]
                    apellido_propietario = resultado[3]
                    

                    # Crear la cadena que se mostrará en el ComboBox
                    display_text = f"{id_propietario}-{nombre_predio}-{nombre_propietario} {apellido_propietario}"

                    # Agregar la cadena al ComboBox
                    self.ui.combo_usuario_oficio.addItem(display_text)

        except Exception as ex:
            print(ex)

    def llenar_oficio(self):
        # Obtener el número de recibo seleccionado en el ComboBox
        listado_usuarios = self.ui.combo_usuario_oficio.currentText()

        # Utilizar expresiones regulares para extraer el número del recibo
        recibo_match = re.search(r'(\d+)-', listado_usuarios)

        if recibo_match:
            num_recibo = int(recibo_match.group(1))

            try:
                with conexion.cursor() as cursor:
                    sql = """SELECT propietario.nombres, propietario.apellidos 
                    FROM propietario 
                    JOIN recibo ON propietario.id = recibo.id_propietario 
                    WHERE recibo.num_recibo = %s;"""
                    cursor.execute(sql, (num_recibo,))

                    resultados = cursor.fetchone()

                    if resultados:
                        # Asignar resultados a QLabel
                        self.ui.txt_dirigido.setText(f"{resultados[0]} {resultados[1]}")
                        

                        # Opcional: No es necesario commit si solo es una consulta de lectura
                        # conexion.commit()

                        # Mostrar un mensaje de éxito
                        qtw.QMessageBox.information(self, "Éxito", "Datos de consumo obtenidos correctamente.")
                    else:
                        qtw.QMessageBox.warning(self, "Advertencia", f"No se encontraron datos para el recibo {num_recibo}.")

            except Exception as ex:
                # Mostrar un mensaje de error al usuario
                qtw.QMessageBox.critical(self, "Error", f"Error al obtener datos de consumo: {str(ex)}")
        else:
            qtw.QMessageBox.warning(self, "Advertencia", "No se pudo extraer el número de recibo del ComboBox.")
    
    
    
    

    #INTERFAZ GASTOS
    def gastos(self):

        self.ui=Ui_interfaz_gastos()
        self.ui.setupUi(self)


        #acciones botones superiores
        self.ui.bt_restaurar.hide()
        self.click_posicion = None
        self.ui.bt_minimizar.clicked.connect(lambda: self.showMinimized())
        self.ui.bt_restaurar.clicked.connect(self.control_bt_restaurar)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_max)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())
        
        #mover ventana
        self.ui.frame_superior.mouseMoveEvent = self.mover_ventana   
        
        #botones de la barra
        self.ui.bt_crear_gasto.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_gastos))
        self.ui.bt_editar_gasto.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_editar_gastos))
        self.ui.bt_eliminar_gasto.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_eliminar_gastos))

        self.ui.bt_crear_gasto.clicked.connect(self.llenar_combo_gastos)
        self.ui.bt_guardar_gasto.clicked.connect(self.guargar_gasto)
        self.ui.bt_actualizar_gastos.clicked.connect(self.actualizar_gasto)
        self.ui.bt_guardar_gastos.clicked.connect(self.guardar_datos_gastos)
        self.ui.bt_actualizar_tabla.clicked.connect(self.actualizar_tabla_eliminar_gasto)
        self.ui.bt_borrar_gasto.clicked.connect(self.eliminar_gasto)

        self.ui.bt_regresar.clicked.connect(self.boton_regresar)

    def llenar_combo_gastos(self):
        try:
            with conexion.cursor() as cursor:
                #se realiza la consulta la base de datos
                sql = """SELECT predio.nombre_predio, punto_agua.num_contador FROM predio JOIN punto_agua 
                ON predio.num_catastral = punto_agua.num_catastral_predio;

                """
                #se ejecuta la consulta sql
                cursor.execute(sql)

                #obtine todos los resultados de la consulta
                resultados = cursor.fetchall()

                #limia el contenidoactual del combobox
                self.ui.combo_contador_gastos.clear()

                #intera sobre los resultados y agrega el combobox
                for resultado in resultados:
                        nombre_predio = resultado[0]
                        punto_agua_num_contador = resultado[1]

                        #crea la cadena que se mostarara en el combobox
                        display_text = f"{nombre_predio}-{punto_agua_num_contador}"

                        #agrega la cadena la combobox
                        self.ui.combo_contador_gastos.addItem(display_text)
                    
        except Exception as ex:
            print(ex)

    def guargar_gasto(self):
        
        fecha = self.ui.txt_agregar_feccha.text()
        monto = int(self.ui.txt_agregar_monto.text())
        descripcion = str(self.ui.txt_agregar_descripcion.toPlainText())
        contador = self.ui.combo_contador_gastos.currentText()

        #utilizar expresiones regulares para extraer el numero del contador
        numero_contador = re.search(r'(\d+)', contador)

        if numero_contador:
            numero_contador = int(numero_contador.group(1))
            
            try:
                with conexion.cursor() as cursor:
                    # Insertar datos en la tabla consumo
                    sql = "INSERT INTO gasto_acueducto (descripcion, fecha, monto) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (descripcion, fecha, monto))

                    id_tipo_gastos = cursor.lastrowid


                    sql = "INSERT INTO gasto_acueducto_contador (id_tipo_gasto, num_contador_punto_agua) VALUES (%s, %s)"
                    cursor.execute(sql, (id_tipo_gastos, numero_contador))
                    
                    #Se limpian los campos luego de ingresar los datos
                    self.ui.txt_agregar_feccha.clear()
                    self.ui.txt_agregar_monto.clear()
                    self.ui.txt_agregar_descripcion.clear()
                    

                    if (cursor.execute):
                        qtw.QMessageBox.information(self, "Éxito", "Datos almacenados correctamente")
                            
                    else:
                        qtw.QMessageBox.critical(self, "Error", "No se almacenaron los datos")
    
                    
            except Exception as ex:
                # Mostrar un mensaje de error si hay algún problema
                print(ex)
                qtw.QMessageBox.critical(self, "Error", "Ha ocurrido un error al almacenar los datos de consumo.")
        else:
            qtw.QMessageBox.warning(self, "Advertencia", "No se pudo extraer el número del contador del ComboBox.")    
            
                
    
    def actualizar_gasto(self):
        tabla_gastos = self.ui.tabla_editar_gastos
        
        
        
        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT gasto_acueducto.id_tipo_gasto, gasto_acueducto.fecha, gasto_acueducto.monto, gasto_acueducto.descripcion, gasto_acueducto_contador.num_contador_punto_agua
FROM gasto_acueducto INNER JOIN gasto_acueducto_contador ON gasto_acueducto.id_tipo_gasto = gasto_acueducto_contador.id_tipo_gasto;"""
                
                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                gastos = cursor.fetchall()

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla_gastos is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(gastos)
                tabla_gastos.setRowCount(i)
                
                

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for usuario in gastos:
                        # Asegúrate de que los índices estén correctos según la estructura de tus datos
                        tabla_gastos.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(usuario[0])))
                        tabla_gastos.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(usuario[1])))
                        tabla_gastos.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(usuario[2])))
                        tabla_gastos.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(usuario[3])))
                        tabla_gastos.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(usuario[4])))
                                              
                        tabla_gastos.item(tablerow, 0).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla_gastos.item(tablerow, 1).setFlags(QtCore.Qt.ItemIsEnabled)
                        tabla_gastos.item(tablerow, 4).setFlags(QtCore.Qt.ItemIsEnabled)
                        
                        tablerow += 1
                else:
                    self.mensaje.setText("No existen gastos en el sistema")
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.exec()

        except Exception as ex:
            print(ex)


    def guardar_datos_gastos(self):
        tabla_gastos = self.ui.tabla_editar_gastos

        try:
            with conexion.cursor() as cursor:
                # Itera sobre las filas de la tabla y realiza la actualización en la base de datos
                for fila in range(tabla_gastos.rowCount()):
                    monto = int(tabla_gastos.item(fila, 2).text()) 
                    descripcion = str(tabla_gastos.item(fila, 3).text()) 
                    id_gastos = str(tabla_gastos.item(fila, 0).text()) 
                    
                    # Realiza la actualización en la base de datos
                    sql_gasto = """UPDATE gasto_acueducto
                    SET monto = %s, descripcion = %s
                    WHERE id_tipo_gasto = %s;"""

                    cursor.execute(sql_gasto, (monto, descripcion, id_gastos))
                    
            # Confirma los cambios en la base de datos
            conexion.commit()

            # Muestra un mensaje de éxito
            QMessageBox.information(self, "Éxito", "Los datos se han guardado correctamente.")
        except Exception as ex:
            print(ex)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error al guardar los datos.")


    def actualizar_tabla_eliminar_gasto(self):
        tabla = self.ui.tabla_eliminar_gastos  # Asegúrate de que este sea el nombre correcto de tu tabla

        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT gasto_acueducto.id_tipo_gasto, gasto_acueducto.monto, gasto_acueducto.descripcion, gasto_acueducto_contador.num_contador_punto_agua, gasto_acueducto.fecha
                FROM gasto_acueducto INNER JOIN gasto_acueducto_contador ON gasto_acueducto.id_tipo_gasto = gasto_acueducto_contador.id_tipo_gasto;"""
                
                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                usuarios_puntos = cursor.fetchall()

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(usuarios_puntos)
                tabla.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for usuario in usuarios_puntos:
                        # Asegúrate de que los índices estén correctos según la estructura de tus datos
                        tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(usuario[0])))
                        tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(usuario[1])))
                        tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(usuario[2])))
                        tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(usuario[3])))
                        tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(usuario[4])))
                                                                  
                        
                        tabla.item(tablerow, 0).setFlags(QtCore.Qt.ItemIsEnabled)
                        
                        tablerow += 1
                else:
                    self.mensaje.setText("No existen gastos")
                    self.mensaje.setIcon(QMessageBox.Warning)
                    self.mensaje.exec()

        except Exception as ex:
            print(ex)


    def eliminar_gasto(self):
        
        id_gasto = self.ui.txt_id_eliminar_gasto.text()
        
        try:
            with conexion.cursor() as cursor:
                # Consulta para eliminar el usuario por su ID
                sql = "DELETE FROM gasto_acueducto WHERE id_tipo_gasto = %s"
                cursor = conexion.cursor()
                cursor.execute(sql, (id_gasto,))

                if cursor.rowcount > 0:
                    qtw.QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                else:
                    qtw.QMessageBox.warning(self, "Advertencia", "No se encontró un usuario con ese ID")

        except Exception as ex:
            qtw.QMessageBox.critical(self, "Error", f"Error en la operación: {str(ex)}") 
                
                     
                
            
if __name__ == "__main__":
    app = qtw.QApplication([])
    widget = Login()
    widget.show()
    app.exec_() 

