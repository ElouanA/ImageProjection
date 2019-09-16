
''' Ce Programme prend en entrée une image et il la découpe de manière à ce qu'elle ne soit pas déformée lorsqu'elle est projetée sur la structure OpenGL. Pour chaque face OpenGL une petite image est coupé dans l'image d'origine. '''

###################################################################

from PIL import Image 
import os
from shutil import rmtree
import numpy as np
import pygame
from pygame.locals import *




##################################################################
image_nom = "illusion"  # Image que l'on souhaite projeter
image_format = ".jpg"
nbface = 25  # nombre de face d'un coté de la structure OpenGL  !! Nombre Impaire !!
theta=np.pi/4   # angle d'ouverture du projecteur
image = Image.open(image_nom + image_format)
im_size = image.size
carre = min(im_size[0], im_size[1])     # Définit la taille en pixel du plus grand carré que l'on peut couper dans l'image
h = 1   # taille arbitraire de la moitié d'une face OpenGL
d0 = nbface*h/np.sin(theta/2) # distance pour laquelle l'image à la même taille que la structure 3D
projecteur = (carre/2,carre/2,d0)   # Coordonnées du projecteur


''' lrd est la liste des distances suivant l'axe z des faces OpenGL. Elle est définit ici par une surface Gaussienne centrée au milieu de la structure OpenGL  '''
sigma = 0.1     # Ecrat type de la surface Gaussienne
lrd = [[-np.exp(-0.5*(((i-nbface/2)**2+(j-nbface/2)**2)/(5000*sigma**2)))/(sigma**2*2*np.pi) for i in range(nbface)] for j in range(nbface)]



##################################################################
# crée le dossier où seront enregistrer les images

if os.path.exists("./" + image_nom):
    rmtree("./" + image_nom)
    os.mkdir("./" + image_nom)
else :
    os.mkdir("./" + image_nom)



''' Pour découper l'image d'origine on la divise d'abord en quatre carré et on applique l'algorithme 
de division sur chaque carré. Cela permet de centrer la caméra au milieu de l'image et de gérer 
correctement les listes ltop et lleft.'''


##################################################################
# hypothénuse[i][j][0 ou 1] = hypothénuse de la face (i,j) suivant une ligne (0) ou une colonne (1)

hypothenuse=[[[0,0] for i in range(nbface)] for j in range(nbface)]



# calcule hypothénuse sur la colone et la ligne du milieu de l'image, pour initialiser la liste.

for k in range(0,nbface):
    hypothenuse[nbface//2][k][1] = carre/nbface
    hypothenuse[k][nbface//2][0] = carre/nbface


for k in range(nbface//2+1,nbface):
    hypothenuse[nbface//2][k][0] = np.sqrt((carre/nbface)**2+((lrd[nbface//2][k]-lrd[nbface//2][k-1])*carre/(2*d0*np.sin(theta/2)))**2)
    hypothenuse[nbface//2][k-nbface//2-1][0] = np.sqrt((carre/nbface)**2+((lrd[nbface//2][k-nbface//2-1]-lrd[nbface//2][k-nbface//2])*carre/(2*d0*np.sin(theta/2)))**2)
    
    hypothenuse[k][nbface//2][1] = np.sqrt((carre/nbface)**2+((lrd[k][nbface//2]-lrd[k-1][nbface//2])*carre/(2*d0*np.sin(theta/2)))**2)
    hypothenuse[k-nbface//2-1][nbface//2][1] = np.sqrt((carre/nbface)**2+((lrd[k-nbface//2-1][nbface//2]-lrd[k-nbface//2][nbface//2])*carre/(2*d0*np.sin(theta/2)))**2)



# Calcule de l'hypothénuse sur les autres faces.
# carré en bas à droite
for i in range (nbface//2+1,nbface):
    for j in range(nbface//2+1,nbface):
        hypothenuse[i][j][0] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i][j-1])*carre/(2*d0*np.sin(theta/2)))**2)
        hypothenuse[i][j][1] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i-1][j])*carre/(2*d0*np.sin(theta/2)))**2)
    
    
# carré en bas à gauche
for i in range (nbface//2+1,nbface):
    for j in range(0,nbface//2):
        hypothenuse[i][j][0] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i][j+1])*carre/(2*d0*np.sin(theta/2)))**2)
        hypothenuse[i][j][1] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i-1][j])*carre/(2*d0*np.sin(theta/2)))**2)
    

