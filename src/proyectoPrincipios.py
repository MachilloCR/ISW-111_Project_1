import smtplib
from colorit import *
import random
import json
import datetime as dt
from datetime import datetime
import ast
import string
from reportlab.pdfgen import canvas


Letra = list(string.ascii_uppercase[:26])
Letras = ("BCDFGHJKLMNPQRSTVWXYZ")

Lugares = [{'Lugar_T': 'San Jose'},{'Lugar_T': 'Alajuela'},{'Lugar_T': 'Heredia'},{'Lugar_T': 'Cartago'},{'Lugar_T': 'San Carlos'},{'Lugar_T': 'Puntarenas'},{'Lugar_T': 'Limon'}]

infoUTemp = []

# estructura de cada terminal {'ID':'','Nombre_Terminal':'','Ubicacion':'','Numero_Terminal':''}

# estructura de cada unidad/bus {'Placa': Placa_Unidad, 'Capacidad':36,'Terminal_Asignada':'','Ruta':''}

#{'ID': idRuta, 'ID_Terminal': idTerminal, 'Placa_Unidad': placaUnidad,'Precio': precio, 'Fecha&Hora_Salida': salidaDT,'Origen': lugarOrigen, 'Fecha&Hora_Llegada': fechaHoraLlegada,'Destino': lugarDestino,'Duracion': duracion}


def menuInicio():  # Menú de Inicial
    seleccion = 0
    print(color("\n=== Menú de Inicio ===",Colors.yellow))
    print(color("1) Iniciar Sesión  \n2) Registrarse   \n3) Salir",Colors.white))
    try:
        seleccion = int(input(color("Escoja una de las opciones anteriores: ",Colors.green)))
    except ValueError:
        print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
        menuInicio()
    if seleccion == 1:
        inicioSesion()
    else:
        if seleccion == 2:
            registroUsuario()
        else:
            if seleccion == 3:
                exit()
            else:
                print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
                menuInicio()


def inicioSesion():  # Login de Pasajeros y Admins
    usuarios = {}
    uLeer = open('Usuarios.txt', 'r')  # Abre el archivo con los usuarios actuales

    with uLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        for line in inf:
            usuarios = (eval(line))
        uLeer.close()
    print(color("\n=== Inicio de Sesión ===",Colors.yellow))
    cedula = input(color("\nDigite el número de cédula: ",Colors.green))
    contra = input(color("Digite la contraseña: ",Colors.green))
    if cedula in usuarios:
        if contra == usuarios[cedula][5]:
            if usuarios[cedula][6] == "a":
                print(color("\n         Acceso Autorizado",Colors.yellow))
                print(color("==== Bienvenido, Administrador ====",Colors.orange))
                Menu_Administrador()
            else:
                infoUTemp.append(cedula)
                infoUTemp.append(usuarios[cedula][0])
                infoUTemp.append(usuarios[cedula][2])
                infoUTemp.append(usuarios[cedula][3])
                print(color("\n       Acceso Autorizado", Colors.yellow))
                print(color("==== Bienvenido, Pasajero ====",Colors.orange))
                MenuPasajero()
        else:
            print(color("Contraseña o Usuario no identificado. Intente de nuevo.",Colors.orange))
            menuInicio()
    else:
        print(color("Contraseña o Usuario no identificado. Intente de nuevo.",Colors.orange))
        menuInicio()


def registroUsuario():  # Registro de Pasajeros
    uArchivo = open('Usuarios.txt', 'r')
    usuarios = {}

    with uArchivo as inf:  # Extrae los datos actuales del archivo de texto
        for line in inf:
            usuarios = (eval(line))
    print(color("\n=== Registro ===",Colors.yellow))
    cedula = input(color("\nDigite su número de cédula: ",Colors.green))
    if cedula in usuarios:
        print(color("Este número de cedula ya se encuentra registrado.",Colors.red))
        menuInicio()
    else:
        nombre = input(color("Digite su nombre completo: ",Colors.green))
        fechaN = input(color("Entre su fecha de nacimiento con el siguiente formato 'dd/mm/aaaa': ",Colors.green))
        try:
            dt.datetime.strptime(fechaN, '%d/%m/%Y')
        except ValueError:
            print(color("Formato incorrecto, debe de ser dd/mm/aaaa",Colors.red))
            registroUsuario()
        fEdad = datetime.strptime(fechaN, '%d/%m/%Y')
        edad = int((datetime.today() - fEdad).days / 365)
        email = input(color("Digite su dirección de email: ",Colors.green))
        genero = ""
        opcion = 0
        try:
            opcion = int(input(color("Digite 1 para 'Hombre' y 2 para 'Mujer': ",Colors.green)))
        except ValueError:
            print(color("## ¡Debe de escoger una de las opcione mostradas! ##\n",Colors.red))
            registroUsuario()
        if opcion == 1:
            genero = "Hombre"
        else:
            if opcion == 2:
                genero = "Mujer"
            else:
                print(color("## ¡Escoja una de las opciones permitidas! ##\n",Colors.red))
                registroUsuario()
        password = input(color("Digite su contraseña: ",Colors.green))
        identificador = "p"
        usuarios[cedula] = [nombre, fechaN, edad, email, genero, password, identificador]

        with open('Usuarios.txt', 'w+') as file:  # Actualiza la información del archivo de texto
            file.write(json.dumps(usuarios))  # use `json.loads` to do the reverse
        print(color("\nUsuario registrado con exito",Colors.orange))
        menuInicio()


################################       MENUS         ###############################


def Menu_Administrador():
    print(color("\n= Menú Administrador =",Colors.yellow))
    print(color("1) Mantenimiento De Terminales \n2) Mantenimiento De Unidades \n3) Mantenimiento de Rutas \n4) Reportes "
        "\n5) Cerrar sesion",Colors.white))
    try:
        seleccion = int(input(color("Escoja una de las opciones anteriores: ",Colors.green)))
    except ValueError:
        print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
        Menu_Administrador()

    if seleccion == 1:
        mantenimientoDeTerminales()
    elif seleccion == 2:
        mantenimiento_de_Unidades()
    elif seleccion == 3:
        mantenimientoRutas()
    elif seleccion == 4:
        reportes()
    else:
        print(color("Cerrar Sesión",Colors.orange))
        menuInicio()


def MenuPasajero():
    print(color("\n= Menú Pasajero =",Colors.yellow))
    print(color("1) Buscar Rutas\n2) Comprar Boletos\n3) Cerrar sesion",Colors.white))
    seleccion = int(input(color("Escoja una de las opciones anteriores: ",Colors.green)))
    if seleccion == 1:
        BuscarRutas()
    elif seleccion == 2:
        comprarBoletos()
    else:
        print("Cerrar sesion")
        menuInicio()


################################        TERMINALES         ###############################


def mantenimientoDeTerminales():  # Menú Principal para el mantenimiento de las Terminales
    while True:
        print(color("\n=== MENÚ TERMINALES ===",Colors.blue))
        print(color("1) Crear terminales \n2) Ver Terminales \n3) Modificar terminales \n4) Eliminar terminales \n5) Volver ",Colors.white))
        try:
            seleccion = int(input(color("Escoja una de las opciones anteriores: ",Colors.green)))
        except ValueError:
            print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
            mantenimientoDeTerminales()
        if seleccion == 1:
            crearTerminal()
        elif seleccion == 2:
            mostrarTerminales()
        elif seleccion == 3:
            modificarTerminal()
        elif seleccion == 4:
            eliminarTerminal()
        elif seleccion == 5:
            print('Saliendo de Mantenimiento de Terminales...\n')
            Menu_Administrador()
        else:
            print("\n## ¡Escoja una de las opciones permitidas! ##\n")
            mantenimientoDeTerminales()


