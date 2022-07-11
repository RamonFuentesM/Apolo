
from tkinter import *
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
import pickle
import os
import signal
import threading
from tkinter import filedialog

import validators



# ===========================================================================================
# ===========================FUNCIONES PARA USO DE HERRAMIENTAS==============================
# ===========================================================================================

def setData(n_scanner, fils, table, ventana_historial): # Esta funcion es para traer los datos de la tabla almacenados en el archivo
    global num_scanner, filas, tabla, tab2, abrir_historial, num_abrir_button
    abrir_historial={} # Variable para almacenar los botones para ver los reportes
    tab2 = ventana_historial
    tabla = table
    num_scanner = n_scanner
    num_abrir_button = 0.216 # Variable para controlar la posicion de los botones en el historial
    filas = fils 

# Para comprobar y limpiar variables
def comprobarCampos(output_text, output, ventanaParametros, createScanButton, cancelButton, botones):
    
        global abortar, comandos, hosts, scanners
        hosts = []
        scanners = []
        comandos = []
        hosts.clear() # Limpio las variables asegurando que esten vacias
        scanners.clear()
        comandos.clear()
        #flag_norellenado= True # por defecto los campos no estan rellenados
        abortar=False #Inicializo la variable para abortar el comando a false por lo que no aborta el comando mientras no se indique
        
        output_text.configure(state=NORMAL)
        output_text.delete(1.0, END) # Limpio el output
        output_text.configure(state=DISABLED) 

        hilo = threading.Thread(target=lambda: ejecutarComandos(output_text, output, ventanaParametros, createScanButton, cancelButton, botones))
        hilo.start()
        createScanButton.configure(state=DISABLED)
        createScanButton.configure(disabledforeground="white")
        createScanButton.configure(text="Cargando...")

# Para ejecutar comandos
def ejecutarComandos(output_text, output, ventanaParametros, createScanButton, cancelButton, botones):
    try:
        for i in range(len(rellenar_comandos)):
            rellenar_comandos[i]()
        if len(comandos) != 0:
            if not os.path.isdir("reportes/" + "Escaner" + str(num_scanner+1)): # Si la carpeta para guardar los resultados (reportes) no existe
                os.mkdir("reportes/" + "Escaner" + str(num_scanner+1)) # Creo la carpeta 
            for boton in botones:
                boton.configure(state=DISABLED) # Se deshabilitan los botones durante la ejecucion
            output_text.configure(state=NORMAL) 
            for comando in comandos:
                print("Iniciando: " + comando)
                backFunction(ventanaParametros, createScanButton) # Para volver a la pantalla principal tras ejecutar un comando
                output_text.configure(state=NORMAL)  # Estado a normal para poder escribir
                cancelButton.configure(state=NORMAL)
                global p
                com = comando
                if comando.__contains__("dotdotpwn"):
                    os.chdir("Herramientas/dotdotpwn/")
                    os.system("ls")
                p = Popen(com, stdout=PIPE, shell=True, preexec_fn=os.setsid)
                for line in p.stdout:
                    output_text.configure(state=NORMAL)
                    output_text.insert(INSERT, line.rstrip().decode() + "\n")
                    output_text.see(END)
                    output.update_idletasks()
                    output_text.configure(state=DISABLED)
                p.stdout.close()
                p.wait()
                if comando.__contains__("dotdotpwn"):
                    os.chdir("../../")
                #botones[index].configure(background="#34363c")
                if abortar:# Si se pulsa en cancel (la X) se abortan todos los procesos
                    break
            cancelButton.configure(state=DISABLED)
            if not abortar: # Si no se han abortado los comandos, creo la fila nueva del historial y la almaceno
                crearFila()
            for boton in botones: # Se habilitan los botones tras la ejecucion
                boton.configure(state=NORMAL)
            
            createScanButton.configure(disabledforeground="lightgrey") # Color por defecto
            createScanButton.configure(text="Crear escáner")
        else:
            output_text.configure(state=NORMAL)
            output_text.insert(INSERT, "Falta no has rellenado ningun parametro" + "\n")
            output_text.configure(state=DISABLED)    
    except: # Informo de situaciones adversas
         output_text.configure(state=NORMAL)
         output_text.insert(INSERT, "Ocurrio un fallo durante la ejecucion" + "\n")
         output_text.configure(state=DISABLED)