# carré en haut à droite
for i in range (0,nbface//2):
    for j in range(nbface//2+1,nbface):
        hypothenuse[i][j][0] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i][j-1])*carre/(2*d0*np.sin(theta/2)))**2)
        hypothenuse[i][j][1] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i+1][j])*carre/(2*d0*np.sin(theta/2)))**2)
    
    
# carré en haut à gauche
for i in range (0,nbface//2):
    for j in range(0,nbface//2):
        hypothenuse[i][j][0] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i][j+1])*carre/(2*d0*np.sin(theta/2)))**2)
        hypothenuse[i][j][1] = np.sqrt((carre/nbface)**2+((lrd[i][j]-lrd[i+1][j])*carre/(2*d0*np.sin(theta/2)))**2)
        




##################################################################
# taillelacet[0 ou 1][i] = taille du lacet suivant la ième ligne (0) ou la ième colonne (1)

taillelacet = [[0 for i in range(nbface)] for j in range(2)]

for k in range(nbface):
    taillelacet[0][k] = sum(hypothenuse[k][l][0] for l in range(nbface))
    taillelacet[1][k] = sum(hypothenuse[l][k][1] for l in range(nbface))
    
    
    


##################################################################
# listes de top et de left. (top, left) sont les coordonnées du coin supérieur gauche de chaque petite image coupé dans l'image d'origine. Les listes sont remplis au fur et à mesures que les petites images sont coupées.

ltop = [[0 for i in range(nbface)] for j in range(nbface)]
lleft = [[0 for i in range(nbface)] for j in range(nbface)]


