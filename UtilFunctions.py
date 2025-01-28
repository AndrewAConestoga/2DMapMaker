import tkinter as tk
import customtkinter as ctk
import Constants as C
import os
import Map as map
import mouse as mouse

### This will be used for the Create button when creating a new map 

def CheckForSaveFolder():

    return os.path.exists("./"+C.SAVE_FOLDER)

def CreateNewSaveFolder():

    os.makedirs(C.SAVE_FOLDER)
    


def ValidateSaveFolder():

    if (CheckForSaveFolder()==False):
        CreateNewSaveFolder()

def GetAllSaveNames():

    filenames = os.listdir(C.SAVE_FOLDER)

    for i in range(len(filenames)):
        filenames[i] = filenames[i].replace(".txt", "")


    return filenames

def CheckIfNotExists(filename):

    try:

        file = open(C.SAVE_FOLDER+filename, "r")
        file.close()
        return False
    
    except FileNotFoundError:

        return True
    
def LoadMapImages(filename):

    try:

        ## get dimensions
        file = open(C.SAVE_FOLDER+filename, "r")

        Y = 1
        line = file.readline()
        X = len(line.split("|"))
        while (file.readline()!=""):
            Y = Y + 1


        ## get images
        file = open(C.SAVE_FOLDER+filename, "r")

        images = [[0 for _ in range(X)] for _ in range(Y)]

        for i in range (Y):

            line = file.readline()
            vals = line.split("|")

            for j in range (X):

                images[i][j] = vals[j].replace("Tiles/","").replace("\n","")



        file.close()

        return images
    
    except FileNotFoundError:

        return C.INVALID
    

        


    






    