# Para cancelar los escáneres
def cancelProcess(output_text):
    # Saco el pid y termino el proceso
    try:
        global abortar, num_scanner #Aborto todos los procesos
        abortar=True
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        if os.path.isdir("reportes/Escaner" + str(num_scanner+1)): # Borro los archivos creados ya que los escaneres se quedaron a medias
            os.system("rm -rf " + "reportes/Escaner" + str(num_scanner+1))
        output_text.configure(state=NORMAL)
        output_text.insert(INSERT, "\nEl escaner ha sido cancelado") # Informo de que el escaner ha sido cancelado
        output_text.configure(state=DISABLED)
    except: # Informo de situaciones adversas
        output_text.configure(state=NORMAL) 
        output_text.insert(INSERT, "\nOcurrio un error durante la cancelacion de los procesos")
        output_text.configure(state=DISABLED)

# Esta funcion es para volver a la pantalla principal de la herramienta
def backFunction(ventanaParametros, createScanButton):
    ventanaParametros.pack_forget()  # Para quitar el frame de los parametros
    createScanButton.configure(state=DISABLED)
    
# Esta funcion es para echar una pagina atras durante la recopilacion de los parametros
def backPageFunction(ventanaParametros, next, launchScanButt, backButton, backPageButton, tool_parameters):
    global numPagina
    numPagina = numPagina-1
    if numPagina != 1:  # Si estoy en todas menos en la primera pagina
        quitarParametros(ventanaParametros, next, launchScanButt, backButton, backPageButton)
        tool_parameters[numPagina]()  # Spawnear parametros
    else:
        quitarParametros(ventanaParametros, next, launchScanButt, backButton, backPageButton)
        tool_parameters[numPagina]()
        backPageButton.configure(state=DISABLED)
    if numPagina == len(tool_parameters)-1:
        launchScanButt.configure(state=DISABLED)
        next.configure(state=NORMAL)
    
# Esta funcion es para echar una pagina adelante durante la recopilacion de los parametros
def pasarPagina(ventanaParametros, next, launchScanButt, backButton, backPageButton, tool_parameters):
    global numPagina
    numPagina = numPagina+1
    backPageButton.configure(state=NORMAL)
    if numPagina < len(tool_parameters):  # Si estoy en todas menos en la primera pagina
        quitarParametros(ventanaParametros, next, launchScanButt, backButton, backPageButton)
        tool_parameters[numPagina]()  # Spawnear parametros
    else:  # Si estoy en la ultima pagina
        quitarParametros(ventanaParametros, next, launchScanButt, backButton, backPageButton)
        next.configure(state=DISABLED)
        tool_parameters[numPagina]()
        launchScanButt.configure(state=NORMAL)
    if numPagina == 1:
        backPageButton.configure(state=NORMAL)
    

# Funcion para quitar los parametros de la tool en concreto
def quitarParametros(ventanaParametros, next, launchScanButt, backButton, backPageButton):
    list = ventanaParametros.place_slaves()
    for w in list:
        if w != next and w != launchScanButt and w != backButton and w != backPageButton: # Retiro todo menos los botones principales de la ventana
            w.place_forget()


def spawnParameters(tab1, botones, valores, output, output_text, createScanButton, cancelButton):
    # Si alguno esta seleccionado funciona, si no no
    global numPagina, rellenar_comandos
    rellenar_comandos={} #Variable para rellenar los comandos de cada herramienta usada
    numPagina = 1 #Comenzamos en la pagina 1
    ventanaParametros = Frame(tab1, height=1550, bg='#34363c')
    tool_parameters = checkTool(valores, ventanaParametros) # Miro las tools que estan seleccionadas
    
    launchScanButt = Button(ventanaParametros, text="Lanzar escáner", highlightthickness=0, font=(
        "QuickSand Medium", 15), bg="#20bebe", fg="white", command=lambda: comprobarCampos(output_text, output, ventanaParametros, createScanButton, cancelButton, botones))
    backPageButton = Button(ventanaParametros, text="<", highlightthickness=0, font=(
        "QuickSand Medium",  15), bg="#17BFE8", fg="white", command=lambda: backPageFunction(ventanaParametros, next, launchScanButt, backButton, backPageButton, tool_parameters))
    next = Button(ventanaParametros, text=">", highlightthickness=0, font=("QuickSand Medium", 15), bg="#17BFE8", fg="white",
                  command=lambda: pasarPagina(ventanaParametros, next, launchScanButt, backButton, backPageButton, tool_parameters))
    backButton = Button(ventanaParametros, text="Atrás", bg="#A8AEAB", fg="white", highlightthickness=0, font=(
        "QuickSand Medium",  15), command=lambda: backFunction(ventanaParametros, createScanButton))
    backButton.place(relx=0.045, rely=0.08, anchor="center")
    #quitarParametros(ventanaParametros, next, launchScanButt, backButton, backPageButton)
    tool_parameters[numPagina]()
    if len(tool_parameters) > 1:
        next.place(relx=.6, rely=0.9, anchor=CENTER)
        backPageButton.configure(state=DISABLED)
        backPageButton.place(relx=0.4, rely=0.9, anchor=CENTER)
        launchScanButt.place(relx=.5, rely=0.9, anchor=CENTER)
        launchScanButt.configure(state=DISABLED)
    else:
        launchScanButt.place(relx=.5, rely=0.9, anchor=CENTER)
    # Para añadir el frame de los parametros
    ventanaParametros.pack(fill=X)

