import tkinter as tk
import UtilFunctions as Util
import customtkinter as ctk 
from PIL import Image
import os 
import Tiles as Tile
import Map as map
from threading import Thread
import mouse as mouse
import Constants as C

## Globals
Map = None


## removes all elements and frames from the screen 
def ClearScreen():

    Map_Frame.forget()
    Create_Frame.forget()
    Title_Frame.forget()
    Edit_Frame.forget()

    ## Reset Labels 
    Dimension_Error_Message.configure(text="")

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
def CreateNewMap(x,y,Name):

    global Map
    Map = map.Map(frame=Map_Frame, x=x, y=y, width=MapEditScreen_Width, height=MapEditScreen_Height, button_height=int(MapEditScreen_Height/y)-C.BUTTON_BORDER_WIDTH, button_width=int(MapEditScreen_Width/x)-C.BUTTON_BORDER_WIDTH, img=blankImage, images=None, tiles=Tiles, name=Name)
    Map.Map.grid(pady=C.PAD_BIG,padx=C.PAD_LARGE,  row=0, column=1, rowspan=2)

## creates a new map and then sets the screen to the map screen with the new map loaded, map size is based on user input in the textboxes
def NewMapScreen():

    ValidDimensions = GetIntDimensions()
    Name = Name_TextBox.get(0.0, "end")
    Name = Name.replace("\n", "")

    if (ValidDimensions[C.X]==C.INVALID or ValidDimensions[C.Y]==C.INVALID):

          Dimension_Error_Message.configure(text="Incorrect dimensions inputted")
          return
    
    elif (InvalidName(Name)):

        Dimension_Error_Message.configure(text="File already exists or empty name")
        return


    CreateNewMap(x=int(Dimension_X_TextBox.get(0.0, "end")), y=int(Dimension_Y_TextBox.get(0.0, "end")), Name=Name)
    global Map
    Map.SaveMapToFile()
    MapScreen()

def EditMap(name):

    images = Util.LoadMapImages(name+".txt")

    if images==C.INVALID:

        return 
    
    x = len(images)
    y = len(images[C.X])

    global Map
    Map = map.Map(frame=Map_Frame, x=x, y=y, width=MapEditScreen_Width, height=MapEditScreen_Height, button_height=int(MapEditScreen_Height/y)-C.BUTTON_BORDER_WIDTH, button_width=int(MapEditScreen_Width/x)-C.BUTTON_BORDER_WIDTH, img=blankImage, images=images, tiles=Tiles, name=name)
    MapScreen()
    Map.Map.grid(pady=C.PAD_BIG,padx=C.PAD_LARGE,  row=0, column=1, rowspan=2)

## Saves the current map as a PNG file in the working directory
def ExportMapToPNG():

    global Map
    Map.ExportMap()

def SaveMap():

    global Map
    Map.SaveMapToFile()


## Gets the dimensions from the GUI elements, Values return -1 or INVALID if they are not valid, returns array of [x_value, y_value]
def GetIntDimensions():

    try:
        ## If inputted values cannot be converted to integers 
        dimension_x = int(Dimension_X_TextBox.get(0.0, "end"))
        dimension_y = int(Dimension_Y_TextBox.get(0.0, "end"))
    except:
        return [C.INVALID,C.INVALID]
    
    if (dimension_x < C.MIN_MAP_SIDE_DIMENSION or dimension_x > C.MAX_MAP_SIDE_DIMENSION):

        dimension_x = C.INVALID

    if (dimension_y < C.MIN_MAP_SIDE_DIMENSION or dimension_y > C.MAX_MAP_SIDE_DIMENSION):

        dimension_y = C.INVALID

    return [dimension_x,dimension_y]

def InvalidName(Name):

    if len(Name)==0 or Util.CheckIfNotExists(Name+".txt")==False:
        return True
    
    return False



## Appearence/Theme of the window and GUI
ctk.set_appearance_mode("dark")        
ctk.set_default_color_theme("green")


## Create the window for the gui
window = ctk.CTk()
Util.ValidateSaveFolder()


### C of the devices resolution
HEIGHT= C.HEIGHT
if window.winfo_screenheight() < HEIGHT:

    ## makes sure window height is not higher then the devices height
    HEIGHT = window.winfo_screenheight()

WIDTH = C.WIDTH
if window.winfo_screenwidth() < WIDTH:

    ## makes sure window width is not wider then the devices width
    WIDTH = window.winfo_screenwidth()
    

### Create the frames that will be used for the different screen layouts 
Map_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")
Edit_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")
Title_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")
Create_Frame = ctk.CTkFrame(master=window, width=WIDTH, height=HEIGHT, fg_color="transparent")

