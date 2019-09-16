
''' Ce Programme permet de générer une structure OpenGL et de mapper des images dessus
Il est possible de déplacer la caméra en utilisant les touches i,j,k,l et de faire tourner la caméra en utilisant les flèches. Il est également possible de zoomer avec les touches b,h ou avec la molette de la souris '''




##################################################################

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random as rd
import pygame
from pygame.locals import *
from openmesh import *
from PIL import Image



#################################################################
# Définition des paramètres

path_to_object = "predi_voiture1.obj"   # chemin vers un objet .obj qui peut être utilisé structure 3D  
image_nom = "illusion"  # Image que l'on souhaite projeter
image_format = ".jpg"
nbface = 25  # nombre de face d'un coté de la structure OpenGL  !! Nombre Impaire !!

image = Image.open(image_nom + image_format)
im_size = image.size
carre = min(im_size[0], im_size[1])     # Définit la taille en pixel du plus grand carré que l'on peut couper dans l'image
h = 1   # taille arbitraire de la moitié d'une face OpenGL
theta=np.pi/4   # Angle d'ouverture de la caméra
d0 = nbface*h/np.sin(theta/2)   # Distance à laquel l'image projeté par la caméra est de taille 2*h*nbface, cela correspond à la taille totale de la structure 3D
projecteur = (nbface*h,nbface*h,d0)   # Coordonnées du projecteur 


''' lrd est la liste des distances suivant l'axe z des faces OpenGL. Elle est définit ici par une surface Gaussienne centrée au milieu de la structure OpenGL  '''
sigma = 0.1     # Ecrat type de la surface Gaussienne
lrd = [[-np.exp(-0.5*(((i-nbface/2)**2+(j-nbface/2)**2)/(5000*sigma**2)))/(sigma**2*2*np.pi) for i in range(nbface)] for j in range(nbface)]


#################################################################
# Définit une liste de points correspondant aux voxels d'un objet 

def points(path_to_object):
    
    object = read_polymesh(path_to_object)

    i = 0
    lcube = []
    
    d=1/(object.points()[2][1]-object.points()[1][1])
    
    for fc in object.points():
        if i%8==0:
            lcube.append([x*d for x in fc])
        i+=1
    
    return lcube



#################################################################
# Les fonctions suivantes permettent de créer des objets OpenGL et de les placer à la position (x,y,z). h est la taille de la moitié d'une face, définit au début du fichier.