def quitarHttps(text): # Funcion para quitar https y http
    text= text.replace("https://www." , "")
    text= text.replace("http://www." , "")
    text= text.replace("http://" , "")
    text= text.replace("https://" , "")
    text= text.replace("/", "")
    return text

#def webIsUP(url):
#    respuesta = os.system("ping -c 1 " + url)
#    if respuesta:
#        return False # La web no existe o esta caida
#    else:
#        return True # La web existe

#def validarURL(url):
#        if validators.url(url) and webIsUP(quitarHttps(url)):    
#            print(True) 
#        else:
#            print(False)

def existeHost(objetivos):
    for val in objetivos:
        if not hosts.__contains__(val):
            hosts.append(val)

def browseFile(entry):
    filename = filedialog.askopenfilename(filetypes=(("txt files","*.txt"),("All files","*.*")))
    if filename: # Si el usuario ha seleccionado un nuevo archivo, entonces:
        entry.configure(state=NORMAL)
        entry.delete(0, END) # Limpio la entrada    
        entry.insert(END, filename) # Inserto la nueva direccion
        entry.configure(state=DISABLED)

def browseDir(entry):
    directory = filedialog.askdirectory()
    if directory: # Si el usuario ha seleccionado un nuevo archivo, entonces:
        entry.configure(state=NORMAL)
        entry.delete(0, END) # Limpio la entrada    
        entry.insert(END, directory) # Inserto la nueva direccion
        entry.configure(state=DISABLED)

def switchEscaneres(numero, boton, escaneres):
    if escaneres[numero]:
        escaneres[numero] = 0
        boton.configure(highlightthickness=0)
    else:
        escaneres[numero] = 1
        boton.configure(highlightbackground="#25ff00", highlightthickness=1)

# BROKEN ACCESS CONTROL 5
## CSRF
## Path trasversal
def brokenAccess():
    #print("Broken access control")
    titulo_BAC.place(relx=.5, rely=0.15, anchor=CENTER)
    CSRF_label.place(relx=0.23, rely=0.3)
    objetivo_CSRF.place(relx=0.08, rely=0.5)
    objetivo_entry_CSRF.place(relx=0.165, rely=0.5)
    profundidad_CSRF.place(relx=0.046, rely=0.65)
    profundidad_entry_CSRF.place(relx=0.165, rely=0.65)
    path_trasversal_label.place(relx=0.68, rely=0.3)
    objetivo_Path.place(relx=0.58, rely=0.5)
    objetivo_entry_Path.place(relx=0.665, rely=0.5)
    url_Path.place(relx=0.535, rely=0.65)
    url_entry_Path.place(relx=0.665, rely=0.65)

def BACCommands():
    objetivos= []
    global comandos, hosts, scanners

    if objetivo_entry_CSRF.get() !="":
        comandos.append("python3 Herramientas/Bolt/bolt.py -u " + objetivo_entry_CSRF.get() + " -l " + str(profundidad_entry_CSRF.get()) + " | tee reportes/Escaner" + str(num_scanner+1) + "/CSRF_BAC.txt")
        objetivos.append(quitarHttps(objetivo_entry_CSRF.get()))
    else:     
        print("Faltan campos en CSRF")
    if objetivo_entry_Path.get() != "":
        comandos.append('perl dotdotpwn.pl -m http-url -h ' + objetivo_entry_Path.get() + ' -u ' + url_entry_Path.get() + 'TRAVERSAL -k "root" -b -r reportes/Escaner' + str(num_scanner+1) + '/PathTrasversal_BAC.txt')
        objetivos.append(quitarHttps(objetivo_entry_Path.get()))
        # os.chdir("../../")
    else:
        print("Faltan campos en Path Trasversal")

    existeHost(objetivos)
    scanners.append("BAC")
        

# CRYPTOGRAPHIC FAILURES 4
## TLS/SSL
## HEADERS

def cryptoFailures():
    #print("Crytographic failures")
    titulo_cripto.place(relx=.5, rely=0.15, anchor=CENTER)
    objetivo_cryto.place(relx=0.33, rely=0.6, anchor=CENTER)
    objetivo_entry_cryto.place(relx=0.5, rely=0.6, anchor=CENTER)
    sslButton.place(relx=0.425, rely=0.4, anchor=CENTER) 
    headersButton.place(relx=0.575, rely=0.4, anchor=CENTER)


