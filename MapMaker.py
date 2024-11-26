import tkinter as tk
import ButtonFunctions as BF
import customtkinter as ctk 
from PIL import Image
import os 
import Tiles as Tile
import ctkxy_frame as ctkxy
import Map as map
from threading import Thread
import pygame as Pygame
import mouse as mouse
import Constants as Constants

## Globals
Map = None


## removes all elements and frames from the screen 
def ClearScreen():

    Map_Frame.forget()
    Create_Frame.forget()
    Title_Frame.forget()
    Edit_Frame.forget()

## Sets the screen to the map screen
def MapScreen():

    ClearScreen()
    Map_Frame.pack()

## Sets the screen to the edit existing map screen
def EditScreen():

    ClearScreen()
    Edit_Frame.pack()

## sets the screen to the title screen
def TitleScreen():

    ClearScreen()
    Title_Frame.pack()

## sets the screen to the create a new map sceen 
def CreateScreen():

    ClearScreen()
    Create_Frame.pack()

## Creates a new blank map of size x as the amount of rows of tiles and y as the amount of columns
def CreateNewMap(x,y):

    global Map
    Map = map.Map(frame=Map_Frame, x=x, y=y, width=MapEditScreen_Width, height=MapEditScreen_Height, button_height=int(MapEditScreen_Height/y)-Constants.BUTTON_BORDER_WIDTH, button_width=int(MapEditScreen_Width/x)-Constants.BUTTON_BORDER_WIDTH, img=blankImage, tiles=Tiles)
    Map.Map.grid(pady=20,padx=50,  row=0, column=1, rowspan=2)

## creates a new map and then sets the screen to the map screen with the new map loaded, map size is based on user input in the textboxes
def NewMapScreen():

    CreateNewMap(x=int(Dimension_X_TextBox.get(0.0, "end")), y=int(Dimension_Y_TextBox.get(0.0, "end")))

    ClearScreen()
    Map_Frame.pack()

def ExportMapToPNG():

    global Map
    Map.ExportMap()


## Appearence/Theme of the window and GUI
ctk.set_appearance_mode("dark")        
ctk.set_default_color_theme("green")


## Create the window for the gui
window = ctk.CTk()


### Constants of the devices resolution
HEIGHT=1000
if window.winfo_screenheight() < HEIGHT:

    ## makes sure window height is not higher then the devices height
    HEIGHT = window.winfo_screenheight()

WIDTH = 1600
if window.winfo_screenwidth() < WIDTH:

    ## makes sure window width is not higher then the devices width
    WIDTH = window.winfo_screenwidth()

### Create the frames that will be used for the different screen layouts 
Map_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")
Edit_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")
Title_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")
Create_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")

## Create the layout for the title screen frame
Create_New_Map_Width = int(WIDTH/3)
Create_New_Map_Height = int(HEIGHT/8)
Title_Label = ctk.CTkLabel(master=Title_Frame, text="2D Map Maker", width=Create_New_Map_Width, height=Create_New_Map_Height, bg_color="transparent", font=('<Abel>', 50))
Create_New_Map = ctk.CTkButton(master=Title_Frame, text="Create New Map", width=Create_New_Map_Width, height=Create_New_Map_Height, command=CreateScreen, font=('<Aerial>', 40))
Edit_Map = ctk.CTkButton(master=Title_Frame, text="Edit Map", width=Create_New_Map_Width, height=Create_New_Map_Height, font=('<Aerial>', 40))

## Create the layout for the create new map screen frame
Dimension_Button_Height = int(HEIGHT/26)
Dimension_Button_Width = int(WIDTH/20)
Create_Map_Button = ctk.CTkButton(master=Create_Frame, width=Create_New_Map_Width, text="Create Map", height=Create_New_Map_Height, command=NewMapScreen)
Dimension_X_TextBox = ctk.CTkTextbox(master=Create_Frame, width=Dimension_Button_Width, height=Dimension_Button_Height, font=('<Aerial>', 20), bg_color="white")
Dimension_Y_TextBox = ctk.CTkTextbox(master=Create_Frame, width=Dimension_Button_Width, height=Dimension_Button_Height, font=('<Aerial>', 20), bg_color="white")
Create_Map_Button.grid(padx=1, row=0, column=0, columnspan=2)
Dimension_X_TextBox.grid(padx=1, pady=80, row=1, column=0)
Dimension_Y_TextBox.grid(padx=1, pady=80, row=1, column=1)