## Create the layout for the title screen frame
Create_New_Map_Width = int(WIDTH*C.SCREEN_FIFTH)
Create_New_Map_Height = int(HEIGHT*C.SCREEN_TENTH)
Create_Map_Width = int(WIDTH*C.SCREEN_THIRD)
Create_Map_Height = int(HEIGHT*C.SCREEN_EIGHTH)
Title_Label = ctk.CTkLabel(master=Title_Frame, text="2D Map Maker", width=Create_Map_Width, height=Create_Map_Height, bg_color="transparent", font=('<Abel>', C.FONT_TITLE))
Create_New_Map = ctk.CTkButton(master=Title_Frame, text="Create New Map", width=Create_Map_Width, height=Create_Map_Height, command=CreateScreen, font=('<Aerial>', C.FONT_LARGE))
Edit_Map = ctk.CTkButton(master=Title_Frame, text="Edit Map", width=Create_Map_Width, height=Create_Map_Height, font=('<Aerial>', C.FONT_LARGE), command=EditScreen)

## Create the layout for the create new map screen frame
Dimension_Button_Height = int(HEIGHT*C.SCREEN_DIMENSION_INPUT_HEIGHT)
Dimension_Button_Width = int(WIDTH*C.SCREEN_DIMENSION_INPUT_WIDTH)
Create_Map_Button = ctk.CTkButton(master=Create_Frame, width=Create_New_Map_Width, text="Create Map", height=Create_New_Map_Height, command=NewMapScreen)
Name_TextBox = ctk.CTkTextbox(master=Create_Frame, width=Create_New_Map_Width, height=Create_New_Map_Height, font=('<Aerial>', C.FONT_SMALL), bg_color="white")
Dimension_X_TextBox = ctk.CTkTextbox(master=Create_Frame, width=Dimension_Button_Width, height=Dimension_Button_Height, font=('<Aerial>', C.FONT_SMALL), bg_color="white")
Dimension_Y_TextBox = ctk.CTkTextbox(master=Create_Frame, width=Dimension_Button_Width, height=Dimension_Button_Height, font=('<Aerial>', C.FONT_SMALL), bg_color="white")
Dimension_X_Label = ctk.CTkLabel(master=Create_Frame, width=Dimension_Button_Width, height=Dimension_Button_Height, font=('<Aerial>', C.FONT_SMALL), text="X")
Dimension_Y_Label = ctk.CTkLabel(master=Create_Frame, width=Dimension_Button_Width, height=Dimension_Button_Height, font=('<Aerial>', C.FONT_SMALL), text="Y")
Name_Label = ctk.CTkLabel(master=Create_Frame, width=Create_New_Map_Width, height=Create_New_Map_Height, font=('<Aerial>', C.FONT_MEDIUM), text="Name")
Dimension_Error_Message = ctk.CTkLabel(master=Create_Frame, width=Create_New_Map_Width, text="", height=Create_New_Map_Height, font=('<Aerial>', C.FONT_MEDIUM))
Space = ctk.CTkLabel(master=Create_Frame, width=Create_New_Map_Width, text="", height=Create_New_Map_Height, font=('<Aerial>', C.FONT_MEDIUM))

Create_Map_Button.grid(padx=C.PAD_PIXEL, pady=C.PAD_HUGE, row=0, column=0, columnspan=2)
Name_Label.grid(padx=C.PAD_PIXEL, row=1, column=0, columnspan=2)
Name_TextBox.grid(padx=C.PAD_PIXEL, pady=C.PAD_SMALL, row=2, column=0, columnspan=2)
Space.grid(pady=C.PAD_LARGE, row=3, column=0, columnspan=2)
Dimension_X_Label.grid(padx=C.PAD_PIXEL, row=4, column=0)
Dimension_Y_Label.grid(padx=C.PAD_PIXEL, row=4, column=1)
Dimension_Y_TextBox.grid(padx=C.PAD_PIXEL, pady=C.PAD_SMALL, row=5, column=0)
Dimension_X_TextBox.grid(padx=C.PAD_PIXEL, pady=C.PAD_SMALL, row=5, column=1)
Dimension_Error_Message.grid(padx=C.PAD_PIXEL, pady=C.PAD_HUGE, row=6, column=0, columnspan=2)

## Create the layout for the edit map screen frame 
All_Maps_Scroll_Frame = ctk.CTkScrollableFrame(Edit_Frame,label_text="Maps", height=int(HEIGHT/1.2), width=int(WIDTH/2), label_font=('<Aerial>', C.FONT_MEDIUM))