def cryptoCommands():
    global comandos, hosts, scanners
    if objetivo_entry_cryto.get() != "" and (escaneres_crypto[0] or escaneres_crypto[1]):
        if escaneres_crypto[0]:
            comandos.append("bash Herramientas/testssl.sh/testssl.sh --vulnerable --protocols " + objetivo_entry_cryto.get() + " | tee reportes/Escaner" + str(num_scanner+1) + "/TLS_SSL_CryptoFailures.txt")
        if escaneres_crypto[1]:
            comandos.append("python3 Herramientas/shcheck/shcheck.py -k " + objetivo_entry_cryto.get() + " | tee reportes/Escaner" + str(num_scanner+1) + "/Headers_CryptoFailures.txt")
        
        objetivos=[quitarHttps(objetivo_entry_cryto.get())]
        existeHost(objetivos)
        scanners.append("Crypt.Failures")
    else:
        print("Faltan campos en Criptographic failures")


# IDENTIFICATION AND AUTENTICATION FAILURES
## BRUTEFORCE

# Tanto esta como la funcion de la contraseña (passToWordlist) estan hechas para funcionar como un checkbutton
def userToWordlist(): 
    global user_wordlist # Esta variable indica si el usuario elige introducir una wordlist o un solo parametro
    if user_wordlist==0: # Usa una wordlist
        user_entry_idAutFailures.delete(0, END)
        user_entry_idAutFailures.configure(state=DISABLED) # Deshabilito la casilla para que los datos se introduzcan mediante el boton de browse
        user_wordlistB.configure(text="Lista de usuarios") # Indico que esta usando una wordlist
        user_browse.place(relx=0.68, rely=0.6, anchor=CENTER) 
        user_wordlist=1 # La siguiente vez que el usuario pulse, quitara la wordlist y usara un usuario
    else:
        user_entry_idAutFailures.configure(state=NORMAL) # Deshabilito la casilla para que los datos se introduzcan mediante el boton de browse
        user_wordlistB.configure(text="Usuario")
        user_browse.place_forget()
        user_entry_idAutFailures.delete(0, END) # Al cambiar del uso de wordlist a usuario, borro la posible dirección introducida
        user_wordlist=0

def passToWordlist(): 
    global pass_wordlist
    if pass_wordlist==0:
        pass_browse.place(relx=0.68, rely=0.73, anchor=CENTER) 
        pass_entry_idAutFailures.configure(state=DISABLED) # Deshabilito la casilla para que los datos se introduzcan mediante el boton de browse
        pass_wordlistB.configure(text="Lista de contraseñas")
        pass_entry_idAutFailures.delete(0, END)
        pass_wordlist=1
    else:
        pass_entry_idAutFailures.configure(state=NORMAL) # Deshabilito la casilla para que los datos se introduzcan mediante el boton de browse
        pass_wordlistB.configure(text="Contraseña")
        pass_browse.place_forget()
        pass_entry_idAutFailures.delete(0, END) # Al cambiar del uso de wordlist a contraseña, borro la posible dirección introducida
        pass_wordlist=0


def idAutFailures():
    #print("Identification and autentication failures")
    titulo_idAutFailures.place(relx=.5, rely=0.15, anchor=CENTER)
    
    host_idAutFailures.place(relx=0.365, rely=0.34, anchor="e")
    host_entry_idAutFailures.place(relx=0.5, rely=0.34, anchor=CENTER)
    
    #ejemplo_label.place(relx=0.82, rely=0.47, anchor=CENTER)
    request_idAutFailures.place(relx=0.365, rely=0.47, anchor="e")
    request_entry_idAutFailures.place(relx=0.5, rely=0.47, anchor=CENTER)

    user_wordlistB.place(relx=0.365, rely=0.6, anchor="e")
    user_entry_idAutFailures.place(relx=0.5, rely=0.6, anchor=CENTER)

    pass_wordlistB.place(relx=0.365, rely=0.73, anchor="e")
    pass_entry_idAutFailures.place(relx=0.5, rely=0.73, anchor=CENTER)