for k in range(nbface):
    ltop[nbface//2][k] = carre/2
    lleft[k][nbface//2] = carre/2




##################################################################
#Découpe des petites images en partant du centre de l'image :

# Carré en bas à droite

for i in range(nbface//2,nbface):
    for j in range(nbface//2,nbface):
        
        distance= projecteur[2]-lrd[i][j]
        
        height = d0*hypothenuse[i][j][1]/(distance)
        width = d0*hypothenuse[i][j][0]/(distance)
        left = lleft[i][j]
        top = ltop[i][j]
        
        if i<nbface-1:
            ltop[i+1][j] = top + height
        
        if j<nbface-1:
            lleft[i][j+1] = left + width
        
        box = (left, top, left+width, top+height)
        area = image.crop(box)
        area.save("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)
        
    


# Carré en bas à gauche

for i in range(nbface//2,nbface):
    for j in range(nbface//2-1, -1, -1):
        
        distance= projecteur[2]-lrd[i][j]
        
        height = d0*hypothenuse[i][j][1]/(distance)
        width = d0*hypothenuse[i][j][0]/(distance)
        left = lleft[i][j+1] - width
        top = ltop[i][j]
        
        if i<nbface-1:
            ltop[i+1][j] = top + height

        lleft[i][j] = left
        
        box = (left, top, left+width, top+height)
        area = image.crop(box)
        area.save("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)



# Carré en haut à droite

for i in range(nbface//2-1, -1, -1):
    for j in range(nbface//2,nbface):
        
        distance= projecteur[2]-lrd[i][j]
        
        height = d0*hypothenuse[i][j][1]/(distance)
        width = d0*hypothenuse[i][j][0]/(distance)
        left = lleft[i][j]
        top = ltop[i+1][j] - height
        

        ltop[i][j] = top
        
        if j<nbface-1:
            lleft[i][j+1] = left + width
        
        box = (left, top, left+width, top+height)
        area = image.crop(box)
        area.save("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)



# Carré en haut à gauche

for i in range(nbface//2-1, -1, -1):
    for j in range(nbface//2-1, -1, -1):
        
        distance= projecteur[2]-lrd[i][j]
        
        height = d0*hypothenuse[i][j][1]/(distance)
        width = d0*hypothenuse[i][j][0]/(distance)
        left = lleft[i][j+1] - width
        top = ltop[i+1][j] - height
        

        ltop[i][j] = top
        
        lleft[i][j] = left 
        
        box = (left, top, left+width, top+height)
        area = image.crop(box)
        area.save("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)





# Définition des images à mettre sur les faces perpendiculaires. 
# Pour les faces perpendiculaires, on part des faces adjacentes et on "recolle" les cotés

for i in range(nbface):
    for j in range(nbface):
        
        # face dessus
        if i>0 and lrd[i-1][j]-lrd[i][j]<0 :
            im1 = Image.open("./" + image_nom + "/" + str(i-1) + "-" + str(j) + image_format)
            im2 = Image.open("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)
            
            im1 = im1.crop((0, im1.size[1]-1, im1.size[0], im1.size[1]))
            im2 = im2.crop((0, 0, im2.size[0], 1))
            
            new_im = Image.new('RGB', (min(im1.size[0],im2.size[0]), im1.size[1]+im2.size[1]))
            new_im.paste(im1, (0,0))
            new_im.paste(im2, (0,im1.size[1]))
            new_im.save("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(0) + image_format)
            
            
        # face dessous
        if i<nbface-1 and lrd[i+1][j]-lrd[i][j]<0:
            im1 = Image.open("./" + image_nom + "/" + str(i+1) + "-" + str(j) + image_format)
            im2 = Image.open("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)
            
            im2 = im2.crop((0, im2.size[1]-1, im2.size[0], im2.size[1]))
            im1 = im1.crop((0, 0, im1.size[0], 1))
            
            new_im = Image.new('RGB', (min(im1.size[0],im2.size[0]), im1.size[1]+im2.size[1]))
            new_im.paste(im2, (0,0))
            new_im.paste(im1, (0,im2.size[1]))
            new_im = new_im.rotate(90, expand=True)
            new_im.save("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(1) + image_format)
            
            
        # face de droite
        if j<nbface-1 and lrd[i][j+1]-lrd[i][j]<0:
            im1 = Image.open("./" + image_nom + "/" + str(i) + "-" + str(j+1) + image_format)
            im2 = Image.open("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)
            
            im2 = im2.crop((im2.size[0]-1, 0, im2.size[0], im2.size[1]))
            im1 = im1.crop((0, 0, 1, im1.size[1]))
            
            new_im = Image.new('RGB', (im2.size[0]+im1.size[0], min(im2.size[1],im1.size[1])))
            new_im.paste(im2, (0,0))
            new_im.paste(im1, (im2.size[0],0))
            new_im = new_im.rotate(-90, expand=True)
            new_im.save("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(2) + image_format)   
             
            
        # face de gauche
        if j>0 and lrd[i][j-1]-lrd[i][j]<0:
            im1 = Image.open("./" + image_nom + "/" + str(i) + "-" + str(j-1) + image_format)
            im2 = Image.open("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format)
            
            im1 = im1.crop((im1.size[0]-1, 0, im1.size[0], im1.size[1]))
            im2 = im2.crop((0, 0, 1, im2.size[1]))
            
            new_im = Image.new('RGB', (im2.size[0]+im1.size[0], min(im2.size[1],im1.size[1])))
            new_im.paste(im1, (0,0))
            new_im.paste(im2, (im2.size[0],0))
            new_im = new_im.rotate(-90, expand=True)
            new_im.save("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(3) + image_format)
            
            
            
            
            
            
            
            
            
            






    