Save_Files = Util.GetAllSaveNames()
for i in range(len(Save_Files)):
    Edit_Map_Button = ctk.CTkButton(master=All_Maps_Scroll_Frame, text=Save_Files[i], width=int(WIDTH/2), height=Create_New_Map_Height/2, command=lambda name=Save_Files[i]: EditMap(name), font=('<Aerial>', C.FONT_SMALL))
    Edit_Map_Button.grid(padx=C.PAD_TINY, pady=C.PAD_TINY, row=i, column=0)


All_Maps_Scroll_Frame.pack(pady=C.PAD_LARGE)



Title_Label.pack(pady=C.PAD_HUGE,padx=0)
Create_New_Map.pack(pady=C.PAD_MEDIUM,padx=0)
Edit_Map.pack(pady=C.PAD_MEDIUM,padx=0)



## settings for the window of the application 
window.geometry(str(WIDTH)+"x"+str(HEIGHT)) ## set the geometry to be 1920 x 1200 but on smaller screens it will fill the entire screen 
window.title("2D Map Maker")


###################### Widgets that will be used for the gui ######################

### Selection of Tiles Scroll Frame
TileSelection_Height = int(HEIGHT*C.SCREEN_HALF)
TileSelection_Width = int(WIDTH*C.SCREEN_QUARTER)
TileSelection_Rows = C.TILE_COLUMNS

### Scrollable Frame for Drawing the map
MapEditScreen_Width = MapEditScreen_Height = int(TileSelection_Width*2)
## MapEditScreen_Height = MapEditScreen_Width

### For Save and Export Frame to display the buttons next to eachother 
Save_Export_Height = MapEditScreen_Height - TileSelection_Height
Save_Export_Frame = ctk.CTkFrame(master=Map_Frame, width = TileSelection_Width, height = Save_Export_Height, fg_color="transparent")

TileSelection = ctk.CTkScrollableFrame(Map_Frame,label_text="Tiles", height=TileSelection_Height, width=TileSelection_Width)

## Tiles Selection Screen Frame 
SIZE_OF_TILES_TUPLE = (int(TileSelection_Width/TileSelection_Rows)-TileSelection_Rows-C.BUTTON_BORDER_WIDTH,int(TileSelection_Width/TileSelection_Rows)-TileSelection_Rows-C.BUTTON_BORDER_WIDTH)
DIMENSION_OF_TILE_BUTTON = int(TileSelection_Width/TileSelection_Rows)-TileSelection_Rows
DIMENSION_OF_MAP_BUTTON = int(MapEditScreen_Width/C.MAP_DIMENSION)-C.BUTTON_BORDER_WIDTH
MAP_BUTTON_SIZE_TUPLE = (DIMENSION_OF_MAP_BUTTON,DIMENSION_OF_MAP_BUTTON)
Tiles = Tile.Tiles(TileSelection, C.TILES_PATH, SIZE_OF_TILES_TUPLE, TileSelection_Width, TileSelection_Height, TileSelection_Rows, MAP_BUTTON_SIZE_TUPLE)
blankImage = ctk.CTkImage(light_image=Image.open(C.TILES_PATH+C.BLANK_IMAGE_NAME), dark_image=Image.open(C.TILES_PATH+C.BLANK_IMAGE_NAME), size=MAP_BUTTON_SIZE_TUPLE)

#map.Map(frame=Map_Frame, x=C.MAP_DIMENSION, y=C.MAP_DIMENSION, width=MapEditScreen_Width, height=MapEditScreen_Height, button_height=DIMENSION_OF_MAP_BUTTON, button_width=DIMENSION_OF_MAP_BUTTON, img=blankImage, tiles=Tiles)

save = ctk.CTkButton(master=Save_Export_Frame, text="Save", width=int(DIMENSION_OF_TILE_BUTTON*1.5), height=int(DIMENSION_OF_TILE_BUTTON*C.SCREEN_HALF), fg_color="#00ABF5", command=SaveMap)
export = ctk.CTkButton(master=Save_Export_Frame, text="Export", width=int(DIMENSION_OF_TILE_BUTTON*1.5), height=int(DIMENSION_OF_TILE_BUTTON*C.SCREEN_HALF), fg_color="#00ABF5", command=ExportMapToPNG)

## Placing widgets on the initial window 
TileSelection.grid(pady=C.PAD_MEDIUM,padx=C.PAD_LARGE, row=0, column=0)
Save_Export_Frame.grid(pady=C.PAD_SMALL,padx=C.PAD_MEDIUM, row=1, column=0)
save.pack(pady=C.PAD_MEDIUM,padx=C.PAD_SMALL,anchor=ctk.SE, side=ctk.RIGHT)
export.pack(pady=C.PAD_MEDIUM,padx=C.PAD_SMALL,anchor=ctk.SE, side=ctk.LEFT)
Title_Frame.pack()

### Mainloop must be after packing buttons/labels or else they will not show up 
window.mainloop()