def idAutFailuresCommands():
    global user_wordlist, pass_wordlist
    print("Comandos Id Aut Fail")
    global comandos, hosts, scanners
    comand = "hydra "
    if host_entry_idAutFailures.get() !="" and user_entry_idAutFailures.get() != "" and pass_entry_idAutFailures.get() != "" and request_entry_idAutFailures.get() != "": # Si algun campo esta vacio
        
        if user_wordlist==0: # Es un usuario solo por lo tanto uso -l
            print("Usuario")
            comand = comand + "-l " + user_entry_idAutFailures.get() #hydra -l <username>
        else: # Es una wordlist de usuarios por lo tanto uso -L
            print("Lista de usuarios")
            comand = comand + "-L " + user_entry_idAutFailures.get() #hydra -L <username>

        if pass_wordlist==0: # Es una contraseña solo por lo tanto uso -p
            print("Contraseña")
            comand = comand + " -p " + pass_entry_idAutFailures.get() + " " #hydra -l <username> -p <wordlist> 
        else: # Es una lista de contraseñas por lo tanto uso -P
            print("Lista de contraseñas")
            comand = comand + " -P " + pass_entry_idAutFailures.get() + " " #hydra -l <username> -P <wordlist> 
        
        comand = comand + quitarHttps(host_entry_idAutFailures.get()) + " http-post-form " # Añado el host: hydra -l <username> -P <wordlist> <host> http-post-form 
        comand = comand + request_entry_idAutFailures.get() + " -V" # Añado el request: hydra -l <username> -P <wordlist> <host> http-post-form <request> -V
        comand = comand + " | tee reportes/Escaner" + str(num_scanner+1) + "/FuerzaBruta_idAutFailuresCommands.txt" # Añado el reporte
        #print(comand)
        comandos.append(comand)

        objetivos=[quitarHttps(host_entry_idAutFailures.get())]
        existeHost(objetivos)
        scanners.append("Id.Aut.Failures")

    else:
        print("Faltan campos en Criptographic failures")
    

# SECURITY MISCONFIGURATION

def secMisconfig():
    #print("Security Misconfiguration")
    titulo_misc.place(relx=.5, rely=0.15, anchor=CENTER)
    objetivo_misc.place(relx=0.33, rely=0.5, anchor=CENTER)
    objetivo_entry_misc.place(relx=0.5, rely=0.5, anchor=CENTER)

def secMisconfigCommands():
    print("Comandos Sec Misc")
    global comandos, hosts, scanners
    if objetivo_entry_misc.get() != "":
        comandos.append("lighthouse " + objetivo_entry_misc.get() + " --only-categories=best-practices --output-path=reportes/Escaner" + str(num_scanner+1) + "/reporte_Sec_Misconfig.html")
        objetivos=[quitarHttps(objetivo_entry_misc.get())]
        existeHost(objetivos)
        scanners.append("Sec.Misconf")
    else:
        print("Faltan campos en Security Misconfiguration")


# VULNERABLE AND OUTDATED COMPONENTS 2

def vulnComp():
    #print("Vulnerable and outdated")
    titulo_comp.place(relx=.5, rely=0.15, anchor=CENTER)
    objetivo_comp.place(relx=0.29, rely=0.5, anchor=CENTER)
    objetivo_entry_comp.place(relx=0.5, rely=0.5, anchor=CENTER)
    proyect_browse.place(relx=0.68, rely=0.5, anchor=CENTER)


def compCommands():
    #global flag_norellenado
    # flag_norellenado vale para determinar si alguno de los campos de las herramientas escogidas no ha sido rellenado
    if objetivo_entry_comp.get() != "":
        global comandos, hosts, scanners
        comandos.append("./Herramientas/dependency-check/bin/dependency-check.sh --scan " + objetivo_entry_comp.get() + " -o reportes/Escaner" + str(num_scanner+1))
        #flag_norellenado = False
        hosts.append("-")
        scanners.append("Out.Components") 
    else:               #Si el parametro ha sido rellenado, configuro los comandos
        print("Faltan campos en Vulnerable and Outdated Components")


# INFORMATION GATHERING 

def infoGathering():
    #print("Information gathering")
    relxIncrement= 0.15
    relx_var= 0.35 # Para colocar los botones más rapido
    titulo_info.place(relx=.5, rely=0.15, anchor=CENTER)
    nmapButton.place(relx=relx_var, rely=0.4, anchor=CENTER) 
    relx_var+=relxIncrement
    whatwebButton.place(relx=0.5, rely=0.4, anchor=CENTER)
    relx_var+=relxIncrement 
    theHarvesterButton.place(relx=relx_var, rely=0.4, anchor=CENTER) 
    objetivo_info.place(relx=0.33, rely=0.6, anchor=CENTER)
    objetivo_entry_info.place(relx=0.5, rely=0.6, anchor=CENTER)

