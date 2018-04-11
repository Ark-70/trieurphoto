from tkinter import *
import numpy as np
from tkinter.ttk import *
from PIL import Image, ImageTk
import os
import shutil
import time

####### FAIT ########
# update tableau au suppr
# check index à chaque démarrage
# resize 300x300
# fix hauteur TKinter 300
# fermer la fenetre a la fin
# plus robuste pour les ajouts de categories

####### TODO ########
# choisir mode region
# produit en croix pour rescale
# jeu de couleur à associer selection/section resultats
# clic droit sur selection = delete

# bonus : UX clavier 1/2/3/4


####### CONSTANTES ########
MOVE = True


class MyWindow(Frame):
    # Initialisation des sections globales
    imgsDir = "imgsToSort"
    indexImg = 0
    strResultat = Label
    optionEntry = ""
    addBtn = Button
    noDmgBtn = Button




    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.initGlobalSections()
        self.initGlobalCategories()

        self.displaySection()
        self.displayCategoriesBtn()


        # self.uniqueImgId = self.getUniqueImgId()

        # btn = Button(sectionBtn, text="Salle de bain")
        # label.bind("<1>", self.quit)

    def initGlobalSections(self):
        self.sectionImgs = Frame
        self.sectionBtns = Frame
        self.sectionAddBtns = Frame
        self.sectionResultats = Frame
        self.sectionCategoriesBtns = Frame

    def initGlobalCategories(self):
        self.myImgs = []
        self.myImgsNames = []
        self.categories = ["salle de bain","cuisine","salon","chambre"]
        self.categoriesButtons = []
        self.regions = ["Dégat des eaux", "",]
        self.regionsButtons = []
        self.options = self.categories
        self.optionsButtons = self.categoriesButtons

    def displaySection(self):
        # les 3 sections principales
        self.sectionImgs = Frame(self, width="300", height="300")
        self.sectionBtns = Frame(self)
        self.sectionResultat = Frame(self, width="300", height="300")
        # les 2 sous-sections du milieu
        self.sectionCategoriesBtns = Frame(self.sectionBtns)
        self.sectionAddBtns = Frame(self.sectionBtns)
        # affichage des 3 sections
        self.sectionImgs.grid(row=0, column=0)
        self.sectionBtns.grid(row=0, column=1)
        self.sectionResultat.grid(row=0, column=2)
        # affichage des 2 sous-sections
        self.sectionAddBtns.grid(row=0)
        self.sectionCategoriesBtns.grid(row=1)

        # inputs de la sous-section du haut AddBtns
        self.optionEntry = Entry(self.sectionAddBtns);
        self.addBtn = Button(self.sectionAddBtns, text="+", command=self.addCustomCategoryButton)
        self.optionEntry.grid(row=0, column=0)
        self.addBtn.grid(row=0, column=1)
        self.strResultat = Label(self.sectionResultat, width="50", text="salut")
        self.strResultat.grid(sticky=W)

    def loadImages(self):
        imgsDir = self.imgsDir
        self.myImgsNames = os.listdir(imgsDir)
        self.imgContainer = Label(self.sectionImgs)
        baseWidth = 300

        for fileName in self.myImgsNames:

            img = Image.open(imgsDir+"/"+fileName)
            ratio = (baseWidth/float(img.size[0]))
            height = int((float(img.size[1])*float(ratio)))
            size = baseWidth, height
            img = img.resize(size, Image.ANTIALIAS)
            # photoImg = ImageTk.PhotoImage(img)


            # im = Image.open(imgsDir+"/"+fileName).thumbnail(size, Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img) # reference PhotoImage in local variable
            # img = img.zoom(25) #with 250, I ended up running out of memory

            self.imgContainer['image'] = img
            self.myImgs.append(img)

        self.displayImage()

    def displayImage(self):
        if(self.indexImg < len(self.myImgs)):
            self.imgContainer['image'] = self.myImgs[self.indexImg]  # store a reference to the image as an attribute of the widget
            self.imgContainer.grid()
        else:
            print("Aucune image restante")
            root.destroy()

    def displayCategoriesBtn(self):
        # créer les catégories par défaut
        for i in range(0,len(self.categories)):
            self.createCategory(self.categories[i], i)

    def createCategory(self, categoryName, index):
        tmpCategoryButton = Button(self.sectionCategoriesBtns, text=categoryName+" ->", command=lambda:self.addImgToCategory(categoryName))
        self.categoriesButtons.append(tmpCategoryButton)
        tmpCategoryButton.grid(row=index, column=0, pady=2)

        tmpDelButton = Button(self.sectionCategoriesBtns, text="-", command=lambda:self.deleteCategoryButton(categoryName, tmpCategoryButton, tmpDelButton))
        self.categoriesButtons.append(tmpDelButton)
        tmpDelButton.grid(row=index, column=1, pady=2)

        if not os.path.exists(categoryName):
            os.makedirs(categoryName);

    def addCustomCategoryButton(self):
        self.strResultat['text'] = ""
        input = self.optionEntry.get().lower().strip().replace("/","").replace("\\","")

        print(self.checkInputValid(input))
        errorBool, errorMsg = self.checkInputValid(input)
        if(not errorBool):
            categoryName = input
            self.categories.append(categoryName)
            index = len(self.categories)
            self.createCategory(categoryName, index)
            self.strResultat['text'] ="Succès : catégorie ajoutée"
        else:
            self.strResultat['text'] = errorMsg

    def checkInputValid(self, input):
        error = False
        errorMsg = ""
        if(not input): #test chaine vide
            error = True
            errorMsg += "Erreur : nom vide\n"

        if(input in self.categories):
            error = True
            errorMsg += "Erreur : nom de catégorie déjà existant\n"

        errorData = (error,errorMsg)
        return errorData

    def deleteCategoryButton(self, categoryName, categoryButton, delButton):
        self.categories.remove(categoryName)
        categoryButton.destroy()
        delButton.destroy()
        self.strResultat['text'] ="Succès : catégorie bien supprimée"

    def addImgToCategory(self, category):
        self.strResultat['text'] =""

        imgsDir = self.imgsDir
        # ImgNameToMove = self.myImgs[self.indexImg]['file'].split("/")[1]
        ImgExtension = "."+self.myImgsNames[self.indexImg].split(".")[-1:][0]
        ImgNameToMove = self.myImgsNames[self.indexImg].replace(ImgExtension,"")

        uniqueId = str(round(time.time()))

        originPath = imgsDir+"/"+ImgNameToMove+ImgExtension
        destPath = category+"/"+category+"_"+uniqueId+ImgExtension

        print(ImgNameToMove)
        print(ImgExtension)
        print(destPath)

        if(MOVE):
            shutil.move(originPath, destPath)
        else:
            shutil.copy(originPath, destPath)


        self.strResultat['text'] ="Succès : image ajoutée à la catégorie "+category

        self.indexImg+=1
        self.displayImage()



    def quit(self, event=None):
        sys.exit()





root = Tk()
root.minsize(width=700, height=350)
myWindow = MyWindow(root)
myWindow.grid()

myWindow.loadImages()

root.mainloop()
