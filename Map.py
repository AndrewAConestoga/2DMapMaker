import customtkinter as ctk
import tkinter as tk
import mouse as mouse 
from PIL import Image
import Tiles as Tile
import Constants as C
import numpy as np
import getpass

class Map:

    def __init__(self, frame, x, y, width, height, button_width, button_height, img,  tiles:Tile, name, images):

        self.MousePressed = False
        self.Map = ctk.CTkFrame(frame, height=height, width=width)
        self.tiles:Tile = tiles
        self.name:str = name

        print(images)

        self.dimension = button_width
        if button_height < self.dimension:
            self.dimension = button_height

        self.Buttons = [[0 for _ in range(int(y))] for _ in range(int(x))]
        self.ImgIndexAtButton = [[0 for _ in range(int(y))] for _ in range(int(x))]

        #####################################
        ## Make 40 the highest dimension a map can be due to lag reasons because customtkinter sucks 
        for i in range(x):
            for j in range(y):
                Button = ctk.CTkButton(master=self.Map, text="", image=img, fg_color="transparent", corner_radius=0, width=self.dimension, height=self.dimension, command=lambda X=i, Y=j: self.SetImageScaled(self.dimension,self.dimension,X,Y))
                Button.bind('<Button-1>',lambda event, X=i, Y=j: self.MousePress(event, X, Y))
                Button.bind('<ButtonRelease-1>',self.MouseReleased)
                Button.bind('<Enter>', command=lambda event, X=i, Y=j: self.AutoFill(event,X,Y))
                Button.grid(row=i, column=j)
                self.Buttons[i][j] = Button

                if images==None:
                    self.ImgIndexAtButton[i][j] = C.BLANK_IMAGE
                    Button.configure(image=self.tiles.GetScaledDownImageAtIndex(C.BLANK_IMAGE,self.dimension,self.dimension))
                else:
                    print("X:"+str(j)+"   Y:"+str(i))
                    self.ImgIndexAtButton[i][j] = self.tiles.GetImageIndexByName(images[i][j])
                    Button.configure(image=self.tiles.GetScaledDownImageByName(images[i][j],self.dimension,self.dimension))




    def SetImageScaled(self, width, height, x, y):

        if (self.tiles.GetSelected()==C.BLANK_IMAGE):

            return False
        
        newImage=self.tiles.GetScaledDownImageAtIndex(self.tiles.GetSelected(),width,height)
        self.Buttons[x][y].configure(image=newImage)
        self.ImgIndexAtButton[x][y] = self.tiles.GetSelected()
        self.GetFirstPixelOfImage(x,y)
        self.MousePressed = True
        

    def AutoFill(self, event, x, y):

        ## If the user is holding down left click and they enter a new tile, then fill it with the selected tile
        if self.MousePressed:
            self.SetImageScaled(self.dimension,self.dimension,x,y)


    def MousePress(self, event, x, y):

        self.MousePressed = True
        mouse.right_click()

    def MouseReleased(self, event):

        self.MousePressed = False

    ## This will be used if the mouse has been released while being pressed outside of the frame 
    def ForceMouseReleased(self):

        self.MousePressed = False

    def IsPressed(self):

        return self.MousePressed

    ## Used for testing 
    def GetFirstPixelOfImage(self, x, y):

        img = self.tiles.GetPillowImageAtIndex(self.ImgIndexAtButton[x][y], C.TILE_SIZE_IN_PNG_IN_PX, C.TILE_SIZE_IN_PNG_IN_PX)

    def ExportMap(self):

        ## img:Image = self.tiles.GetPillowImageAtIndex(self.ImgIndexAtButton[0][0], C.TILE_SIZE_IN_PNG_IN_PX, C.TILE_SIZE_IN_PNG_IN_PX)
        ## ArrayOfPixels = [[0 for _ in range(int(C.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons))] for _ in range(int(C.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons[0]))]
        ArrayOfPixels = np.zeros(shape=(int(C.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons), int(C.TILE_SIZE_IN_PNG_IN_PX)*len(self.Buttons[C.X]), C.RGBA), dtype=np.uint8)


        for my in range (len(self.Buttons)):
            for mx in range(len(self.Buttons[C.X])):

                # Load image 
                img:Image = self.tiles.GetPillowImageAtIndex(self.ImgIndexAtButton[my][mx], C.TILE_SIZE_IN_PNG_IN_PX, C.TILE_SIZE_IN_PNG_IN_PX).convert("RGBA")

                for px in range(C.TILE_SIZE_IN_PNG_IN_PX):
                    for py in range(C.TILE_SIZE_IN_PNG_IN_PX):
                
                        pixel = img.getpixel((px,py))
                        ArrayOfPixels[py+(my*C.TILE_SIZE_IN_PNG_IN_PX),px+(mx*C.TILE_SIZE_IN_PNG_IN_PX)] = pixel

        newImg = Image.fromarray(ArrayOfPixels, "RGBA")
        newImg.save("/Users/"+getpass.getuser()+"/Downloads/"+self.name+".png")

    
    def SaveMapToFile(self):

        file = open(C.SAVE_FOLDER+self.name+".txt", "w")

        for x in range(len(self.Buttons)):
            for y in range(len(self.Buttons[C.X])):

                print(self.tiles.GetImagePathAtIndex(self.ImgIndexAtButton[x][y]),file=file, end="")
                if y < len(self.Buttons[C.X]) - 1:
                    print("|", file=file, end="")

            if x < len(self.Buttons) - 1:
                print("",file=file)

        file.close()