Title_Label.pack(pady=80,padx=0)
Create_New_Map.pack(pady=20,padx=0)
Edit_Map.pack(pady=20,padx=0)



## settings for the window of the application 
window.geometry(str(WIDTH)+"x"+str(HEIGHT)) ## set the geometry to be 1920 x 1200 but on smaller screens it will fill the entire screen 
window.title("2D Map Maker")


###################### Widgets that will be used for the gui ######################

### Selection of Tiles Scroll Frame
TileSelection_Height = int(HEIGHT/2)
TileSelection_Width = int(WIDTH/4)
TileSelection_Rows = Constants.TILE_COLUMNS
TileSelection = ctk.CTkScrollableFrame(Map_Frame,label_text="Tiles", height=TileSelection_Height, width=TileSelection_Width)

### Scrollable Frame for Drawing the map
MapEditScreen_Width = int(TileSelection_Width*2.3)
MapEditScreen_Height = int(TileSelection_Width*2.3)

### For Save and Export Frame to display the buttons next to eachother 
Save_Export_Height = MapEditScreen_Height - TileSelection_Height
Save_Export_Frame = ctk.CTkFrame(master=Map_Frame, width = TileSelection_Width, height = Save_Export_Height, fg_color="transparent")

TileSelection = ctk.CTkScrollableFrame(Map_Frame,label_text="Tiles", height=TileSelection_Height, width=TileSelection_Width)

## Tiles Selection Screen Frame 
SIZE_OF_TILES_TUPLE = (int(TileSelection_Width/TileSelection_Rows)-TileSelection_Rows-Constants.BUTTON_BORDER_WIDTH,int(TileSelection_Width/TileSelection_Rows)-TileSelection_Rows-Constants.BUTTON_BORDER_WIDTH)
DIMENSION_OF_TILE_BUTTON = int(TileSelection_Width/TileSelection_Rows)-TileSelection_Rows
DIMENSION_OF_MAP_BUTTON = int(MapEditScreen_Width/Constants.MAP_DIMENSION)-Constants.BUTTON_BORDER_WIDTH
MAP_BUTTON_SIZE_TUPLE = (DIMENSION_OF_MAP_BUTTON,DIMENSION_OF_MAP_BUTTON)
Tiles = Tile.Tiles(TileSelection, Constants.TILES_PATH, SIZE_OF_TILES_TUPLE, TileSelection_Width, TileSelection_Height, TileSelection_Rows, MAP_BUTTON_SIZE_TUPLE)
blankImage = ctk.CTkImage(light_image=Image.open(Constants.TILES_PATH+"White.jpg"), dark_image=Image.open(Constants.TILES_PATH+"White.jpg"), size=MAP_BUTTON_SIZE_TUPLE)

#map.Map(frame=Map_Frame, x=Constants.MAP_DIMENSION, y=Constants.MAP_DIMENSION, width=MapEditScreen_Width, height=MapEditScreen_Height, button_height=DIMENSION_OF_MAP_BUTTON, button_width=DIMENSION_OF_MAP_BUTTON, img=blankImage, tiles=Tiles)

save = ctk.CTkButton(master=Save_Export_Frame, text="Save", width=int(DIMENSION_OF_TILE_BUTTON*1.5), height=int(DIMENSION_OF_TILE_BUTTON/2), fg_color="#00ABF5")
export = ctk.CTkButton(master=Save_Export_Frame, text="Export", width=int(DIMENSION_OF_TILE_BUTTON*1.5), height=int(DIMENSION_OF_TILE_BUTTON/2), fg_color="#00ABF5", command=ExportMapToPNG)

## Placing widgets on the initial window 
TileSelection.grid(pady=20,padx=50, row=0, column=0)
Save_Export_Frame.grid(pady=10,padx=20, row=1, column=0)
save.pack(pady=20,padx=10,anchor=ctk.SE, side=ctk.RIGHT)
export.pack(pady=20,padx=10,anchor=ctk.SE, side=ctk.LEFT)
Title_Frame.pack()

### Mainloop must be after packing buttons/labels or else they will not show up 
window.mainloop()





