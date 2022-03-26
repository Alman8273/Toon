import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path

import sys
import matplotlib.pyplot as plt #resolved
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('425x600')
top.resizable(0,0)
top.title('Toon')
top.configure(background='#9c9c9c')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

    #top of app.\
greet=Label(top, text="Welcome to the Image Cartoonifier", fg='red', bg='#9c9c9c', font=("Helvetica", 16, 'bold'))
greet.place(x=45,y=10)

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)

upload=Button(top,text="Select image",command=upload,padx=10,pady=5)
upload.configure(background='#449656', foreground='white',font=('Arial',16,'bold'))
upload.pack(side=TOP,pady=50)

def cartoonify(ImagePath):
    # read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
   
    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose png or jpeg file")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (960, 540))
    
    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))

    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    
    #applying bilateral filter to remove noise and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
   
    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    #plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
       
    save_gray=Button(top,text="Save Grayscaled",command=lambda: save1(ReSized2, ImagePath),padx=30,pady=5)
    save_gray.configure(background='#3e2945', foreground='white',font=('Arial',16,'bold'))
    save_gray.pack(side=TOP,pady=10)

    save_blurredgray=Button(top,text="Save Blurred Grayscale",command=lambda: save2(ReSized3, ImagePath),padx=30,pady=5)
    save_blurredgray.configure(background='#3e2945', foreground='white',font=('Arial',16,'bold'))
    save_blurredgray.pack(side=TOP,pady=10)
        
    save_sketch=Button(top,text="Save Sketch",command=lambda: save3(ReSized4, ImagePath),padx=30,pady=5)
    save_sketch.configure(background='#3e2945', foreground='white',font=('Arial',16,'bold'))
    save_sketch.pack(side=TOP,pady=10)
        
    save_blurredorig=Button(top,text="Save Blurred Original",command=lambda: save4(ReSized5, ImagePath),padx=30,pady=5)
    save_blurredorig.configure(background='#3e2945', foreground='white',font=('Arial',16,'bold'))
    save_blurredorig.pack(side=TOP,pady=10)
        
    save_tonnd=Button(top,text="Save Toon'd",command=lambda: save5(ReSized6, ImagePath),padx=30,pady=5)
    save_tonnd.configure(background='#3e2945', foreground='white',font=('Arial',16,'bold'))
    save_tonnd.pack(side=TOP,pady=10)
   
    saves=Label(top, text="Select the image you would like to save!", fg='red', bg='#9c9c9c', font=("Helvetica", 16, 'bold'))
    saves.place(x=15,y=113)   
    
    plt.show()
    
    
def save1(ReSized2, ImagePath):
    #saving an image using imwrite()
    newName="grayscale edit"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized2, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
def save2(ReSized3, ImagePath):
    #saving an image using imwrite()
    newName="blurred grayscale edit"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized3, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
def save3(ReSized4, ImagePath):
    #saving an image using imwrite()
    newName="sketched edit"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized4, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
def save4(ReSized5, ImagePath):
    #saving an image using imwrite()
    newName="blurred original edit"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized5, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
def save5(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="blurred original edit"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

top.mainloop()
