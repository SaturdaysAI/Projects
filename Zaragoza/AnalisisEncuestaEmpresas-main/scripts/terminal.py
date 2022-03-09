"""
Procesamiento de instrucciones.
No se puede grabar o reproducir un fichero que se esté grabando o reproduciendo. Para este control empleamos listaArchivos[]

"""
import re
import os


def esEntero(s):
    """
    Devuelve True si la cadena s representa un entero positivo o negaiivo 

    Parameters
    ----------
    s : string
    Returns
    -------
    Boolean
    """
    # Empleo esEntero() en cuenta de isdigit() porque isdigit() no detecta enteros negativos.
    reg_exp = "[-+]?\d+$"
    return re.match(reg_exp, s) is not None

def es_flotante(variable):
    try:
        float(variable)
        return True
    except:
        return False


anchoPantalla = 100
altoPantalla = 40

def imprimeLineasConMarco(s, ancho=0, margen=4) :
    espacios = margen*" "
    lt = s.split('\n')
    if ancho == 0:
        ancho  = 5 + max( [len(l) for l in lt] )
    if ancho+5 > anchoPantalla:
        ancho = anchoPantalla-5
    for l in lt:
        if l == "<LINEA>":
            print(" +" + (ancho)*"-" + "+")
        else :
            while len(l) > ancho-2*margen:
                print(" |" + espacios + l[:ancho-2*margen] + espacios + "|")
                l = l[(ancho+4) :]
            print(" |" + espacios + l + (ancho-len(l)-2*margen)*" " + espacios + "|")
    

def confirma() :
    """
    Pide confirmación al usuario.
    Returns
    -------
    bool: 
        Si responde 's' (sí) o 'y' (yes), devuelve True,
        si reponde 'n' (no) devuelve False, y el otro caso repite el bucle.
    """
    contador = 0
    while True :
        contador += 1
        resp = input("Confirmar [S/N]: ")
        if resp == "S" or resp == "s" or resp == "Y" or resp == "y" :
            return True
        if resp == "N" or resp == "n" or contador > 6:
            return False

def borrarPantalla(): #Definimos la función estableciendo el nombre que queramos
    print("\033[2J\033[1;1f")
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def preprocesamiento(s) :
    """
    Separa una instrucción en sus parámetros en una lista. Los parámetros deben estar separados por espacios, comas o puntos y comas.
    Los parámetros se devuelven en una lista.
    Si un parámetro representa un entero, en la lista estará como entero.
    Se pueden indicar rangos de valores entre dos números. La lista contendrá todos esos números. Ejemplos:
        "N 1,..,5,7,15,..,11" --> ['N', 1, 2, 3, 4, 5, 7, 15, 14, 13, 12, 11]
        "N 0,-1,..,-5,PEPE" --> ['N', 0, -1, -2, -3, -4, -5, 'PEPE']
    Ejemplo de utilización: ejemploProcesainstruccion(s)
    Parameters
    ----------
    s : string a preprocesar
    Returns
    -------
    l : list
    """
    # 1º Hacemos que los argumentos se separen por espacios, comas y puntos y comas.
    l = re.split(';|,| ', s)
    
    # 2º eliminamos posibles argumentos vacíos.
    n = l.count('')
    for i in range(n):
        l.remove('')
    
    # 3º Si un argumento es una cadena que representa un entero, lo cambia por el entero representado.
    for i, v in enumerate(l):
        if esEntero(v):
            l[i] = int(v)
    
    # 4º Tratamiento de rangos, que se definen como .. entre dos números, dejando espacios o comas entre los números y '..'
    ips = l.count('..')
    while ips > 0:
        ips = l.index('..')
        if type(l[ips-1]) == int and ips < len(l)-1 and type(l[ips+1]) == int:
            ini = l[ips-1]
            fin = l[ips+1]
            l.pop(ips)
            if ini == fin:
                l.pop(ips)
            elif ini < fin - 1:
                for v in range(ini+1, fin):
                    l.insert(ips, v)
                    ips += 1
            elif ini > fin + 1:
                for v in range(ini-1, fin, -1):
                    l.insert(ips, v)
                    ips += 1
        else:
            l.pop(ips)
        ips = l.count('..')
    return l
    

def nuevoArchivo(nombreArchivo):
    """
    Cuando se ejecuta graba <nombre archivo>
    Inicializa el archivo y le pone una cabecera. Si existiera anteriormente, lo borrará.
    Parameters
    ----------
    nombreArchivo : string

    Returns
    -------
    booleand: True o False si tiene éxito o no

    """
    global listaInstrucciones
    global listaArchivosReproduccion 
    global listaArchivosGrabacion
    if listaArchivosReproduccion.count(nombreArchivo) > 0  or listaArchivosGrabacion.count(nombreArchivo) > 0:
        print("ERROR: se intenta grabar un archivo que está en ejecución o grabándose. Recursividad no permitida.")
        return False
    else :
        with open(nombreArchivo, 'w') as f:
            f.writelines("Fichero instrucciones.\n")
        f.close()
        listaArchivosGrabacion.append(nombreArchivo)
        return True
    

