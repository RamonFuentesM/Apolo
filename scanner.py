import os
from subprocess import Popen, PIPE, STDOUT
from tkinter import *                    
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import font
from scannerFunctions import *
from tkinter import messagebox


  
    
# https://www.w3schools.com/colors/colors_hexadecimal.asp -> Para los colores
# https://coderslegacy.com/python/list-of-tkinter-widgets/ -> Lista de widgets
# https://www.activestate.com/resources/quick-reads/how-to-position-widgets-in-tkinter/


# =============================================================================================
# =======================================RAIZ:=================================================
# =============================================================================================



raiz=Tk()

width, height = 1152, 720

width_sc = raiz.winfo_screenwidth()
height_sc = raiz.winfo_screenheight()

x = (width_sc/2) - (width/2)
y = (height_sc/2) - (height/2)

raiz.geometry('%dx%d+%d+%d' % (width, height, x, y)) ## Para spawnear la ventana en el medio de la pantalla

raiz.config(bg="#01252a")
raiz.resizable(False,False)

icon = PhotoImage(file = 'Imagenes/Icon.png')
raiz.iconphoto(False, icon) 
raiz.title("Apolo")

tabs = ttk.Notebook(raiz) 

styleTabs = ttk.Style()

styleTabs.theme_create( "styleTabs", settings={
        "Treeview":{"configure":  {"background": "white", "font":('Quicksand',13), "rowheight": 23},
                                    "map":       {"background": [("selected", "lightblue")] }},
        "Treeview.Heading":{"configure": {"background": "lightgrey", "fg":"white", "font":('Quicksand',15)}},
        "TNotebook": {"configure": {"background": "#1e1f21"} }, #Fondo de las tabs
        "TNotebook.Tab": {
            "configure": {"background": "#1e1f21", "padding": [5, 2], "font": ("Quicksand",15), "foreground":'white' }, #La tab cuando no es seleccionada
            "map":       {"background": [("selected", "#34363c")] } } } ) # La tab cuando esta seleccionada


styleTabs.theme_use('styleTabs')


tab1 = Frame(tabs, background='#34363c')
tab2 = Frame(tabs, background='#34363c')

# =============================================================================================
# =======================================TAB 1:================================================
# =============================================================================================

img = PhotoImage(file="Imagenes/ApoloIcon.png")
smallimage= img.subsample(1,1)
tituloTab1 = Label(tab1, image=smallimage, bd = 0,)
tituloTab1.place(relx=.5, rely=0.15, anchor="center")

def selectButton(numero):
    if valores[numero]:
        botones[numero].configure(background="#25ff00")
        valores[numero]=0
    else:
        botones[numero].configure(background="#34363c")
        valores[numero]=1
    if valores.count(0)==0:
        createScanButton.configure(state=DISABLED)
    else:
        createScanButton.configure(state=NORMAL)


imagenBotones = ["idAutFailures", "BAC", "Component", "IG", "SSRF", "Crypto"]
relxBut=.08
relyBut=.35
padx= .1683
relxLabel=0.006

b1Img=(PhotoImage(file="Imagenes/BACIcon.png")).subsample(15,15)
boton1 = Button(tab1, font=("Helvetica", 20), image=b1Img,  highlightthickness=0, fg='white', background='#34363c', command= lambda numero=0 : selectButton(numero))
boton1.place(relx=relxBut, rely=relyBut, anchor="center")
b1titulo = Label(tab1, text="Broken \n access control", background="#34363c", fg="white", font=("Quicksand Medium", 12))
b1titulo.place(relx=relxBut, rely=.47, anchor=CENTER)

relxBut+=padx
b2Img=(PhotoImage(file="Imagenes/CryptoIcon.png")).subsample(15,15)
boton2 = Button(tab1, font=("Helvetica", 20), image=b2Img, highlightthickness=0, fg='white', background='#34363c', command= lambda numero=1 : selectButton(numero))
boton2.place(relx=relxBut, rely=relyBut, anchor="center") 
b2titulo = Label(tab1, text="Cryptographic \n failures", background="#34363c", fg="white", font=("Quicksand Medium", 12))
b2titulo.place(relx=relxBut, rely=.47, anchor=CENTER)

