import customtkinter as ctk
import tkinter as tk
import mouse as mouse 
from PIL import Image
import Tiles as Tile
import ctkxy_frame as ctkxy
import Constants as Constants
import numpy as np

class Map:

    def __init__(self, frame, x, y, width, height, button_width, button_height, img, tiles:Tile):

        self.MousePressed = False
        self.Map = ctk.CTkFrame(frame, height=height, width=width)
        self.tiles = tiles
        self.button_width = button_width
        self.button_height = button_height

        self.Buttons = [[0 for _ in range(int(y))] for _ in range(int(x))]
        self.ImgIndexAtButton = [[0 for _ in range(int(y))] for _ in range(int(x))]

        #####################################
        ## Make 40 the highest dimension a map can be due to lag reasons because customtkinter sucks 
        for i in range(x):
            for j in range(y):
                Button = ctk.CTkButton(master=self.Map, text="", image=img, fg_color="transparent", corner_radius=0, width=button_width, height=button_height, command=lambda X=i, Y=j: self.SetImageScaled(self.button_width,self.button_height,X,Y))
                Button.bind('<Button-1>',self.MousePress)
                Button.bind('<ButtonRelease-1>',self.MouseReleased)
                Button.bind('<Enter>', command=lambda event, X=i, Y=j: self.AutoFill(event,X,Y))
                Button.configure(image=self.tiles.GetScaledDownImageAtIndex(Constants.BLANK_IMAGE,button_width,button_height))
                Button.grid(row=i, column=j, padx=0, pady=0)
                self.Buttons[i][j] = Button
                self.ImgIndexAtButton[i][j] = Constants.BLANK_IMAGE


    def SetImageScaled(self, width, height, x, y):

        if (self.tiles.GetSelected()==Constants.BLANK_IMAGE):
            return False
        
        newImage=self.tiles.GetScaledDownImageAtIndex(self.tiles.GetSelected(),width,height)
        self.Buttons[x][y].configure(image=newImage)
        self.ImgIndexAtButton[x][y] = self.tiles.GetSelected()
        self.GetFirstPixelOfImage(x,y)
        self.MousePressed = True
        mouse.click("right")

    def AutoFill(self, event, x, y):

        ## If the user is holding down left click and they enter a new tile, then fill it with the selected tile
        if self.MousePressed:
            self.SetImageScaled(self.button_width,self.button_height,x,y)


    def MousePress(self, event):

        pass

    def MouseReleased(self, event):

        self.MousePressed = False

    ## This will be used if the mouse has been released while being pressed outside of the frame 
    def ForceMouseReleased(self):

        self.MousePressed = False

    ## Used for testing 
    def GetFirstPixelOfImage(self, x, y):

        img = self.tiles.GetPillowImageAtIndex(self.ImgIndexAtButton[x][y], Constants.TILE_SIZE_IN_PNG_IN_PX, Constants.TILE_SIZE_IN_PNG_IN_PX)

    def ExportMap(self):

        img:Image = self.tiles.GetPillowImageAtIndex(self.ImgIndexAtButton[0][0], Constants.TILE_SIZE_IN_PNG_IN_PX, Constants.TILE_SIZE_IN_PNG_IN_PX)
        ## ArrayOfPixels = [[0 for _ in range(int(Constants.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons))] for _ in range(int(Constants.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons[0]))]
        ArrayOfPixels = np.zeros(shape=(int(Constants.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons[0]), int(Constants.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons), 4), dtype=np.uint8)


        for mx in range (len(self.Buttons)):
            for my in range(len(self.Buttons[0])):

                # Load image 
                img:Image = self.tiles.GetPillowImageAtIndex(self.ImgIndexAtButton[my][mx], Constants.TILE_SIZE_IN_PNG_IN_PX, Constants.TILE_SIZE_IN_PNG_IN_PX).convert("RGBA")

                for px in range(Constants.TILE_SIZE_IN_PNG_IN_PX):
                    for py in range(Constants.TILE_SIZE_IN_PNG_IN_PX):
                
                        pixel = img.getpixel((px,py))
                        ArrayOfPixels[py+(my*Constants.TILE_SIZE_IN_PNG_IN_PX),px+(mx*Constants.TILE_SIZE_IN_PNG_IN_PX)] = pixel

        newImg = Image.fromarray(ArrayOfPixels, "RGBA")
        newImg.save("TestMap.png")




            
        ## img = Image.new(size=(len(self.Buttons), len(self.Buttons[0])), mode="RGB")
        





## WindowManager, AlertManager, FileManager, DeviceManager, Device, Alarm, Blinds, Camera, CoffeeMachine, Sensor, Shower, SmokeDetector, Thermostat.