def infoCommands():
    #global flag_norellenado
    if objetivo_entry_info.get() != "":
        global comandos, hosts, scanners
        if escaneres_infg[0]:
            comandos.append("nmap " + quitarHttps(objetivo_entry_info.get()) + " -v | tee reportes/Escaner" + str(num_scanner+1) + "/nmap_InformationGathering.txt")
        if escaneres_infg[1]:
            comandos.append("whatweb " + objetivo_entry_info.get() + " -v | tee reportes/Escaner" + str(num_scanner+1) + "/whatweb_InformationGathering.txt")
        if escaneres_infg[2]:
            comandos.append("theHarvester -d " + quitarHttps(objetivo_entry_info.get()) + " -b google,linkedin,twitter,yahoo,duckduckgo,bing | tee reportes/Escaner" + str(num_scanner+1) + "/TheHarvester_InformationGathering.txt")
        if escaneres_infg[0] or escaneres_infg[1] or escaneres_infg[2] or escaneres_infg[3]:
            objetivos=[quitarHttps(objetivo_entry_info.get())]
            existeHost(objetivos)
            scanners.append("Info.Gather") 
    else:               #Si el parametro ha sido rellenado, configuro los comandos
        print("Faltan campos en Information Gathering")

        
# COMPROBAR EL BOTON/ES ACTIVADOS