relxBut+=padx
b3Img=(PhotoImage(file="Imagenes/IdentAuthFailures.png")).subsample(15,15)
boton3 = Button(tab1, font=("Helvetica", 20), image=b3Img, highlightthickness=0, fg='white', background='#34363c', command= lambda numero=2 : selectButton(numero))
boton3.place(relx=relxBut, rely=relyBut, anchor="center")
b3titulo = Label(tab1, text="Identification \n failures", background="#34363c", fg="white", font=("Quicksand Medium", 12))
b3titulo.place(relx=relxBut, rely=.47, anchor=CENTER)

relxBut+=padx
b4Img=(PhotoImage(file="Imagenes/SecMisconfig.png")).subsample(15,15)
boton4 = Button(tab1, font=("Helvetica", 20), image=b4Img, highlightthickness=0, fg='white', background='#34363c', command= lambda numero=3 : selectButton(numero))
boton4.place(relx=relxBut, rely=relyBut, anchor="center") 
b4titulo = Label(tab1, text="Security \n misconfiguration", background="#34363c", fg="white", font=("Quicksand Medium", 12))
b4titulo.place(relx=relxBut, rely=.47, anchor=CENTER) 

relxBut+=padx
b5Img=(PhotoImage(file="Imagenes/ComponentIcon.png")).subsample(15,15)
boton5 = Button(tab1, font=("Helvetica", 20), image=b5Img, highlightthickness=0, fg='white', background='#34363c', command= lambda numero=4 : selectButton(numero))
boton5.place(relx=relxBut, rely=relyBut, anchor="center")
b5titulo = Label(tab1, text="Vulnerable & outdated \n components", background="#34363c", fg="white", font=("Quicksand Medium", 12))
b5titulo.place(relx=relxBut, rely=.47, anchor=CENTER)

relxBut+=padx
b6Img=(PhotoImage(file="Imagenes/IGIcon.png")).subsample(15,15)
boton6 = Button(tab1, font=("Helvetica", 20), image=b6Img, highlightthickness=0, fg='white', background='#34363c', command= lambda numero=5 : selectButton(numero))
boton6.place(relx=relxBut, rely=relyBut, anchor="center")
b6titulo = Label(tab1, text="Information \n gathering", background="#34363c", fg="white", font=("Quicksand Medium", 12))
b6titulo.place(relx=relxBut, rely=.47, anchor=CENTER)
#b5titulo.place(relx=.836, rely=.44)



valores = [1,1,1,1,1,1]

botones= [boton1, boton2, boton3, boton4, boton5, boton6]

# targetLabel = Label(tab1, text="Target", font=("Calibri", 17))
# targetLabel.place(relx=0.3, rely=0.5, anchor="w")
# target = Entry(tab1, width = 20, font=("Calibri", 15))
# target.place(relx=0.5, rely=0.5, anchor="center")


# =============================================================================================
# =======================================OUTPUT FRAME:=========================================
# =============================================================================================

output = LabelFrame(tab1, text='Output', bg='#1e1f21', font=('QuickSand Medium',14), fg='white')
output.pack_propagate(False)
output.pack(ipady=120, side="bottom", fill="x", expand=False)
output.update_idletasks()
output_text = scrolledtext.ScrolledText(output, font=('Firacode', 10), fg='white', bg='#161719')
output_text.configure(state=DISABLED)
output_text.pack(fill="both", expand=True)

def reinicioBotones(): # Para reiniciar los botones a su valor por defecto cuando creo el escaner
    spawnParameters(tab1, botones, valores, output, output_text, createScanButton, cancelButton)
    for i in range(6):
        valores[i] = 1
        botones[i].configure(background="#34363c")

createScanButton = Button(tab1, text="Crear escáner", font=("QuickSand Medium", 15), highlightthickness=0, bg="#20bebe", fg="white", command=reinicioBotones)
createScanButton.config(height=1, width=11)
createScanButton.configure(disabledforeground="lightgrey")
createScanButton.configure(state=DISABLED)
createScanButton.place(relx=.48, rely=0.57, anchor="center") 
cancelButton = Button(tab1, text="X", font=("QuickSand Medium", 15), highlightthickness=0, fg='white', background='#ff0022', command=lambda : cancelProcess(output_text))
cancelButton.configure(state=DISABLED)
cancelButton.place(relx=.58, rely=0.57, anchor="center") 


# =============================================================================================
# =======================================TAB 2:================================================
# =============================================================================================

tituloTab2 = Label(tab2, text="Historial", font=("QuickSand Medium", 40), fg="white", bg="#34363c")
tituloTab2.place(relx=.5, rely=0.09, anchor="center")

