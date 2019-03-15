#Tkinter para diseño de GUI
from tkinter import filedialog
from tkinter import *

#Libreria para manipulación de imágenes en GUI
from PIL import Image
from PIL import ImageTk

#OpenCV para manipulación de imagenes
import cv2

#Cálculos
import numpy as np

#Función para realizar gradiente automático
#Recibe la imagen a convertir, sigma = 0.33 no recuerdo porque, probar con 0
def AutoCanny(image, sigma=0):
    
    #Obtiene la media de la intensidad de los pixeles en la imagen
    v = np.median(image)

    #Aplica detección automática usando como paramétros la media
    minim = int(max(0, (1.0 - sigma)*v ))
    maxim = int(min(255, (1.0 + sigma)*v ))
    edgeImage = cv2.Canny(image, minim, maxim)

    #retorna la imagen transformada
    return edgeImage


#Función para obtener imagen mediante su ruta
def SelectImage():

    #contenedores de imagenenes, (original y modificada)
    global panelA, panelB

    #imagen guardada en su ruta
    path = filedialog.askopenfilename()

    #Validar si se seleccionó una imagen
    if len(path) > 0:

        #Se carga la imagen
        image = cv2.imread(path)

        #Conversión de la imagen a escala de grises
        #1
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #Imagen difuminada
        #Limpia el ruido en la imagen
        blurImage = cv2.GaussianBlur(grayImage, (5, 5), 0)

        #Transformar imagen a solo bordes
        edgedImage = AutoCanny(blurImage)

        #Copia de imagen de contornos, el próximo método modifica la imagen, por eso se hace una copia
        edgedImageCp = edgedImage

        #Retorna una lista de los contornos de los objetos 
        (contornos,_) = cv2.findContours(edgedImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #Dibuja los contornos econtrados sobre la imagen original
        cv2.drawContours(image, contornos, -1,(0,0,255), 2)
        
        
        #OpenCV representa colores en BGR, PIL en RGB, conversión necesaria para imagen original
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #Convertir imagen original y nueva a formato PIL
        image = Image.fromarray(image)
        edgedImage = Image.fromarray(edgedImage)

        #Convirtiendo imagen de formato PIL a Tk
        image = ImageTk.PhotoImage(image)
        edgedImage = ImageTk.PhotoImage(edgedImage)

        #Si los paneles están vacíos
        if panelA is None or panelB is None:

            #La imagen original se mostrará en A, la modificada en B
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            panelB = Label(image=edgedImage)
            panelB.image = edgedImage
            panelB.pack(side="right", padx=10, pady=10)

        else:
            #Actualizar los paneles en caso contrario
            panelA.configure(image=image)
            panelB.configure(image=edgedImage)
            panelA.image = image
            panelB.image = edgedImage
        
        
#Programa principal

#Ventana principal
window = Tk()

#Inicializando panel en nulo
panelA = None
panelB = None

#Botón para seleccionar imagen
btn = Button(window, text="Seleccione imagen", command=SelectImage)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

window.mainloop()        
        
        