def checkTool(tools_activadas, ventanaParametros):
    tool_parameters = {}
    for index, valor in enumerate(tools_activadas):
        if valor == 0:  # Meto la herramienta que esta seleccionada en un diccionario junto con su numero de pagina por clave
            match index:
                case 0:
                    tool_parameters[len(tool_parameters)+1] = brokenAccess #Es la longitud del diccionario +1 porque cada pagina la identifico a partir del 1
                    rellenar_comandos[len(rellenar_comandos)] = BACCommands
                    global CSRF_label,objetivo_CSRF, objetivo_entry_CSRF, profundidad_CSRF, profundidad_entry_CSRF, titulo_BAC, path_trasversal_label, objetivo_Path, objetivo_entry_Path, url_Path, url_entry_Path # Por que creo aqui los parametros? Para que en la funcion se coloque y no se creen varias veces
                    titulo_BAC = Label(ventanaParametros, text="BROKEN ACCESS CONTROL", background="#34363c", fg="white", font=("Quicksand medium", 30), anchor=CENTER)
                    CSRF_label = Label(ventanaParametros, text="CSRF", font=("Quicksand medium", 18), background="#34363c", fg="white") 
                    objetivo_CSRF = Label(ventanaParametros, text="Objetivo", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    objetivo_entry_CSRF = Entry(ventanaParametros, width=20, font=("Calibri", 15))
                    profundidad_CSRF = Label(ventanaParametros, text="Profundidad", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    profundidad_entry_CSRF= Spinbox(ventanaParametros, from_ = 1, to = 4, increment = 1, font=("Quicksand medium", 15), width=2)
                    path_trasversal_label = Label(ventanaParametros, text="Path trasversal", font=("Quicksand medium", 18), background="#34363c", fg="white") 
                    objetivo_Path = Label(ventanaParametros, text="Objetivo", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    objetivo_entry_Path = Entry(ventanaParametros, width=20, font=("Calibri", 15))
                    url_Path = Label(ventanaParametros, text="URL a testear", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    url_entry_Path = Entry(ventanaParametros, width=20, font=("Calibri", 15))

                case 1:
                    tool_parameters[len(tool_parameters)+1] = cryptoFailures 
                    rellenar_comandos[len(rellenar_comandos)] = cryptoCommands
                    global escaneres_crypto
                    escaneres_crypto = [0,0]
                    global sslButton, headersButton, objetivo_cryto, objetivo_entry_cryto, titulo_cripto # Por que creo aqui los parametros? Para que en la funcion se coloque y no se creen varias veces
                    titulo_cripto = Label(ventanaParametros, text="CRYPTOGRAPHIC FAILURES", background="#34363c", fg="white", font=("Quicksand medium", 30), anchor=CENTER)
                    sslButton = Button(ventanaParametros, font=("Quicksand medium", 15), text="testssl", highlightthickness=0, fg='white', background='#34363c', command= lambda: switchEscaneres(0, sslButton, escaneres_crypto))
                    sslButton.configure(width=10)
                    headersButton = Button(ventanaParametros, font=("Quicksand medium", 15), text="shcheck", highlightthickness=0, fg='white', background='#34363c', command= lambda: switchEscaneres(1, headersButton, escaneres_crypto))                    
                    headersButton.configure(width=10)                    
                    
                    objetivo_cryto = Label(ventanaParametros, text="Objetivo", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    objetivo_entry_cryto = Entry(ventanaParametros, width=20, font=("Calibri", 15))

                case 2:
                    tool_parameters[len(tool_parameters)+1] = idAutFailures
                    rellenar_comandos[len(rellenar_comandos)] = idAutFailuresCommands
                    global user_wordlistB, pass_wordlistB, host_idAutFailures, host_entry_idAutFailures, user_browse, pass_browse, user_entry_idAutFailures, titulo_idAutFailures, pass_entry_idAutFailures, request_idAutFailures, request_entry_idAutFailures # Por que creo aqui los parametros? Para que en la funcion se coloque y no se creen varias veces
                    global user_wordlist, pass_wordlist
                    user_wordlist=0
                    pass_wordlist=0
                    titulo_idAutFailures = Label(ventanaParametros, text="IDENTIFICATION AND AUTHENTICATION FAILURES", background="#34363c", fg="white", font=("Quicksand medium", 30), anchor=CENTER)
                    user_wordlistB = Button(ventanaParametros, font=("Quicksand medium", 15), text="Usuario", highlightthickness=0, fg='white', background='#34363c', command= userToWordlist)
                    pass_wordlistB = Button(ventanaParametros, font=("Quicksand medium", 15), text="Contraseña", highlightthickness=0, fg='white', background='#34363c', command= passToWordlist)
                    host_idAutFailures = Label(ventanaParametros, text="Host", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    host_entry_idAutFailures = Entry(ventanaParametros, width=20, font=("Calibri", 15))
                    request_idAutFailures = Label(ventanaParametros, text="Request body", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    request_entry_idAutFailures = Entry(ventanaParametros, width=20, font=("Calibri", 15))
                    user_entry_idAutFailures = Entry(ventanaParametros, width=20, font=("Calibri", 15))                    
                    pass_entry_idAutFailures = Entry(ventanaParametros, width=20, font=("Calibri", 15))
                    user_browse = Button(ventanaParametros, font=("Quicksand medium", 15), text="Browse", highlightthickness=0, fg='white', background='#34363c', command= lambda: browseFile(user_entry_idAutFailures))
                    pass_browse = Button(ventanaParametros, font=("Quicksand medium", 15), text="Browse", highlightthickness=0, fg='white', background='#34363c', command= lambda: browseFile(pass_entry_idAutFailures))
                    
                case 3:
                    tool_parameters[len(tool_parameters)+1] = secMisconfig
                    rellenar_comandos[len(rellenar_comandos)] = secMisconfigCommands
                    global objetivo_misc, objetivo_entry_misc, titulo_misc # Por que creo aqui los parametros? Para que en la funcion se coloque y no se creen varias veces
                    titulo_misc = Label(ventanaParametros, text="SECURITY MISCONFIGURATION", background="#34363c", fg="white", font=("Quicksand medium", 30), anchor=CENTER)
                    objetivo_misc = Label(ventanaParametros, text="Objetivo", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    objetivo_entry_misc = Entry(ventanaParametros, width=20, font=("Calibri", 15))

                case 4:
                    tool_parameters[len(tool_parameters)+1] = vulnComp
                    rellenar_comandos[len(rellenar_comandos)] = compCommands
                    global proyect_browse, objetivo_comp, objetivo_entry_comp, titulo_comp # Por que creo aqui los parametros? Para que en la funcion se coloque y no se creen varias veces
                    titulo_comp = Label(ventanaParametros, text="VULNERABLE AND OUTDATED COMPONENTS", background="#34363c", fg="white", font=("Quicksand medium", 30), anchor=CENTER)
                    objetivo_comp = Label(ventanaParametros, text="Ruta del proyecto", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    objetivo_entry_comp = Entry(ventanaParametros, width=20, font=("Calibri", 15))
                    objetivo_entry_comp.configure(state=DISABLED)
                    proyect_browse = Button(ventanaParametros, font=("Quicksand medium", 15), text="Browse", highlightthickness=0, fg='white', background='#34363c', command= lambda : browseDir(objetivo_entry_comp))                    

                case 5:
                    tool_parameters[len(tool_parameters)+1] = infoGathering
                    rellenar_comandos[len(rellenar_comandos)] = infoCommands
                    global escaneres_infg
                    escaneres_infg = [0,0,0]
                    global nmapButton, whatwebButton, theHarvesterButton, objetivo_info, objetivo_entry_info, titulo_info # Por que creo aqui los parametros? Para que en la funcion se coloque y no se creen varias veces
                    titulo_info = Label(ventanaParametros, text="INFORMATION GATHERING", background="#34363c", fg="white", font=("Quicksand medium", 30), anchor=CENTER)
                    nmapButton = Button(ventanaParametros, font=("Quicksand medium", 15), text="Nmap", highlightthickness=0, fg='white', background='#34363c', command= lambda: switchEscaneres(0, nmapButton, escaneres_infg))
                    nmapButton.configure(width=10)
                    whatwebButton = Button(ventanaParametros, font=("Quicksand medium", 15), text="Whatweb", highlightthickness=0, fg='white', background='#34363c', command= lambda: switchEscaneres(1, whatwebButton, escaneres_infg))                    
                    whatwebButton.configure(width=10)
                    theHarvesterButton = Button(ventanaParametros, font=("Quicksand medium", 15), text="theHarvester", highlightthickness=0, fg='white', background='#34363c', command= lambda: switchEscaneres(2, theHarvesterButton, escaneres_infg))                    
                    theHarvesterButton.configure(width=10)
                    objetivo_info = Label(ventanaParametros, text="Objetivo", font=("Quicksand medium", 15), background="#34363c", fg="white") 
                    objetivo_entry_info = Entry(ventanaParametros, width=20, font=("Calibri", 15))
                    
    return tool_parameters

# ======================================================================
# ==============================TABLAS==================================
# ======================================================================

# Obtiene los valores de la fila seleccionada
def findRow():  # Obtiene la fila de la tabla en forma de lista
    tool_parameters = tabla.item(tabla.focus())
    return tool_parameters["values"]

# Actualiza la posicion de los botones de la taba
def actualizarTabla():
    global num_abrir_button
    num_abrir_button = 0.2167
    for fila in filas: # Borro todos los botones
        boton=abrir_historial[fila[0]]
        boton.place_forget()
    for fila in filas: # Meto los botones con su nueva posición
        boton=abrir_historial[fila[0]]
        boton.place(relh=0.035, relw=0.094, relx=0.04, rely=num_abrir_button)
        num_abrir_button=num_abrir_button+0.0335 

# Borra los valores de la fila seleccionada
def deleteRow():
    row=findRow()
    if len(row)!=0:
        selected_item=tabla.selection()
        tabla.delete(selected_item)
        filas.remove(row)
        datos=[num_scanner, filas]
        almacenarDatos(datos)
        path="reportes/" + row[0]
        if os.path.isdir(path):
            os.system("rm -rf " + path)
        actualizarTabla()
        boton = abrir_historial[row[0]]
        boton.place_forget()
        abrir_historial.pop(row[0])
        
# Hace un cat a todo el directorio
def catDirectiorio(directorio):
    directorio= "reportes/"+ directorio
    hay_txt=False
    hay_html=False

    for i in os.listdir(directorio): # Comprueba si hay archivos html y txt para abrirlos
        if i.endswith('.txt'):
                hay_txt=True
        if i.endswith('.html'):
                hay_html=True
    if hay_txt: # Si hay archivos txt creo un comando que hace un cat de todos los archivos en una nueva terminal
        var= "gnome-terminal -e "
        var = var + '"bash -c '
        var = var + "'cat "+ directorio + "*.txt;$SHELL'"
        var = var + '"'
        os.system(var)
    if hay_html: # Su hay un archivo html los abro en una ventana de firefox 
        os.system("nohup firefox "+ directorio + "*.html &")
    

# Inserta una fila en la tabla
def insertTabla(fila):
    global num_abrir_button, abrir_historial
    boton = Button(tab2, font=("Quicksand ", 13), text=fila[0], borderwidth=0, highlightthickness=0, fg='black', background='#f9f9f9', command= lambda directorio = fila[0] + "/" : catDirectiorio(directorio))
    abrir_historial[fila[0]] = boton
    boton.place(relh=0.035, relw=0.094, relx=0.04, rely=num_abrir_button)   

    num_abrir_button=num_abrir_button+0.0335
    
    tabla.insert('', 'end', text="5", values=(fila[0], fila[1], fila[2], fila[3]))

# Almacena los datos en un archivo (datos.pkl)
def almacenarDatos(datos):
    with open('historial/datos.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(datos, f)

# Obtiene la carpeta donde estan situado el escaner escogido
def inspeccionarReportes():
    try:
        fila=findRow()
        os.system('xdg-open "%s"' % "reportes/" + fila[0])
    except:
        print("Error al buscar la carpeta")

def crearFila():
    global num_scanner
    num_scanner = num_scanner + 1
    hosts_string = ", ".join(str(x) for x in hosts)
    escaneres_string = ", ".join(str(x) for x in scanners)
    now = datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    nueva_fila = ["Escaner"+ str(num_scanner), hosts_string, fecha, escaneres_string]
    filas.append(nueva_fila)
    datos = [num_scanner, filas]
    almacenarDatos(datos)
    insertTabla(nueva_fila)