def escribeLineaArchivo(nombreArchivo, linea) :
    if os.path.isfile(nombreArchivo) :
        with open(nombreArchivo, 'a') as f:
            f.writelines(linea+"\n")
            f.close()
    else : 
        nuevoArchivo(nombreArchivo)
        escribeLineaArchivo(nombreArchivo, linea)


def procesaArchivo(nombreArchivo) :
    global listaInstrucciones
    global listaArchivosReproduccion 
    global listaArchivosGrabacion
    r = False
    if os.path.isfile(nombreArchivo):
        if listaArchivosReproduccion.count(nombreArchivo) == 0 and listaArchivosGrabacion.count(nombreArchivo) == 0:
            with open(nombreArchivo, 'r') as f:
                l = f.readlines()
                for ind, lin in enumerate(l):
                    if lin[-1:] == '\n':
                        l[ind] = lin[:-1]
                        
                if l[0].find("Fichero instrucciones.") == -1:
                    print("ERROR. El fichero", nombreArchivo, "no es un fichero de instrucciones.")
                else :
                    l.pop(0) # quitamos primera línea
                    listaArchivosReproduccion.append(nombreArchivo)
                    l.append(listaInstrucciones)
                    listaInstrucciones = l
                    r = True
                f.close()
        else:
            print("ERROR: se intenta ejecutar un archivo que está en ejecución o grabándose. Recursividad no permitida.")
    else:
        print("Error, se intenta ejecutar archivo", nombreArchivo, "pero no se ha encontrado.")
    return r


listaInstrucciones = []
listaArchivosReproduccion = []
listaArchivosGrabacion = []

def entradaInstuccion(n, promt) :
    global listaInstrucciones
    global listaArchivosReproduccion 
    global listaArchivosGrabacion
    instruccion = ''
    print()
    while instruccion == '':
        if len(listaInstrucciones) > 0:
            instruccion = listaInstrucciones.pop(0)
            l = preprocesamiento(instruccion)
            if instruccion[0:1] != '#':
                print(promt(n, listaArchivosGrabacion, listaArchivosReproduccion) + instruccion)
            if len(listaInstrucciones) == 0 :
                listaArchivosReproduccion.pop()
            elif type(listaInstrucciones[0]) == list:
                listaInstrucciones = listaInstrucciones[len(listaInstrucciones)-1]
                listaArchivosReproduccion.pop()
            if len(l) == 2 and type(l[0]) == str and (l[0].lower() == "graba" or l[0].lower() == "reproduce"):
                procesaArchivo(l[1])
                instruccion = ''
        else :
            instruccion = input(promt(n, listaArchivosGrabacion, listaArchivosReproduccion))
            l = preprocesamiento(instruccion)
        
            if len(l) == 2 and  type(l[0]) == str  and type(l[1]) == str and str(l[0]).lower() + " " + str(l[1]).lower() == "fin graba" and len(listaArchivosGrabacion) > 0:
                listaArchivosGrabacion.pop()
                instruccion = ''
            else:
                if len(listaArchivosGrabacion) > 0:
                    escribeLineaArchivo(listaArchivosGrabacion[len(listaArchivosGrabacion)-1], instruccion)
                if len(l) == 1  and type(l[0]) == str and l[0].lower() == "cls" :
                    borrarPantalla()
                    instruccion = ''
                elif len(l) == 2  and type(l[0]) == str  and type(l[1]) == str and l[0].lower() == "graba" :
                    nuevoArchivo(l[1])
                    instruccion = ''
                elif len(l) == 2 and  type(l[0]) == str  and type(l[1]) == str and l[0].lower() == "reproduce" :
                    procesaArchivo(l[1])
                    instruccion = ''
        if instruccion[0:1] == '#':
            print("\x1b[1;32m" + instruccion)
            instruccion = ''
        elif len(l) == 1  and type(l[0]) == str and l[0].lower() == "cls" :
            borrarPantalla()
            instruccion = ''
        elif len(l) == 1 and type(l[0]) == str and (l[0] == 'q' or l[0] == 'Q' or l[0].lower() == 'quit' or l[0].lower() == 'exit'):
            print("\n\nSALIMOS DE EJECUCIÓN DE PROGRAMA")
            import sys
            sys.exit()

    print("\x1b[1;37m")    # Color blanco
    return instruccion
    

def terminal(parse, promt):
    comando = ""
    n = 0
    while comando.lower() != 'q':
        comando = entradaInstuccion(n, promt)
        parse(comando)
        n += 1


def promtEjemplo(n, listaArchivosGrabacion, listaArchivosReproduccion) :
    r = "Instrucción"
    if len(listaArchivosGrabacion) > 0: 
        r += '[:> '+ listaArchivosGrabacion[len(listaArchivosGrabacion)-1] + ']'
    if len(listaArchivosReproduccion) > 0: 
        r += '[' + listaArchivosReproduccion[len(listaArchivosReproduccion)-1] + ':>]'
    r  += " <" + str(n) + ">: "
    # El return devuelve cadena que pone colores. Ver https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html
    return "\x1b[1;33m" + r + "\x1b[1;34m"


def ejemploProcesainstruccion(s):
    """
    Un modelo de procesamiento.
    """
    l = preprocesamiento(s)
    print("PROCESAR INSTRUCCIÓN CON ARGUMENTOS:", l)
            
if __name__  == "__main__":
    terminal(ejemploProcesainstruccion, promtEjemplo)


    