def crearTerminal():  # Crea la terminal
    Lista_Lugares = []
    Lista_Terminales = []
    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con las Terminales actuales
    lugLeer = open('Lugares.txt', 'r')  # Abre el archivo con los Lugares actuales


    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with lugLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Lugares = ast.literal_eval(lugLeer.read())
    lugLeer.close()


    Numero_CodigoT = random.randint(1, 99)
    print(color("========= Crear Terminal =========", Colors.orange))
    Nombre_Terminal = str(input(color("Escriba el nombre de la terminal: ",Colors.green)))
    print(color("1>San José | 2>Alajuela | 3>Heredia | 4>Cartago | 5>San Carlos | 6>Puntarenas | 7>Limón",Colors.white))
    Selec_Lugar = int(input(color("Digite el número del lugar donde desea crear la terminal: ",Colors.green)))

    if Selec_Lugar == 1:  # crea el ID de las Terminales
        Siglas = "TSJ"
        ID_Terminal = Siglas + str(Numero_CodigoT)  # asgina el codigo a la terminal
        ubicacion_Terminal = Lugares[0]['Lugar_T']  # asigna el Lugar de la terminal
    elif Selec_Lugar == 2:
        Siglas = "TA"
        ID_Terminal = Siglas + str(Numero_CodigoT)
        ubicacion_Terminal = Lugares[1]['Lugar_T']
    elif Selec_Lugar == 3:
        Siglas = "TH"
        ID_Terminal = Siglas + str(Numero_CodigoT)
        ubicacion_Terminal = Lugares[2]['Lugar_T']
    elif Selec_Lugar == 4:
        Siglas = "TC"
        ID_Terminal = Siglas + str(Numero_CodigoT)
        ubicacion_Terminal = Lugares[3]['Lugar_T']
    elif Selec_Lugar == 5:
        Siglas = "TSC"
        ID_Terminal = Siglas + str(Numero_CodigoT)
        ubicacion_Terminal = Lugares[4]['Lugar_T']
    elif Selec_Lugar == 6:
        Siglas = "TP"
        ID_Terminal = Siglas + str(Numero_CodigoT)
        ubicacion_Terminal = Lugares[5]['Lugar_T']
    elif Selec_Lugar == 7:
        Siglas = "TL"
        ID_Terminal = Siglas + str(Numero_CodigoT)
        ubicacion_Terminal = Lugares[6]['Lugar_T']
    else:
        print(color("El lugar no existe",Colors.red))
        mantenimientoDeTerminales()
    # por si el numero del codigo ya esta asginado a otra terminal
    for a in Lista_Terminales:  # Saca la terminal de la lista
        if ID_Terminal == a['ID']:  # Pregunta el ID de la terminal y en caso de estar elimina la terminal
            Numero_CodigoT = random.randint(1, 99)
            ID_Terminal = Siglas + str(Numero_CodigoT)
        else:
            Terminal = {'ID': ID_Terminal, 'Nombre_Terminal': Nombre_Terminal, 'Ubicacion': ubicacion_Terminal,
                        'Numero_Terminal': '', 'Unidad_1': '', 'Unidad_2': ''}

    Terminal = {'ID': ID_Terminal, 'Nombre_Terminal': Nombre_Terminal, 'Ubicacion': ubicacion_Terminal,
                'Numero_Terminal': '', 'Unidad_1': '', 'Unidad_2': ''}

    # agrega la terminal a su respectiva ubicacion y le asigna el numero a la terminal "1 o 2"

    for b in Lista_Lugares:  # Saca la terminal de la lista
        if Terminal['Ubicacion'] == b['Ubicacion_T']:
            if b['Terminal_1'] == '':  # pregunta si la terminal 1 esta disponible
                Terminal = {'ID': ID_Terminal, 'Nombre_Terminal': Nombre_Terminal,'Ubicacion': ubicacion_Terminal, 'Numero_Terminal': '1', 'Unidad_1': '','Unidad_2': ''}
                b['Terminal_1'] = ID_Terminal
                Lista_Terminales.append(Terminal)

                with open('Terminales.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                    file.write(json.dumps(Lista_Terminales))

                with open('Lugares.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                    file.write(json.dumps(Lista_Lugares))

                print(color('\n¡Terminal creada exitosamente!\n',Colors.orange))
                mantenimientoDeTerminales()

            elif b['Terminal_2'] == '':
                Terminal = {'ID': ID_Terminal, 'Nombre_Terminal': Nombre_Terminal, 'Ubicacion': ubicacion_Terminal,'Numero_Terminal': '2', 'Unidad_1': '', 'Unidad_2': ''}
                b['Terminal_2'] = ID_Terminal
                Lista_Terminales.append(Terminal)

                with open('Terminales.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                    file.write(json.dumps(Lista_Terminales))

                with open('Lugares.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                    file.write(json.dumps(Lista_Lugares))

                print(color('\n¡Terminal creada exitosamente!\n',Colors.orange))


                mantenimientoDeTerminales()
            else:
                print(color("\nTodas las terminales estan llenas\n",Colors.red))
                mantenimientoDeTerminales()


def mostrarTerminales():  # Muestra las terminales existentes
    Lista_Terminales = []
    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales

    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()
    print(color("\n========= Mostrar Terminal =========", Colors.orange))
    print(color("= Lista de Terminales =",Colors.blue))
    for parada in Lista_Terminales:  # Saca cada Terminal de la lista
        for dato in parada:  # Saca cada dato de la terminal
                print(parada[dato], end="|")
        print("")
    mantenimientoDeTerminales()


def modificarTerminal():  # Modifica la terminal, realizando las verificaciones pertinentes
    contTerminal = 0
    Lista_Terminales = []
    Lista_Unidades = []
    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales

    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()
    print(color("\n========= Modificar Terminal =========", Colors.orange))
    print(color("= Lista de Terminales =",Colors.blue))
    for a in Lista_Terminales:
        print('ID: ', a['ID'], ' Nombre: ', a['Nombre_Terminal'])
    Modificar_Terminal = str(input(color("\nDigite el ID de la terminal a modificar: ",Colors.green)))
    contador = 0
    for Terminal_A_Modificar in Lista_Terminales:  # Saca la terminal de la lista
        if Modificar_Terminal == Terminal_A_Modificar['ID']:  # Pregunta el ID de la terminal
            if Terminal_A_Modificar['Unidad_1'] != '':
                for u in Lista_Unidades:
                    if u['Placa'] == Terminal_A_Modificar['Unidad_1']:
                        if u['Ruta'] != '':
                            print(color('\nEsta terminal no puede ser editada ya que tiene rutas registradas\n',Colors.red))
                            mantenimientoDeTerminales()
                        elif Terminal_A_Modificar['Unidad_2'] != '':
                            for u2 in Lista_Unidades:
                                if u2['Placa'] == Terminal_A_Modificar['Unidad_2']:
                                    if u2['Ruta'] != '':
                                        print(color('\nEsta terminal no puede ser editada ya que tiene rutas registradas\n',Colors.red))
                                        mantenimientoDeTerminales()
                                    else:
                                        Nuevo_Nombre_T = str(input(color("Digite el Nuevo nombre de la terminal",Colors.green)))
                                        Terminal_A_Modificar['Nombre_Terminal'] = Nuevo_Nombre_T  # Cambia el nombre de la terminal

                                        with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                            file.write(
                                                json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                                        print(color('\nTerminal Modificada\n',Colors.orange))
                                        break
                                        mantenimientoDeTerminales()
                        else:
                            Nuevo_Nombre_T = str(input(color("Digite el Nuevo nombre de la terminal",Colors.green)))
                            Terminal_A_Modificar['Nombre_Terminal'] = Nuevo_Nombre_T  # Cambia el nombre de la terminal

                            with open('Terminales.txt',
                                      'w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                file.write(
                                    json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                            print(color('\nTerminal Modificada\n',Colors.orange))
                            break
                            mantenimientoDeTerminales()
            elif Terminal_A_Modificar['Unidad_2'] != '':
                for u in Lista_Unidades:
                    if u['Placa'] == Terminal_A_Modificar['Unidad_2']:
                        if u['Ruta'] != '':
                            print(color('\nEsta terminal no puede ser editada ya que tiene rutas registradas\n',Colors.red))
                            mantenimientoDeTerminales()
                        else:
                            Nuevo_Nombre_T = str(input(color("Digite el Nuevo nombre de la terminal",Colors.green)))
                            Terminal_A_Modificar['Nombre_Terminal'] = Nuevo_Nombre_T  # Cambia el nombre de la terminal

                            with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                file.write(
                                    json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                            print(color('\nTerminal Modificada\n',Colors.orange))
                            break
                            mantenimientoDeTerminales()
            else:
                Nuevo_Nombre_T = str(input(color("Digite el Nuevo nombre de la terminal",Colors.green)))
                Terminal_A_Modificar['Nombre_Terminal'] = Nuevo_Nombre_T  # Cambia el nombre de la terminal

                with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                    file.write(
                        json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                print(color('\nTerminal Modificada\n',Colors.orange))
                break
                mantenimientoDeTerminales()
        else:
            contTerminal += 1
    if contTerminal == len(Lista_Terminales):
        print(color('Terminal no encontrada',Colors.red))
        mantenimientoDeTerminales()


def eliminarTerminal():  # Elimina la terminal, realizando las verificaciones pertinentes
    contador = 0

    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales
    lugLeer = open('Lugares.txt', 'r')  # Abre el archivo con los Lugares actuales

    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()

    with lugLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Lugares = ast.literal_eval(lugLeer.read())
    lugLeer.close()
    print(color("\n========= Eliminar Terminal =========", Colors.orange))
    print(color("= Lista de Terminales =",Colors.blue))
    for a in Lista_Terminales:
        print('ID: ', a['ID'], ' Nombre: ', a['Nombre_Terminal'])
    Eliminar_Terminal = str(input(color("\nDigite el ID de la terminal a eliminar",Colors.green)))
    contador = 0
    for Terminal_A_Modificar in Lista_Terminales:  # Saca la terminal de la lista
        if Eliminar_Terminal == Terminal_A_Modificar['ID']:  # Pregunta el ID de la terminal
            if Terminal_A_Modificar['Unidad_1'] != '':
                for u in Lista_Unidades:
                    if u['Placa'] == Terminal_A_Modificar['Unidad_1']:
                        if u['Ruta'] != '':
                            print(color('\nEsta terminal no puede ser eliminada ya que tiene rutas registradas\n',Colors.red))
                            mantenimientoDeTerminales()
                        elif Terminal_A_Modificar['Unidad_2'] != '':
                            for u2 in Lista_Unidades:
                                if u2['Placa'] == Terminal_A_Modificar['Unidad_2']:
                                    if u2['Ruta'] != '':
                                        print(color('\nEsta terminal no puede ser eliminada ya que tiene rutas registradas\n',Colors.red))
                                        mantenimientoDeTerminales()
                                    else:
                                        for tL in Lista_Lugares:
                                            if Eliminar_Terminal == tL['Terminal_1']:
                                                tL['Terminal_1'] = ''
                                                break
                                            elif Eliminar_Terminal == tL['Terminal_2']:
                                                tL['Terminal_2'] = ['']
                                                break
                                        Lista_Terminales.remove(Terminal_A_Modificar)
                                        Lista_Unidades.remove(u)
                                        Lista_Unidades.remove(u2)

                                        with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                            file.write(json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                                        with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                                            file.write(json.dumps(Lista_Unidades))

                                        with open('Lugares.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                                            file.write(json.dumps(Lista_Lugares))

                                        print('\nTerminal Eliminada\n')
                                        break
                                        mantenimientoDeTerminales()
                        else:
                            for tL in Lista_Lugares:
                                if Eliminar_Terminal == tL['Terminal_1']:
                                    tL['Terminal_1'] = ''
                                    break
                                elif Eliminar_Terminal == tL['Terminal_2']:
                                    tL['Terminal_2'] = ''
                                    break
                            Lista_Terminales.remove(Terminal_A_Modificar) #Elimina la terminal
                            Lista_Unidades.remove(u)

                            with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                file.write(json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                            with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                                file.write(json.dumps(Lista_Unidades))

                            with open('Lugares.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                                file.write(json.dumps(Lista_Lugares))

                            print(color('\nTerminal Eliminada\n',Colors.orange))
                            break
                            mantenimientoDeTerminales()
            elif Terminal_A_Modificar['Unidad_2'] != '':
                for uDos in Lista_Unidades:
                    if uDos['Placa'] == Terminal_A_Modificar['Unidad_2']:
                        if uDos['Ruta'] != '':
                            print(color('\nEsta terminal no puede ser eliminada ya que tiene rutas registradas\n',Colors.red))
                            mantenimientoDeTerminales()
                        else:
                            for tL in Lista_Lugares:
                                if Eliminar_Terminal == tL['Terminal_1']:
                                    tL['Terminal_1'] = ''
                                    break
                                elif Eliminar_Terminal == tL['Terminal_2']:
                                    tL['Terminal_2'] = ''
                                    break
                            Lista_Terminales.remove(Terminal_A_Modificar)  # Elimina la terminal
                            Lista_Unidades.remove(uDos)

                            with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                file.write(json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                            with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                                file.write(json.dumps(Lista_Unidades))

                            with open('Lugares.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                                file.write(json.dumps(Lista_Lugares))

                            print(color('\nTerminal Eliminada\n',Colors.orange))
                            break
                            mantenimientoDeTerminales()
            else:
                for tL in Lista_Lugares:
                    if Eliminar_Terminal == tL['Terminal_1']:
                        tL['Terminal_1'] = ''
                        break
                    elif Eliminar_Terminal == tL['Terminal_2']:
                        tL['Terminal_2'] = ''
                        break
                Lista_Terminales.remove(Terminal_A_Modificar)  # Elimina la terminal

                with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                    file.write(json.dumps(Lista_Terminales))  # use `json.loads` to do the reverse

                with open('Lugares.txt', 'w+') as file:  # Actualiza la información del archivo de texto
                    file.write(json.dumps(Lista_Lugares))

                print(color('\nTerminal Eliminada\n',Colors.orange))
                mantenimientoDeTerminales()
        else:
            contador = contador + 1
    if contador == len(Lista_Terminales):
        print(color('Terminal no encontrada',Colors.red))
        mantenimientoDeTerminales()

##################################        UNIDADES          ##############################

def mantenimiento_de_Unidades():  # Menú Principal para el mantenimiento de las Unidades
    while True:
        print(color("\n=== MENÚ UNIDADES ===", Colors.blue))
        print(color("1) Crear unidades \n2) Ver Unidades \n3) Modificar Unidades \n4) Eliminar Unidades \n5) Volver ",Colors.white))
        seleccion = int(input(color("Escoja una de las opciones anteriores: ",Colors.green)))
        if seleccion == 1:
            crearUnidad()
        elif seleccion == 2:
            mostraUnidades()
        elif seleccion == 3:
            modificarUnidades()
        elif seleccion == 4:
            eliminarUnidades()
        elif seleccion == 5:
            print(color('Saliendo de Mantenimiento de Unidades...\n',Colors.orange))
            Menu_Administrador()
        else:
            print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
            mantenimientoDeTerminales()#


def crearUnidad():  # Crea la unidad
    Lista_Terminales = []
    Lista_Unidades = []
    asientosbus = []

    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales

    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()


    # aqui se crea la placa del cada bus/unidad
    i = 1
    Letras_Placa = ""
    Numeros_Placa = str(random.randint(100, 999))
    while i < 4:
        LRandom = random.choice(Letras)
        Letras_Placa = Letras_Placa + LRandom
        i = i + 1
    Placa_Unidad = Letras_Placa + Numeros_Placa

    print(color("========= Crear Unidad =========", Colors.orange))
    Bus_Terminal = str(input(color("Digite la ID de la terminal a la cual quiere asignar esta unidad: ",Colors.green)))
    print(color("*La capacidad Maxima de que puede terner la unidad es de 36*", Colors.orange))
    Capacidad_Unidad = str(input(color("Digite la capacidad de esta unidad: ",Colors.green)))
    # Registra la unidad a la terminal
    if Capacidad_Unidad <= "36":
        a=1
    else:
        print(color("\nEl numero de asientos esta fuera del rango permitido\n",Colors.red))
        crearUnidad()
    ########################## CREA LA MATRIZ DE ASIENTOS########################
    for i in range(6):
        asientosbus.append([])  # inserta la lista que funciona como Filas
        for j in range(6):
            nombre_asiento = str(1 + i) + Letra[j]
            asiento = {'nombre': nombre_asiento, 'nombre_color': ''}
            asientosbus[i].append(asiento)  # agrega el valor de la columna en este caso es un dict
    contador = 0
    for a in Lista_Terminales:  # Saca la terminal de la lista
        if a['ID'] == Bus_Terminal:
            if a['Unidad_1'] == '':
                Bus = {'Placa': Placa_Unidad, 'Capacidad': Capacidad_Unidad,'Asientos':asientosbus, 'Terminal_Asignada': a['ID'], 'Ruta': ''}
                a['Unidad_1'] = Bus['Placa']
                Lista_Unidades.append(Bus)

                with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                    file.write(json.dumps(Lista_Terminales))

                with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                    file.write(json.dumps(Lista_Unidades))

                print(color('\nUnidad Creada\n',Colors.orange))
                mantenimiento_de_Unidades()

            elif a['Unidad_2'] == '':
                Bus = {'Placa': Placa_Unidad, 'Capacidad': Capacidad_Unidad,'Asientos':asientosbus, 'Terminal_Asignada': a['ID'], 'Ruta': ''}
                a['Unidad_2'] = Bus['Placa']
                Lista_Unidades.append(Bus)

                with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                    file.write(json.dumps(Lista_Terminales))

                with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                    file.write(json.dumps(Lista_Unidades))

                print(color('\nUnidad Creada\n',Colors.orange))
                mantenimiento_de_Unidades()
            else:
                print(color('\nNo es posible registrar más unidades a esta terminal\n',Colors.red))
                mantenimiento_de_Unidades()
        else:
            contador += 1
    if contador == len(Lista_Terminales):
        print(color("\nLa ID no pertenece a ninguna terminal registrada\n",Colors.red))
        mantenimiento_de_Unidades()


def mostraUnidades():  # Muestra las unidades existentes
    Lista_Unidades = []
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()
    print(color("========= Mostrar Unidad =========", Colors.orange))
    print(color("= Lista De Unidades =",Colors.blue))
    for uni in Lista_Unidades:
        print('Placa: ', uni['Placa'],'Capacidad: ',uni['Capacidad'],' Terminal Asignada: ', uni['Terminal_Asignada'],'Ruta: ',uni['Ruta'])
    print("")
    mantenimiento_de_Unidades()


def modificarUnidades():
    Lista_Terminales = []
    Lista_Unidades = []
    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales

    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()

    print(color("========= Modificar Unidad =========", Colors.orange))
    print(color("= Lista De Unidades =", Colors.blue))
    for a in Lista_Unidades:
        print('Placa: ', a['Placa'], ' Terminal Asignada: ', a['Terminal_Asignada'])
    Modificar_Unidad = input(color("\nDigite la placa de la unidad a modificar: ",Colors.green))
    cU = 0
    for ru in Lista_Unidades:
        if Modificar_Unidad == ru['Placa']:
            if ru['Ruta'] == '':
                nueva_Terminal = str(input(color("Digite ID de la nueva terminal a asignar: ",Colors.green)))
                contador = 0
                for t in Lista_Terminales:
                    if nueva_Terminal == t['ID']:
                        if t['Unidad_1'] == '':
                            t['Unidad_1'] = ru['Placa']
                            ru['Terminal_Asignada'] = nueva_Terminal

                            with open('Terminales.txt',
                                      'w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                file.write(
                                    json.dumps(Lista_Terminales))

                            with open('Unidades.txt',
                                      'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                                file.write(
                                    json.dumps(Lista_Unidades))

                            print(color('\nUnidad Modificada\n',Colors.orange))
                            mantenimiento_de_Unidades()
                        elif t['Unidad_2'] == '':
                            t['Unidad_2'] = ru['Placa']
                            ru['Terminal_Asignada'] = nueva_Terminal

                            with open('Terminales.txt',
                                      'w+') as file:  # Actualiza la información del archivo de texto - Terminales
                                file.write(
                                    json.dumps(Lista_Terminales))

                            with open('Unidades.txt',
                                      'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                                file.write(
                                    json.dumps(Lista_Unidades))

                            print(color('\nUnidad Modificada\n',Colors.orange))
                            mantenimiento_de_Unidades()
                        else:
                            print(color("\nEsa terminal cuenta con el maximo de unidades permitido\n", Colors.red))
                            mantenimiento_de_Unidades()
                    else:
                        contador += 1
                if contador == len(Lista_Terminales):
                    print(color("\nNo existe una terminal bajo ese nombre\n", Colors.red))
                    mantenimiento_de_Unidades()
            else:
                print(color("\nLa unidad tiene rutas registradas\n", Colors.red))
                mantenimiento_de_Unidades()
        else:
            cU += 1
    if cU == len(Lista_Unidades):
        print(color("\nPlaca no válida\n", Colors.red))
        mantenimiento_de_Unidades()


def eliminarUnidades(): #Elimina la ruta existente y la elimina también de la unidad asignada
    Lista_Terminales = []
    Lista_Unidades = []
    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales


    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()

    print(color("========= Eliminar Unidad =========", Colors.orange))
    print(color("= Lista De Unidades =", Colors.blue))
    for a in Lista_Unidades:
        print('Placa: ', a['Placa'], ' Terminal Asignada: ', a['Terminal_Asignada'])
    Modificar_Unidad = input(color("\nDigite la placa de la unidad a eliminar: ",Colors.green))
    cU = 0
    for ru in Lista_Unidades:
        if Modificar_Unidad == ru['Placa']:
            if ru['Ruta'] == '':
                for uni in Lista_Terminales:
                    if uni['Unidad_1'] == ru['Placa']:
                        uni['Unidad_1'] = ''
                        Lista_Unidades.remove(ru)

                        with open('Terminales.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                            file.write(json.dumps(Lista_Terminales))

                        with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                            file.write(json.dumps(Lista_Unidades))

                        print(color("\nUnidad Eliminada\n", Colors.orange))
                        mantenimiento_de_Unidades()
                    elif uni['Unidad_2'] == ru['Placa']:
                        uni['Unidad_2'] = ''
                        Lista_Unidades.remove(ru)

                        with open('Terminales.txt',
                                  'w+') as file:  # Actualiza la información del archivo de texto - Terminales
                            file.write(
                                json.dumps(Lista_Terminales))

                        with open('Unidades.txt',
                                  'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                            file.write(
                                json.dumps(Lista_Unidades))

                        print(color("\nUnidad Eliminada\n", Colors.orange))
                        mantenimiento_de_Unidades()
            else:
                print(color("\nLa unidad tiene rutas registradas\n", Colors.red))
                mantenimiento_de_Unidades()
        else:
            cU += 1
    if cU == len(Lista_Unidades):
        print(color("\nPlaca no válida\n", Colors.red))
        eliminarUnidades()

##################################        RUTAS         ##############################

def mantenimientoRutas():
    global seleccion
    while True:
        print(color("\n=== MENÚ RUTAS ===", Colors.blue))
        print(color("1) Crear Rutas \n2) Ver Rutas \n3) Modificar Rutas \n4) Eliminar Rutas \n5) Volver ",Colors.white))
        try:
            seleccion = int(input(color("Escoja una de las opciones anteriores: ",Colors.green)))
        except ValueError:
            print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
            mantenimientoRutas()
        if seleccion == 1:
            crearRuta()
        elif seleccion == 2:
            mostrarRutas()
        elif seleccion == 3:
            modificarRutas()
        elif seleccion == 4:
            eliminarRuta()
        elif seleccion == 5:
            print(color('Saliendo de Mantenimiento de Rutas...\n',Colors.orange))
            Menu_Administrador()
        else:
            print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
            mantenimientoRutas()

def crearRuta(): #Crea la ruta
    contadorLU = 0  # Contador de iteraciones de la lista de terminales
    contadorUR = 0  # Contador para verificar que se encontrarón
    contadorLT = 0
    Lista_Terminales = []
    Lista_Unidades = []
    Lista_Rutas = []
    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales
    ruLeer = open('Rutas.txt', 'r')  # Abre el archivo con los usuarios actuales

    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()

    with ruLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Rutas = ast.literal_eval(ruLeer.read())
    ruLeer.close()

    print(color("========= Crear Ruta =========", Colors.orange))
    idTerminal = ''
    placaUnidad = ''
    if not Lista_Rutas:
        idRuta = 1
    else:
        idRuta = Lista_Rutas[len(Lista_Rutas)-1]["ID"] + 1
    print(color("1>San José | 2>Alajuela | 3>Heredia | 4>Cartago | 5>San Carlos | 6>Puntarenas | 7>Limón", Colors.white))
    opOrigen = int(input(color("Digite el lugar de salida: ",Colors.green)))  # Permite escoger el lugar de Origen
    if opOrigen == 1:  # crea el ID de las Terminales
        lugarOrigen = "San Jose"
    elif opOrigen == 2:
        lugarOrigen = "Alajuela"
    elif opOrigen == 3:
        lugarOrigen = "Heredia"
    elif opOrigen == 4:
        lugarOrigen = "Cartago"
    elif opOrigen == 5:
        lugarOrigen = "San Carlos"
    elif opOrigen == 6:
        lugarOrigen = "Puntarenas"
    elif opOrigen == 7:
        lugarOrigen = "Limon"
    else:
        print(color("El lugar no existe", Colors.red))
        crearRuta()
    print(color("1>San José | 2>Alajuela | 3>Heredia | 4>Cartago | 5>San Carlos | 6>Puntarenas | 7>Limón", Colors.white))
    opDestino = int(input(color("Digite el lugar de Destino: ",Colors.green)))  # Permite escoger el lugar de destino
    if opDestino == 1:  # crea el ID de las Terminales
        lugarDestino = "San Jose"
    elif opDestino == 2:
        lugarDestino = "Alajuela"
    elif opDestino == 3:
        lugarDestino = "Heredia"
    elif opDestino == 4:
        lugarDestino = "Cartago"
    elif opDestino == 5:
        lugarDestino = "San Carlos"
    elif opDestino == 6:
        lugarDestino = "Puntarenas"
    elif opDestino == 7:
        lugarDestino = "Limon"
    else:
        print(color("El lugar no existe", Colors.red))
        crearRuta()

    if lugarOrigen == lugarDestino:  # Comprueba que el lugar de origen y llegada no sean el mismo
        print(color("El Lugar de Salida y Destino no pueden ser el mismo", Colors.red))
        crearRuta()
    try:
        precio = int(input(color("Digite el precio que va a tener esa ruta: ",Colors.green)))
    except ValueError:
        print(color("## Debe de registrar un valor númeral ##\n",Colors.red))
        crearRuta()
    fechaSalida = input(color("Digite la fecha de salidad con el siguiente formato 'dd-mm-aaaa': ",Colors.green))
    try:
        dt.datetime.strptime(fechaSalida, '%d-%m-%Y')
    except ValueError:
        print(color("Formato incorrecto, debe de ser dd-mm-aaaa",Colors.red))
        crearRuta()
    horaSalida = input(color("Digite la hora de la salida con el siguiente formato 'HH:MM': ",Colors.green))
    try:
        dt.datetime.strptime(horaSalida, '%H:%M')
    except ValueError:
        print(color("Formato incorrecto, debe de ser HH:MM",Colors.red))
        crearRuta()

    try:
        horas = int(input(color("Digite la cantidad de horas que durará el viaje: ",Colors.green)))
    except ValueError:
        print(color("## Debe de registrar un valor númeral ##\n",Colors.red))
        crearRuta()
    try:
        minutos = int(input(color("Digite la cantidad de minutos que durará el viaje: ",Colors.green)))
    except ValueError:
        print(color("## Debe de registrar un valor númeral ##\n",Colors.red))
        crearRuta()
    dHoras = dt.timedelta(hours=horas)
    dMinutos = dt.timedelta(minutes=minutos)

    salidaTotal = fechaSalida+' '+horaSalida
    salidaDT = datetime.strptime(salidaTotal, '%d-%m-%Y %H:%M')

    duracion = dHoras + dMinutos
    fechaHoraLlegada = (salidaDT + dHoras + dMinutos)

    for x in Lista_Terminales:
        if lugarOrigen == x['Ubicacion']:
            for y in Lista_Unidades:
                if x['Unidad_1'] == y['Placa'] or x['Unidad_2'] == y['Placa']:
                    if y['Ruta'] == '':
                        contadorUR = 1
                        y['Ruta'] = idRuta
                        idTerminal = x['ID']
                        placaUnidad = y['Placa']
                        break
                else:
                    contadorLU += 1
            if contadorUR == 1:
                Ruta = {'ID': idRuta, 'ID_Terminal': idTerminal, 'Placa_Unidad': placaUnidad,
                        'Precio': precio, 'Fecha&Hora_Salida': str(salidaDT),'Origen': lugarOrigen, 'Fecha&Hora_Llegada': str(fechaHoraLlegada),
                        'Destino': lugarDestino,'Duracion': str(duracion)}  # Crea diccionario de la Ruta para almacenarse en la lista
                Lista_Rutas.append(Ruta)
                with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Terminales
                    file.write(json.dumps(Lista_Unidades))

                with open('Rutas.txt',
                            'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                    file.write(
                        json.dumps(Lista_Rutas))

                print(color('\nRuta creada exitosamente\n',Colors.orange))
                break
                mantenimientoRutas()
            elif contadorLU == len(Lista_Unidades):
                print(color("No hay unidades disponibles\n",Colors.red))
                mantenimientoRutas()
        else:
            contadorLT += 1
    if contadorLT == len(Lista_Terminales):
        print(color('No existen terminales para ese lugar\n',Colors.red))
        mantenimientoRutas()

def mostrarRutas():
    Lista_Rutas = []
    ruLeer = open('Rutas.txt', 'r')  # Abre el archivo con los usuarios actuales

    with ruLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Rutas = ast.literal_eval(ruLeer.read())
    ruLeer.close()
    print(color("========= Mostrar Rutas =========", Colors.orange))
    print(color("= Lista De Rutas =", Colors.blue))
    for rutas in Lista_Rutas:  # Saca cada unidad de la lista
        for dato in rutas:  # Saca cada dato de la unidad
            print(rutas[dato], end="|")
        print("")
    mantenimientoRutas()

def modificarRutas(): #Modifica Rutas
    Lista_Rutas = []
    Lista_Historial =[]
    uHistorial = open('Historial.txt', 'r')  # Abre el archivo con los usuarios actuales
    ruLeer = open('Rutas.txt', 'r')

    with ruLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Rutas = ast.literal_eval(ruLeer.read())
    ruLeer.close()

    with uHistorial as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Historial = ast.literal_eval(uHistorial.read())
    uHistorial.close()
    print(color("========= Modificar Ruta =========", Colors.orange))
    print(color("= Lista De Rutas =", Colors.blue))
    for x in Lista_Rutas:
        print('ID: ', x['ID'],' ID de la Terminal Asignada: ',x['ID_Terminal'],' Unidad Asignada: ',x['Placa_Unidad'],' Lugar Origen: ',x['Origen'],' Lugar Destino: ',x['Destino'])
    Modificar_Ruta = int(input(color("\nDigite la ID de la ruta a  modificar: ",Colors.green)))
    cr = 0
    for lr in Lista_Rutas:
        if Modificar_Ruta == lr['ID']:
            cr2 = 0
            for lh in Lista_Historial:
                if Modificar_Ruta == lh['ID_Ruta']:
                    print(color('\nEsta ruta tiene compra de boletos registrada.\n',Colors.red))
                    mantenimientoRutas()
                else:
                    cr2 += 1
            if cr2 == len(Lista_Historial):
                print(color("== Datos a Modificar ==",Colors.blue))
                print(color("1) Fecha y Hora de Salida/Llegada junto a duración del viaje\n  2) Precio\n", Colors.white))

                opcion = int(input(color('Que dato desea modificar: ',Colors.green)))
                if opcion == 1:
                    fechaSalida = input(color("Digite la fecha de salidad con el siguiente formato 'dd-mm-aaaa': ",Colors.green))
                    try:
                        dt.datetime.strptime(fechaSalida, '%d-%m-%Y')
                    except ValueError:
                        print(color("Formato incorrecto, debe de ser dd-mm-aaaa",Colors.red))
                        mantenimientoRutas()
                    horaSalida = input(color("Digite la hora de la salida con el siguiente formato 'HH:MM': ",Colors.green))
                    try:
                        dt.datetime.strptime(horaSalida, '%H:%M')
                    except ValueError:
                        print(color("Formato incorrecto, debe de ser HH:MM",Colors.red))
                        mantenimientoRutas()
                    try:
                        horas = int(input(color("Digite la cantidad de horas que durará el viaje: ",Colors.green)))
                    except ValueError:
                        print(color("## Debe de registrar un valor númeral ##\n",Colors.red))
                        mantenimientoRutas()
                    try:
                        minutos = int(input(color("Digite la cantidad de minutos que durará el viaje: ",Colors.green)))
                    except ValueError:
                        print(color("## Debe de registrar un valor númeral ##\n",Colors.red))
                        mantenimientoRutas()
                    dHoras = dt.timedelta(hours=horas)
                    dMinutos = dt.timedelta(minutes=minutos)

                    salidaTotal = fechaSalida + ' ' + horaSalida
                    salidaDT = datetime.strptime(salidaTotal, '%d-%m-%Y %H:%M')

                    duracion = dHoras + dMinutos
                    fechaHoraLlegada = (salidaDT + dHoras + dMinutos)
                    lr["Fecha&Hora_Salida"] = str(salidaDT)
                    lr["Fecha&Hora_Llegada"] = str(fechaHoraLlegada)
                    lr["Duracion"] = str(duracion)

                    with open('Rutas.txt',
                              'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                        file.write(
                            json.dumps(Lista_Rutas))

                    print(color('Datos actualizados exitosamente\n',Colors.orange))
                    mantenimientoRutas()

                elif opcion == 2:
                    precioNuevo = int(input(color("Digite el nuevo precio para esa ruta: ",Colors.green)))
                    lr["Precio"] = precioNuevo

                    with open('Rutas.txt',
                              'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                        file.write(
                            json.dumps(Lista_Rutas))

                    print(color('Datos actualizados exitosamente\n',Colors.orange))
                    mantenimientoRutas()
                else:
                    print(color("## ¡Escoja una de las opciones mostradas! ##\n",Colors.red))
                    mantenimientoRutas()
        else:
          cr += 1
    if cr == len(Lista_Rutas):
        print(color('\nID no válida\n',Colors.red))
        mantenimientoRutas()

def eliminarRuta():
    Lista_Unidades = []
    Lista_Rutas = []
    Lista_Historial = []
    uHistorial = open('Historial.txt', 'r')  # Abre el archivo con los usuarios actuales
    ruLeer = open('Rutas.txt', 'r')
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()

    with ruLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Rutas = ast.literal_eval(ruLeer.read())
    ruLeer.close()

    with uHistorial as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Historial = ast.literal_eval(uHistorial.read())
    uHistorial.close()
    print(color("========= Elimnar Ruta =========", Colors.orange))
    print(color("= Lista De Rutas =", Colors.blue))
    for x in Lista_Rutas:
        print('ID: ', x['ID'], ' ID de la Terminal Asignada: ', x['ID_Terminal'], ' Unidad Asignada: ',
              x['Placa_Unidad'], ' Lugar Origen: ', x['Origen'], ' Lugar Destino: ', x['Destino'])
    Modificar_Ruta = int(input(color("\nDigite la ID de la ruta a eliminar: ",Colors.green)))
    cr = 0
    for lr in Lista_Rutas:
        if Modificar_Ruta == lr['ID']:
            cr2 = 0
            for lh in Lista_Historial:
                if Modificar_Ruta == lh['ID_Ruta']:
                    print(color('\nEsta ruta tiene compra de boletos registrada.\n',Colors.red))
                    mantenimientoRutas()
                else:
                    cr2 += 1
            if cr2 == len(Lista_Historial):
                for idU in Lista_Unidades:
                    if Modificar_Ruta == idU["Ruta"]:
                        idU["Ruta"] = ''
                        Lista_Rutas.remove(lr)

                        with open('Unidades.txt',
                                  'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                            file.write(
                                json.dumps(Lista_Unidades))

                        with open('Rutas.txt',
                                  'w+') as file:  # Actualiza la información del archivo de texto - Unidades
                            file.write(
                                json.dumps(Lista_Rutas))

                        print(color('Ruta eliminada de manera exitosa\n',Colors.orange))
                        mantenimientoRutas()

        else:
            cr += 1
    if cr == len(Lista_Rutas):
        print(color('\nID no válida\n',Colors.red))
        mantenimientoRutas()

##################################        PASAJEROS         ##############################

def BuscarRutas():
    Rutas_Temporales = []
    Lista_Terminales = []
    Lista_Unidades = []
    Lista_Rutas = []
    Lista_Lugares = []
    lugLeer = open('Lugares.txt', 'r')  # Abre el archivo con los Lugares actuales
    tLeer = open('Terminales.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')  # Abre el archivo con los usuarios actuales
    ruLeer = open('Rutas.txt', 'r')  # Abre el archivo con los usuarios actuales

    with tLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Terminales = ast.literal_eval(tLeer.read())
    tLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()

    with ruLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Rutas = ast.literal_eval(ruLeer.read())
    ruLeer.close()

    with lugLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Lugares = ast.literal_eval(lugLeer.read())
    lugLeer.close()

    print(color("\n== Bienvenido a Busqueda de Rutas ==\n", Colors.blue))
    print(
        color("1>San José | 2>Alajuela | 3>Heredia | 4>Cartago | 5>San Carlos | 6>Puntarenas | 7>Limón", Colors.white))
    Lugar_salida = int(input(color("Digite el numero del lugar de Salida: ", Colors.green)))
    if Lugar_salida == 1:
        Lugar_salida = "San Jose"
    elif Lugar_salida == 2:
        Lugar_salida = "Alajuela"
    elif Lugar_salida == 3:
        Lugar_salida = "Heredia"
    elif Lugar_salida == 4:
        Lugar_salida = "Cartago"
    elif Lugar_salida == 5:
        Lugar_salida = "San Carlos"
    elif Lugar_salida == 6:
        Lugar_salida = "Puntarenas"
    elif Lugar_salida == 7:
        Lugar_salida = "Limon"
    else:
        print(color("El lugar no existe", Colors.red))
        BuscarRutas()
    Lugar_Destino = int(input(color("Digite el numero del lugar de Destino ", Colors.green)))
    if Lugar_Destino == 1:
        Lugar_Destino = "San Jose"
    elif Lugar_Destino == 2:
        Lugar_Destino = "Alajuela"
    elif Lugar_Destino == 3:
        Lugar_Destino = "Heredia"
    elif Lugar_Destino == 4:
        Lugar_Destino = "Cartago"
    elif Lugar_Destino == 5:
        Lugar_Destino = "San Carlos"
    elif Lugar_Destino == 6:
        Lugar_Destino = "Puntarenas"
    elif Lugar_Destino == 7:
        Lugar_Destino = "Limon"
    else:
        print(color("El lugar no existe", Colors.red))
        BuscarRutas()

    Fecha_S = str(input(color("Digite la fecha de salida con el siguiente formato 'aaaa-mm-dd': ", Colors.green)))
    try:
        dt.datetime.strptime(Fecha_S, '%Y-%m-%d')
    except ValueError:
        print(color("Formato incorrecto, debe de ser aaaa-mm-dd", Colors.red))
        BuscarRutas()
    ###########################Imprime las Rutas directas################################
    F = ""
    print(color("=== RUTAS DIRECTAS ===", Colors.blue))
    if Lugar_salida != Lugar_Destino:  # imprime las Rutas Directas
        x = 0
        for Ruta in Lista_Rutas:  # Saca cada ruta de la lista
            F = Ruta['Fecha&Hora_Salida'].split()
            c = 0
            if Lugar_salida == Ruta['Origen'] and Lugar_Destino == Ruta['Destino'] and Fecha_S == F[0]:
                for nom in Lista_Terminales:
                    if nom['ID'] == Ruta['ID_Terminal']:
                        for bus in Lista_Unidades:
                            if bus['Placa'] == Ruta['Placa_Unidad']:
                                for asiento in bus['Asientos']:
                                    for espacio in asiento:
                                        if espacio['nombre_color'] == "":
                                            print('Codigo:', Ruta['ID'], '|', 'Lugar de Origen:', Ruta['Origen'], '|',
                                                  'Nombre de Terminal:',
                                                  nom['Nombre_Terminal'], '|', 'Lugar de Destino:', Ruta['Destino'],
                                                  '|',
                                                  ' Fecha y Hora de salida:', Ruta['Fecha&Hora_Salida'], '|',
                                                  ' Fecha y Hora de llegada:', Ruta['Fecha&Hora_Llegada'], '|',
                                                  ' Duración Total:', Ruta['Duracion'], '|', 'Precio Total:',
                                                  Ruta['Precio'])
                                            c += 1
                                            print("")
                                            break
                                        else:
                                            a = 0
                                    if c == 1:
                                        break
                            elif c == 1:
                                break
                            else:
                                a = 0
                    else:
                        a = 1
            # elif x == 2:
            # break
            else:
                a = 1

    else:
        print(color("El lugar de salida no puede ser el mismo que el de destino", Colors.red))

    ###########################Imprime las Rutas indirectas################################

    print(color("=== RUTAS INDIRECTAS ===", Colors.blue))
    for Rutasindirectas in Lista_Rutas:  # Saca cada ruta de la lista
        F = Rutasindirectas['Fecha&Hora_Salida'].split()
        if Lugar_salida == Rutasindirectas['Origen'] or Lugar_Destino == Rutasindirectas['Destino'] and Fecha_S == F[0]:
            Rutas_Temporales.append(Rutasindirectas)
        else:
            a = 2

    Indicador = "NO"
    for Ruta1 in Rutas_Temporales:  # saca la primer ruta
        FechaR1 = Ruta1['Fecha&Hora_Salida'].split()
        for Ruta2 in Rutas_Temporales:  # saca la segunda ruta2 para compararla con la ruta1
            FechaR2 = Ruta2['Fecha&Hora_Salida'].split()
            if Ruta1['Origen'] == Lugar_salida and Ruta1['Destino'] == Ruta2['Origen'] and Ruta2[
                'Destino'] == Lugar_Destino:  #
                for ubica in Lista_Lugares:
                    if Ruta1['Fecha&Hora_Llegada'] < Ruta2['Fecha&Hora_Salida']:
                        if Ruta1['ID_Terminal'] == ubica['Terminal_1']:
                            if FechaR1[0] == FechaR2[0]:
                                for bus in Lista_Unidades:
                                    if bus['Placa'] == Ruta1['Placa_Unidad']:
                                        for asiento in bus['Asientos']:
                                            for espacio in asiento:
                                                if espacio['nombre_color'] == "":
                                                    Indicador = "SI"
                                                    break
                                                else:
                                                    a = 9
                                            break
                                    else:
                                        a = 0
                            else:
                                a = 1  # print("no hay ruta")
                        else:
                            a = 2
                    else:
                        a = 2  # print("no hay ruta 1")

                h1 = Ruta1['Duracion']
                h1Split = h1.split(":")
                h2 = Ruta2['Duracion']
                h2Split = h2.split(":")
                horaUno = dt.timedelta(hours=int(h1Split[0]), minutes=int(h1Split[1]), seconds=int(h1Split[2]))
                horaDos = dt.timedelta(hours=int(h2Split[0]), minutes=int(h2Split[1]), seconds=int(h2Split[2]))
                actual = horaUno + horaDos
                precioTotal = int(Ruta1['Precio']) + int(Ruta2['Precio'])
                if Indicador == "SI":
                    for nom in Lista_Terminales:
                        if nom['ID'] == Ruta1['ID_Terminal']:
                            print('Codigo:', Ruta1['ID'], '|', 'Lugar de Origen:', Ruta1['Origen'], '|',
                                  'Nombre de Terminal:', nom['Nombre_Terminal'], '|',
                                  ' Lugar de Destino:', Ruta1['Destino'], '|', ' Fecha y Hora de salida:',
                                  Ruta1['Fecha&Hora_Salida'], '|', 'Fecha y Hora de llegada:',
                                  Ruta1['Fecha&Hora_Llegada'], '|',
                                  ' Duración Total:', Ruta1['Duracion'], '|', 'Precio Total:', Ruta1['Precio'])
                            print("")
                        else:
                            a = 0
                else:
                    print(color("No hay Rutas directas", Colors.yellow))

                if Indicador == "SI":
                    for ubica2 in Lista_Lugares:
                        if Ruta2['ID_Terminal'] == ubica2['Terminal_1']:
                            for nom in Lista_Terminales:
                                if nom['ID'] == Ruta2['ID_Terminal']:
                                    print('Codigo:', Ruta2['ID'], '|', 'Lugar de Origen:', Ruta2['Origen'], '|',
                                          'Nombre de Terminal:',
                                          nom['Nombre_Terminal'], '|', 'Lugar de Destino:', Ruta2['Destino'], '|',
                                          ' Fecha y Hora de salida:', Ruta2['Fecha&Hora_Salida'], '|',
                                          ' Fecha y Hora de llegada:', Ruta2['Fecha&Hora_Llegada'], '|',
                                          ' Duración Total:', Ruta2['Duracion'], '|', 'Precio Total:', Ruta2['Precio'])
                                    print("")
                                else:
                                    a = 0
                        else:
                            a = 2
                    print(color('Duración total: ', Colors.green), actual)
                    print(color('Precio total: ', Colors.green), precioTotal)
                    print("")
                else:
                    print(color("No hay Rutas Indirectas", Colors.yellow))
            else:  # no hay rutas indirectas
                a = 1

    MenuPasajero()
def comprarBoletos():
    Campos_Temporales = []
    ruta_temporal=[]
    Lista_Unidades = []
    Lista_Rutas = []
    Lista_Historial =[]
    uHistorial = open('Historial.txt', 'r')  # Abre el archivo con los usuarios actuales
    unLeer = open('Unidades.txt', 'r')
    ruLeer = open('Rutas.txt', 'r')

    with uHistorial as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Historial = ast.literal_eval(uHistorial.read())
    uHistorial.close()

    with ruLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Rutas = ast.literal_eval(ruLeer.read())
    ruLeer.close()

    with unLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Unidades = ast.literal_eval(unLeer.read())
    unLeer.close()

    print(color("\n== Bienvenido a Compra de Boletos ==\n", Colors.blue))
    print(color("1> SI | 2> NO", Colors.orange))
    Comprar_Boleto = int(input(color("Desea comprar boletos?",Colors.green)))

    if Comprar_Boleto == 1:
        Comprar_Rutas = int(input(color("Digite el codigo de La Ruta a comprar: ",Colors.green)))
        Cantidad_boletos = int(input(color("Digite cuantos boletos desea comprar:",Colors.green)))
        print(color("\nNo pueden ser mas de 5 :",Colors.red))
        if Cantidad_boletos <= 5:
            a=1
        else:
            print(color("La cantidad de Acompañantes no es permitida",Colors.red))
            comprarBoletos()


        no_hay_espacio="SI"
        cont1=0
        #saca los asientos y los guarda en una lista
        for R in Lista_Rutas:
            if R['ID'] == Comprar_Rutas:
                ruta_temporal.append(R)
                for bus in Lista_Unidades:
                    if bus['Placa'] == R['Placa_Unidad']:
                        for Fila_asientos in bus['Asientos']:
                            for valor in Fila_asientos:
                                if cont1 < Cantidad_boletos:
                                    if valor['nombre']!="*":
                                        if valor['nombre_color'] != '':  # pregunta si nombre_color tiene algún valor, nombre color va a ser el indicante si está ocupado el asiento o no.
                                            #print("\t", valor['nombre_color'], end="")  # imprima el asiento ocupado
                                            a=1
                                        else:
                                            valor['nombre_color']=color(valor['nombre'],Colors.green)
                                            Campos_Temporales.append(valor['nombre'])
                                            cont1 = cont1 + 1
                                    else:
                                        no_hay_espacio="NO"
                                        break
                                else:
                                    break
        print(color("== Sus asientos ==",Colors.orange))
        for c in Campos_Temporales:
            print("\t", color(c,Colors.blue), end="")
        #ocupa el asiento que sigue de los que compraron
        cont2 = 1
        if no_hay_espacio == "SI":
            for R in Lista_Rutas:
                if R['ID'] == Comprar_Rutas:
                    for bus in Lista_Unidades:
                        if bus['Placa'] == R['Placa_Unidad']:
                            for Fila_asientos in bus['Asientos']:
                                for valor in Fila_asientos:
                                    if cont2 <= 1:
                                        if valor['nombre_color'] != '':  # pregunta si nombre_color tiene algún valor, nombre color va a ser el indicante si está ocupado el asiento o no.
                                            #print("\t", valor['nombre_color'], end="")  # imprima el asiento ocupado
                                            a=1
                                        else:
                                            valor['nombre_color']=color(valor['nombre'],Colors.red)
                                            # imprima el asiento desocupado
                                            cont2 = cont2 + 1
                                    else:
                                        break

            #IMPRIME EL BUS PARA QUE EL QUE COMPRA VEA LOS ASIENTOS
            print(color("======>  BUS  <======",Colors.yellow))
            cont = 1
            for R in Lista_Rutas:
                if R['ID'] == Comprar_Rutas:
                    for bus in Lista_Unidades:
                        if bus['Placa'] == R['Placa_Unidad']:
                            for Fila_asientos in bus['Asientos']:
                                for valor in Fila_asientos:
                                    if cont <= int(bus['Capacidad']):
                                        if valor['nombre_color'] != '':  # pregunta si nombre_color tiene algún valor, nombre color va a ser el indicante si está ocupado el asiento o no.
                                            print("\t", valor['nombre_color'], end="")  # imprima el asiento ocupado
                                            cont = cont + 1
                                        else:
                                            print("\t", valor['nombre'], end="")  # imprima el asiento desocupado
                                            cont = cont + 1
                                    elif cont > int(bus['Capacidad']):
                                        valor['nombre'] = "*"
                                        valor['nombre_color_R'] = "*"
                                print("")
            campos=""

            for c in Campos_Temporales:
                if campos == '':
                    campos = c
                else:
                    campos = campos+","+c


            with open('Unidades.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                file.write(json.dumps(Lista_Unidades))

            ############################################ SACA EL PRECIO Y SI HAY QUE HACER DESCUENTO ################################################
            precio_A_pagar=0
            if infoUTemp[2] >= 65:
                for ruta in ruta_temporal:
                    precio_r=ruta['Precio']
                    precio_A_pagar=precio_r*0.5
                    precio_A_pagar=precio_A_pagar*Cantidad_boletos
            else:
                for ruta2 in ruta_temporal:
                    precio_r = ruta2['Precio']
                    precio_A_pagar=precio_r*Cantidad_boletos
            #print(precio_A_pagar)




            ##################### SE SACAN ALGUNOS DATOS PARA EL ARCHIVO HISTORIAL#########################
            Ruta_Origen=""
            Ruta_Destino=""
            Ruta_duracion=""
            for r in ruta_temporal:
                ID_Ruta = r['ID']
                Ruta_Origen = r['Origen']
                Ruta_Destino = r['Destino']
                Ruta_duracion= r['Duracion']

            #################### MANDA EL CORREO###########################

            message='Muchas Gracias,{} por su compra en la ruta {} - {} ,los asientos para su viaje son: {}'.format(infoUTemp[1],Ruta_Origen,Ruta_Destino,campos)
            subject="Compra de Boletos"

            message= 'Subject: {}\n\n{}'.format(subject, message)

            server= smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('pruebaproyectoestebanjose@gmail.com','Proyecto123')

            server.sendmail('pruebaproyectoestebanjose@gmail.com',infoUTemp[3],message)
            server.quit()
            print(color("Compra realizada con exito",Colors.orange))

            ############################## GUARDA LOS DATOS DE LA COMPRA EN HISTORIAL #####################
            Fecha=dt.datetime.now()
            Fecha_sistemastr=str(Fecha.strftime("%Y-%m-%d %H:%M"))

            Datos_a_guardar={'Cedula':infoUTemp[0],'ID_Ruta':ID_Ruta,'Lugar_Salida':Ruta_Origen,'Lugar_LLegada':Ruta_Destino,'Fecha_Compra':Fecha_sistemastr,'Boletos':Cantidad_boletos,
                             'Asientos':campos,'Duracion':Ruta_duracion,'Costo_Total':precio_A_pagar}

            Lista_Historial.append(Datos_a_guardar)

            with open('Historial.txt','w+') as file:  # Actualiza la información del archivo de texto - Unidades
                file.write(json.dumps(Lista_Historial))

        else:
            print(color("* No hay espacios dispanibles *",Colors.red))
        MenuPasajero()


    elif Comprar_Boleto == 2:
        MenuPasajero()
    else:
        print(color("El numero no corresponde a ninguna opcion",Colors.red))
        comprarBoletos()

##################################        REPORTES        ##############################

def reportes(): #Creacion del PDF de Reportes utilizando la libreria ReportLab
    usuarios = {}
    cuentoP = {}
    Lista_Historial =[]
    lineasTexto = []
    uHistorial = open('Historial.txt', 'r')  # Abre el archivo con los usuarios actuales
    uLeer = open('Usuarios.txt', 'r')  # Abre el archivo con los usuarios actuales

    with uHistorial as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        Lista_Historial = ast.literal_eval(uHistorial.read())
    uHistorial.close()

    with uLeer as inf:  # Extrae los datos actuales del archivo de texto y los guarda en un diccionario
        for line in inf:
            usuarios = (eval(line))
        uLeer.close()

    M = 0
    F = 0
    for gen in Lista_Historial:
        if gen["Cedula"] in usuarios:
            if not cuentoP:
                cuentoP = {gen["Cedula"] : 'x'}
                if usuarios[gen["Cedula"]][4] == 'Hombre':
                    M += 1
                else:
                    F += 1
            else:
                if gen["Cedula"] in cuentoP:
                    M = M
                    F = F
                else:
                    cuentoP[gen["Cedula"]] = "x"
                    if usuarios[gen["Cedula"]][4] == 'Hombre':
                        M += 1
                    else:
                        F += 1

    mString = str(M)
    fString = str(F)

    titulo = 'Reportes de Compras de Tiquetes'
    cantidad = "La cantida de mujeres que han comprado tiquetes es de {} y la cantidad de hombres es de {}.".format(fString, mString)
    subtitulo = 'Lista de Compras de: Más Antiguo a Más Actual.'


    for rep in Lista_Historial:
        cedStr = str(rep['Cedula'])
        lugSalidaStr = str(rep["Lugar_Salida"])
        lugDestinoStr = str(rep["Lugar_LLegada"])
        horaCompraStr = str(rep["Fecha_Compra"])
        cantBoletosStr = str(rep["Boletos"])
        asientosStr = str(rep["Asientos"])
        duracionStr = str(rep["Duracion"])
        ctStr = str(rep["Costo_Total"])

        lineasTexto.append("Cedula del Pasajero: {}".format(cedStr))
        lineasTexto.append("Lugar de Salida: {}".format(lugSalidaStr))
        lineasTexto.append("Lugar de Destino: {}".format(lugDestinoStr))
        lineasTexto.append("Fecha y Hora de Compra: {}".format(horaCompraStr))
        lineasTexto.append("Cantidad de Boletos: {}".format(cantBoletosStr))
        lineasTexto.append("Asientos: {}".format(asientosStr))
        lineasTexto.append("Duración en Horas y Minutos: {}".format(duracionStr))
        lineasTexto.append("Costo Total: {}".format(ctStr))
        lineasTexto.append("*****************************************")


    pdf = canvas.Canvas('Reporte.pdf')

    pdf.setTitle('Reporte Actual de Compras')
    pdf.drawString(200, 770, titulo)
    pdf.drawString(40, 670, cantidad)
    pdf.drawString(40, 570, subtitulo)

    text = pdf.beginText(40, 500)
    text.setFont("Courier", 12)
    for line in lineasTexto:
        text.textLine(line)

    pdf.drawText(text)
    pdf.save()

    print(color("\n¡Reporte creado exitosamente!",Colors.orange))
    print(input("Aprete Enter para continuar..."))
    Menu_Administrador()


menuInicio()