tabla = ttk.Treeview(tab2, column=("Name", "Host", "Date", "Scanners"), show='headings', height=20)

tabla.column("Name", anchor="center", width="110")
tabla.heading("Name", text="Nombre")
tabla.column("Host", anchor="center", width="230")
tabla.heading("Host", text="Host")
tabla.column("Date", anchor="center", width="120")
tabla.heading("Date", text="Fecha")
tabla.column("Scanners", anchor="center", width="598")
tabla.heading("Scanners", text="Escáneres")


tabla.place(relx=.5, rely=.53, anchor=CENTER)
inspeccionar = Button(tab2, text="Inspeccionar", highlightthickness=0, font=("Quicksand Medium", 12), fg="white", bg="#20bebe", command=inspeccionarReportes)
inspeccionar.place(relx=.0915, rely=.94, anchor=CENTER)
delete= Button(tab2, text="Borrar", highlightthickness=0, font=("Quicksand Medium", 12), fg="white", bg="#ff0022", command=deleteRow)
delete.place(relx=.19, rely=.94, anchor=CENTER)


tabs.add(tab1, text="Escáneres")
tabs.add(tab2, text="Historial")

tabs.pack(expand=True, fill="both")

# =============================================================================================
# ======================CREACION DE DIRECTORIOS y LECTURA DE DATOS:===============================
# =============================================================================================

# Leo aqui los datos debido a que tienen que colocarse en la tabla al mismo ejecutar Apolo

# En esta carpeta se almacenaran los informes generados por cada uno de los escaneres
if not os.path.isdir("reportes"): # Si la carpeta para guardar los resultados (reportes) no existe
    os.mkdir("reportes") # Creo la carpeta 

# En esta carpeta se almacenaran los datos de la tabla
if not os.path.isdir("historial"): # Si la carpeta para guardar los datos no existe
    os.mkdir("historial") # Creo la carpeta 

# Aqui se crea el archivo de los datos
if not os.path.isfile("historial/datos.pkl"):
    with open('historial/datos.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        num_scanner=0 # num_scanner me servira para nombrar todos los escaneres como escaner1, escaner2, ...
        filas=[] # filas contendra una lista con cada una de las filas de la tabla que tambien son listas
        setData(num_scanner, filas, tabla, tab2)
        datos = [num_scanner, filas]
        almacenarDatos(datos)

else: # Aqui se leen los datos si existe el archivo
        with open('historial/datos.pkl', "rb") as f:  # Abro el archivo como lectura 
            num_scanner, filas = pickle.load(f) #Cargo los datos del archivo en mis dos variables
            setData(num_scanner, filas, tabla, tab2)
        for fila in filas: # Inserto los datos
            insertTabla(fila)


def cerrar(opcion):
    if opcion:
        cancelProcess(output_text)
        raiz.destroy()
    else: 
        exit_popup.destroy()

# Aqui creo el popup que se muestra antes de cerrar el entorno
def cerrarVentana():
    global exit_popup, exit_image
    exit_popup = Toplevel(raiz)
    exit_popup.title("Cerrar")
    exit_popup.geometry("250x120")
    exit_popup.resizable(False, False)
    exit_popup.config(bg="#34363c")
    exit_icon = PhotoImage(file="Imagenes/close.png")
    exit_popup.iconphoto(False, exit_icon)
    exit_image =PhotoImage(file="Imagenes/CerrarNegro.png")

    exit_label = Label(exit_popup, text="¿Desea salir del entorno?", bg="#34363c", font=("Quicksand", 14), fg="white")
    exit_label.pack(pady=10)

    exit_frame = Frame(exit_popup, bg="#34363c")
    exit_frame.pack(pady=5)

    put_exit_image = Label(exit_frame, image=exit_image, borderwidth=0)
    put_exit_image.grid(row=0, column=0, padx=10)

    button_si= Button(exit_frame, text="Salir",  highlightthickness=0, fg="black", font=("Quicksand Medium", 10), command= lambda : cerrar(1))
    button_si.grid(row=0, column=1, padx=10)

    button_no= Button(exit_frame, text="Cancelar",  highlightthickness=0, fg="black", font=("Quicksand Medium", 10),  command= lambda : cerrar(0))
    button_no.grid(row=0, column=2, padx=10)
    


raiz.protocol("WM_DELETE_WINDOW", cerrarVentana)

raiz.mainloop()