# Crée une face 
def face_devant(x,y,z):
    glBegin(GL_QUADS)
    
    glColor3f(255,255,255)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-h+x, -h+y, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-h+x,  h+y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(h+x,  h+y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(h+x, -h+y, z)
    
    glEnd()




# Place un carre perpendiculaire à une face de devant :
def face_dessous(x,y,z,p):
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-h+x,  -h+y, p+z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-h+x, -h+y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(h+x,  -h+y, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(h+x, -h+y, p+z)
    
    glEnd()


def face_dessus(x,y,z,p):
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-h+x,  h+y, p+z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-h+x, h+y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(h+x,  h+y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(h+x, h+y, p+z)
    
    glEnd()
    
    
def face_droite(x,y,z,p):
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3f(h+x,  -h+y, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(h+x, -h+y, p+z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(h+x,  h+y, p+z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(h+x, h+y, z)
    
    glEnd()
    

def face_gauche(x,y,z,p):
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-h+x,  -h+y, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-h+x, -h+y, p+z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-h+x,  h+y, p+z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-h+x, h+y, z)
    
    glEnd()


# Place un cube à la position (x,y,z) h est la taille de la moitié d'un carré. Ce Cube permet de représenter le projecteur
def Cube(x,y,z):
    glBegin(GL_QUADS)
    
    glColor3f(1,0,0)
    glNormal3f(0,0,-h)
    glVertex3f( -h+x, -h+y, z)
    glVertex3f(  h+x, -h+y, z)
    glVertex3f(  h+x,  h+y, z)
    glVertex3f( -h+x,  h+y, z)
    
    glNormal3f(0,0,h)
    glVertex3f( -h+x, -h+y,  2*h+z)
    glVertex3f(  h+x, -h+y,  2*h+z)
    glVertex3f(  h+x,  h+y,  2*h+z)
    glVertex3f( -h+x,  h+y,  2*h+z)
    
    glNormal3f(0,-h,0) 
    glVertex3f( -h+x, -h+y, z)
    glVertex3f(  h+x, -h+y, z)
    glVertex3f(  h+x, -h+y, 2*h+z)
    glVertex3f( -h+x, -h+y, 2*h+z)
    
    glNormal3f(0,h,0)
    glVertex3f( -h+x,  h+y, z)
    glVertex3f(  h+x,  h+y, z)
    glVertex3f(  h+x,  h+y, 2*h+z)
    glVertex3f( -h+x,  h+y, 2*h+z)
        
    glNormal3f(-h,0,0) 
    glVertex3f( -h+x, -h+y, z)
    glVertex3f( -h+x,  h+y, z)
    glVertex3f( -h+x,  h+y, 2*h+z)
    glVertex3f( -h+x, -h+y, 2*h+z)                      
    
    glNormal3f(h,0,0)   
    glVertex3f(  h+x, -h+y, z)
    glVertex3f(  h+x,  h+y, z)
    glVertex3f(  h+x,  h+y, 2*h+z)
    glVertex3f(  h+x, -h+y, 2*h+z)

    glEnd()
    
    
# crée un triangle dont une des somments est à la position (x,y,z). Le triange permet de visualiser l'angle d'ouverture du projecteur.
def Triangle(x,y,z):
    glBegin(GL_TRIANGLES)
    glColor3f(1,0,0)
    glVertex3f( x, y, z)
    glVertex3f(  x-3*h*np.sin(theta/2), y, z-3*h*np.cos(theta/2))
    glVertex3f(  x+3*h*np.sin(theta/2), y, z-3*h*np.cos(theta/2))
    glEnd()




#################################################################
# Construit la liste des faces perpendiculaires à afficher. Ordre des faces dans le vecteur : dessus , dessous , droite , gauche

def face_perpendiculaires(lrd):
    s = []
    for i in range(nbface):
        tmp1 = []
        for j in range(nbface):
            tmp2 = [0,0,0,0]
            if i>0 and lrd[i-1][j]-lrd[i][j]<0 :
                tmp2[0] = lrd[i-1][j]-lrd[i][j]
                
            if i<nbface-1 and lrd[i+1][j]-lrd[i][j]<0:
                tmp2[1] = lrd[i+1][j]-lrd[i][j]
                
            if j<nbface-1 and lrd[i][j+1]-lrd[i][j]<0:
                tmp2[2] = lrd[i][j+1]-lrd[i][j]
                
            if j>0 and lrd[i][j-1]-lrd[i][j]<0:
                tmp2[3] =  lrd[i][j-1]-lrd[i][j]
            tmp1.append(tmp2)
        s.append(tmp1)
            
    return s
    
fp = face_perpendiculaires(lrd)



#################################################################
# Charge une image 

def loadTexture(texture_path):
    textureSurface = pygame.image.load(texture_path)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    return [glGenTextures(1),textureData,width,height]
    
    





#################################################################
# La fonction main initialise la fenetre pygame et contient la boucle infinie qui permet de représenter la structure OpenGL


def main():
    
    # Initialisation de Pygame 
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    
    # Crée la liste des images à projeter sur les faces de devant
    textures = []
    
    for i in range(nbface):
        tmp = []
        
        for j in range(nbface):
            tmp.append(loadTexture("./" + image_nom + "/" + str(i) + "-" + str(j) + image_format))

        textures.append(tmp)
    
    
    # Crée la liste des images à projeter sur les faces perpendiculaires
    
    textures_p = []
    
    for i in range(nbface):
        for j in range(nbface):
            tmp = [0,0,0,0]
            
            if fp[i][j][0] != 0:
                tmp[0] = loadTexture("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(0) + image_format)
            
            if fp[i][j][1] != 0:
                tmp[1] = loadTexture("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(1) + image_format)
            
            if fp[i][j][2] != 0:
                tmp[2] = loadTexture("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(2) + image_format)
                
            if fp[i][j][3] != 0:
                tmp[3] = loadTexture("./" + image_nom + "/" + str(i) + "-" + str(j) + "-" + str(3) + image_format)
        
            textures_p.append(tmp)
    
    
    
    # Définit la fenêtre d'observation
    gluPerspective(45, (display[0]/display[1]), 0.1, 5000.0)
    glTranslatef(-nbface*h,nbface*h,-20)

    
    # Boucle infinie qui permet de représenter la structure OpenGL
    
    while True:

        # Modification de la fenêtre d'observation : translations, rotations.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(5,0,1,0)
                    
                if event.key == pygame.K_RIGHT:
                    glRotatef(5,0,-1,0)

                if event.key == pygame.K_UP:
                    glRotate(5,1,0,0)
                    
                if event.key == pygame.K_DOWN:
                    glRotate(5,-1,0,0)
                
                if event.key == pygame.K_i:
                    glTranslatef(0,h/2,0)
                
                if event.key == pygame.K_k:
                    glTranslatef(0,-h/2,0)
                    
                if event.key == pygame.K_j:
                    glTranslatef(-h/2,0,0)
                
                if event.key == pygame.K_l:
                    glTranslatef(h/2,0,0)
                
                if event.key == pygame.K_b:
                    glTranslatef(0,0,-h)
                
                if event.key == pygame.K_h:
                    glTranslatef(0,0,h)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,2)

                if event.button == 5:
                    glTranslatef(0,0,-2)
                    
        
        
        # Efface le Buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        

        # Crée les faces OpenGL et affiche l'image sur les faces correspondantes.
        
        for i in range(nbface):
            for j in range(nbface):
                
                # Faces de devant 
                
                glBindTexture(GL_TEXTURE_2D, textures[i][j][0])
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textures[i][j][2], textures[i][j][3],
                    0, GL_RGBA, GL_UNSIGNED_BYTE, textures[i][j][1])
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                
                face_devant(2*h*j,-2*h*i,lrd[i][j])
                
                
                
                # faces perpendiculaires 
                
                if fp[i][j][0] != 0 :
                    
                    glBindTexture(GL_TEXTURE_2D, textures_p[i*nbface+j][0][0])
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textures_p[i*nbface+j][0][2], textures_p[i*nbface+j][0][3],
                        0, GL_RGBA, GL_UNSIGNED_BYTE, textures_p[i*nbface+j][0][1])
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                    
                    face_dessus(2*h*j,-2*h*i,lrd[i][j],fp[i][j][0])
                    
    
                if fp[i][j][1] != 0:
                    
                    glBindTexture(GL_TEXTURE_2D, textures_p[i*nbface+j][1][0])
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textures_p[i*nbface+j][1][2], textures_p[i*nbface+j][1][3],
                        0, GL_RGBA, GL_UNSIGNED_BYTE, textures_p[i*nbface+j][1][1])
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                    
                    face_dessous(2*h*j,-2*h*i,lrd[i][j],fp[i][j][1])
                    
                
                if fp[i][j][2] != 0:
                    
                    glBindTexture(GL_TEXTURE_2D, textures_p[i*nbface+j][2][0])
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textures_p[i*nbface+j][2][2], textures_p[i*nbface+j][2][3],
                        0, GL_RGBA, GL_UNSIGNED_BYTE, textures_p[i*nbface+j][2][1])
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                    
                    face_droite(2*h*j,-2*h*i,lrd[i][j],fp[i][j][2])
                    
                    
                if fp[i][j][3] != 0:
                    
                    glBindTexture(GL_TEXTURE_2D, textures_p[i*nbface+j][3][0])
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textures_p[i*nbface+j][3][2], textures_p[i*nbface+j][3][3],
                        0, GL_RGBA, GL_UNSIGNED_BYTE, textures_p[i*nbface+j][3][1])
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                    
                    face_gauche(2*h*j,-2*h*i,lrd[i][j],fp[i][j][3])
                    
        
        # Représente le projecteur 
        Cube(projecteur[0], -projecteur[1], projecteur[2])
        Triangle(projecteur[0], -projecteur[1], projecteur[2])
        
        # Affichage pygame
        pygame.display.flip()
        pygame.time.wait(5)




# Exécution de la fonction main()
main()
