import tkinter as tk
import time as Time
import UtilFunctions as BF
import customtkinter as ctk 
from PIL import Image
import os 
from threading import Thread
import Constants as C

def ErrorWindow():

    errorWindow = tk.Tk()

    errorMessage = tk.Label(master=errorWindow, text="This is an Error Message")
    errorMessage.pack()
    errorWindow.mainloop()


class Tiles:


    ## constructor for the tile class which will be a button
    def __init__(self, master, file_path, sizeOfImages, widthOfFrame, heightOfFrame, amountOfRows, sizeOfMapButtons):

        self.imageList = os.listdir(file_path)
        self.images = []
        self.selected = C.BLANK_IMAGE
        self.path = file_path

        for i in range(len(self.imageList)):
           
            if self.imageList[i].endswith(".png") or self.imageList[i].endswith(".jpg"):
               
                self.images.append(ctk.CTkImage(light_image=Image.open(file_path+self.imageList[i]), dark_image=Image.open(file_path+self.imageList[i]), size=sizeOfImages))

            else:

                self.imageList.remove(i)

        ## 
        SIZE_OF_TILES_TUPLE = (int(widthOfFrame/amountOfRows)-amountOfRows-C.BUTTON_BORDER_WIDTH,int(widthOfFrame/amountOfRows)-amountOfRows-C.BUTTON_BORDER_WIDTH)
        DIMENSION_OF_TILE_BUTTON = int(widthOfFrame/amountOfRows)-amountOfRows

        ## Add buttons to the scrollable frame
        self.mapElementButton = []
        for i in range(self.GetNumberOfImages()):
             newButton = ctk.CTkButton(master=master, text="", border_width=0,  image=self.GetImageAtIndex(i), width=DIMENSION_OF_TILE_BUTTON, height=DIMENSION_OF_TILE_BUTTON,corner_radius=0,fg_color="grey",command=lambda button_id=i: self.ButtonClicked(button_id))
             newButton.grid(row=int(i/amountOfRows), column=i%amountOfRows)
             self.mapElementButton.append(newButton)






    def GetImageAtIndex(self, index):

        try:

            return self.images[index]
        
        except:

            return False
        
    def GetImageByName(self, name):

        for i in range(len(self.imageList)):

            if self.imageList[i]==name:

                return self.images[i]
            
        return ctk.CTkImage(light_image=Image.open(self.path+"White.jpg"), dark_image=Image.open(self.path+"White.jpg"), size=C.TILE_SIZE_IN_PNG_IN_PX)
    
    def GetImageIndexByName(self, name):

        for i in range(len(self.imageList)):

            if self.imageList[i]==name:

                return i
            
        return C.BLANK_IMAGE
    
    def GetScaledDownImageByName(self, name, widthOfScale, heightOfScale):

        for i in range(len(self.imageList)):

            if self.imageList[i]==name:

                return ctk.CTkImage(light_image=Image.open(self.path+name), dark_image=Image.open(self.path+name), size=(widthOfScale,heightOfScale))
            
        return ctk.CTkImage(light_image=Image.open(self.path+"White.jpg"), dark_image=Image.open(self.path+"White.jpg"), size=(widthOfScale,heightOfScale))
        
    def GetScaledDownImageAtIndex(self, index, widthOfScale, heightOfScale):

        
        if index==C.BLANK_IMAGE:

            return ctk.CTkImage(light_image=Image.open(self.path+"White.jpg"), dark_image=Image.open(self.path+"White.jpg"), size=(widthOfScale,heightOfScale))

        try:

            return ctk.CTkImage(light_image=Image.open(self.path+self.imageList[index]), dark_image=Image.open(self.path+self.imageList[index]), size=(widthOfScale,heightOfScale))
        
        except:

            return False
        
    ## gets the Pillow image obj at index, used for taking images and reading pixel data from the image 
    def GetPillowImageAtIndex(self, index, width, height):

        if index==C.BLANK_IMAGE:

            return Image.open(self.path+"White.jpg").resize(size = (C.TILE_SIZE_IN_PNG_IN_PX, C.TILE_SIZE_IN_PNG_IN_PX))

        try:

            return Image.open(self.path+self.imageList[index]).resize(size = (C.TILE_SIZE_IN_PNG_IN_PX, C.TILE_SIZE_IN_PNG_IN_PX))
        
        except:

            return False

        
    def GetImagePathAtIndex(self, index):
        
        if index==C.BLANK_IMAGE:

            return self.path+"White.jpg"

        try:

            return self.path+self.imageList[index]
        
        except:

            return False

    def GetNumberOfImages(self):

        return len(self.images)
    
    

    def GetTileDimension(self):

        try:

            return ctk.CTkButton(self.mapElementButton[0]).cget("width")
        
        except:

            return False
        
    def GetSelected(self):

        return self.selected

        
    def ButtonClicked(self, button_num):

        for i in range(len(self.mapElementButton)):
            self.mapElementButton[i].configure(fg_color="grey")

        self.mapElementButton[button_num].configure(fg_color="blue")
        self.mapElementButton[button_num].update_idletasks()
        self.selected = button_num
        return self.GetImageAtIndex(button_num)


