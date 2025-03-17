#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#%% SECTION 1 inclusion de packages externes 


import numpy as np
import platform
import tempfile
import os
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
# necessite scikit-image 
from skimage import io as skio


#%% SECTION 2 fonctions utiles pour le TP

def viewimage(im,normalise=True,MINI=0.0, MAXI=255.0):
    """ Cette fonction fait afficher l'image EN NIVEAUX DE GRIS 
        dans gimp. Si un gimp est deja ouvert il est utilise.
        Par defaut normalise=True. Et dans ce cas l'image est normalisee 
        entre 0 et 255 avant d'être sauvegardee.
        Si normalise=False MINI et MAXI seront mis a 0 et 255 dans l'image resultat
        
    """
    imt=np.float32(im.copy())
    if platform.system()=='Darwin': #on est sous mac
        prephrase='open -a GIMP '
        endphrase=' ' 
    elif platform.system()=='Windows': 
        #ou windows ; probleme : il faut fermer gimp pour reprendre la main; 
        #si vous savez comment faire (commande start ?) je suis preneur 
        prephrase='"C:/Program Files/GIMP 2/bin/gimp-2.10.exe" '
        endphrase=' '
    else: #SINON ON SUPPOSE LINUX (si vous avez un windows je ne sais pas comment faire. Si vous savez dites-moi.)
        prephrase='gimp '
        endphrase= ' &'
    
    if normalise:
        m=im.min()
        imt=imt-m
        M=imt.max()
        if M>0:
            imt=255*imt/M

    else:
        imt=(imt-MINI)/(MAXI-MINI)
        imt[imt<0]=0
        imt[imt>1]=1
        imt *= 255
    
    nomfichier=tempfile.mktemp('TPIMA.png')
    commande=prephrase +nomfichier+endphrase
    imt = imt.astype(np.uint8)
    skio.imsave(nomfichier,imt)
    os.system(commande)

def viewimage_color(im,normalise=True,MINI=0.0, MAXI=255.0):
    """ Cette fonction fait afficher l'image EN COULEURS
        dans gimp. Si un gimp est deja ouvert il est utilise.
        Par defaut normalise=True. Et dans ce cas l'image est normalisee 
        entre 0 et 255 avant d'être sauvegardee.
        Si normalise=False MINI(defaut 0) et MAXI (defaut 255) seront mis a 0 et 255 dans l'image resultat
        
    """
    imt=np.float32(im.copy())
    if platform.system()=='Darwin': #on est sous mac
        prephrase='open -a GIMP '
        endphrase= ' '
    elif platform.system()=='Windows': 
        #ou windows ; probleme : il faut fermer gimp pour reprendre la main; 
        #si vous savez comment faire (commande start ?) je suis preneur 
        prephrase='"C:/Program Files/GIMP 2/bin/gimp-2.10.exe" '
        endphrase=' '
    else: #SINON ON SUPPOSE LINUX (si vous avez un windows je ne sais comment faire. Si vous savez dites-moi.)
        prephrase='gimp '
        endphrase=' &'
    
    if normalise:
        m=imt.min()
        imt=imt-m
        M=imt.max()
        if M>0:
            imt=255*imt/M
    else:
        imt=(imt-MINI)/(MAXI-MINI)
        imt[imt<0]=0
        imt[imt>1]=1
        imt *= 255
    
    nomfichier=tempfile.mktemp('TPIMA.pgm')
    commande=prephrase +nomfichier+endphrase
    imt = imt.astype(np.uint8)
    skio.imsave(nomfichier,imt)
    os.system(commande)

def noise(im,br):
    """ Cette fonction ajoute un bruit blanc gaussier d'ecart type br
       a l'image im et renvoie le resultat"""
    imt=np.float32(im.copy())
    sh=imt.shape
    bruit=br*np.random.randn(*sh)
    imt=imt+bruit
    return imt

def quantize(im,n=2):
    """
    Renvoie une version quantifiee de l'image sur n (=2 par defaut) niveaux  
    """
    imt=np.float32(im.copy())
    if np.floor(n)!= n or n<2:
        raise Exception("La valeur de n n'est pas bonne dans quantize")
    else:
        m=imt.min()
        M=imt.max()
        imt=np.floor(n*((imt-m)/(M-m)))*(M-m)/n+m
        imt[imt==M]=M-(M-m)/n #cas des valeurs maximales
        return imt
    

def seuil(im,s):
    """ renvoie une image blanche(255) la ou im>=s et noire (0) ailleurs.
    """
    imt=np.float32(im.copy())
    mask=imt<s
    imt[mask]=0
    imt[~mask]=255
    return imt

def gradx(im):
    "renvoie le gradient dans la direction x"
    imt=np.float32(im)
    gx=0*imt
    gx[:,:-1]=imt[:,1:]-imt[:,:-1]
    return gx

def grady(im):
    "renvoie le gradient dans la direction y"
    imt=np.float32(im)
    gy=0*imt
    gy[:-1,:]=imt[1:,:]-imt[:-1,:]
    return gy

def view_spectre(im,option=1,hamming=False):
    """ affiche le spectre d'une image
     si option =1 on affiche l'intensite de maniere lineaire
     si option =2 on affiche le log
     si hamming=True (defaut False) alors une fenetre de hamming est appliquee avant de prendre la transformee de Fourier
     """
    imt=np.float32(im.copy())
    (ty,tx)=im.shape
    pi=np.pi
    if hamming:
        XX=np.ones((ty,1))@(np.arange(0,tx).reshape((1,tx)))
        YY=(np.arange(0,ty).reshape((ty,1)))@np.ones((1,tx))
        imt=(1-np.cos(2*pi*XX/(tx-1)))*(1-np.cos(2*pi*YY/(ty-1)))*imt
    aft=np.fft.fftshift(abs(np.fft.fft2(imt)))
    
    if option==1:
        viewimage(aft)
    else:
        viewimage(np.log(0.1+aft))


def filterlow(im): 
    """applique un filtre passe-bas parfait a une image (taille paire)"""
    (ty,tx)=im.shape
    imt=np.float32(im.copy())
    pi=np.pi
    XX=np.concatenate((np.arange(0,tx/2+1),np.arange(-tx/2+1,0)))
    XX=np.ones((ty,1))@(XX.reshape((1,tx)))
    
    YY=np.concatenate((np.arange(0,ty/2+1),np.arange(-ty/2+1,0)))
    YY=(YY.reshape((ty,1)))@np.ones((1,tx))
    mask=(abs(XX)<tx/4) & (abs(YY)<ty/4)
    imtf=np.fft.fft2(imt)
    imtf[~mask]=0
    return np.real(np.fft.ifft2(imtf))

def filtergauss(im):
    """applique un filtre passe-bas gaussien. coupe approximativement a f0/4"""
    (ty,tx)=im.shape
    imt=np.float32(im.copy())
    pi=np.pi
    XX=np.concatenate((np.arange(0,tx/2+1),np.arange(-tx/2+1,0)))
    XX=np.ones((ty,1))@(XX.reshape((1,tx)))
    
    YY=np.concatenate((np.arange(0,ty/2+1),np.arange(-ty/2+1,0)))
    YY=(YY.reshape((ty,1)))@np.ones((1,tx))
    # C'est une gaussienne, dont la moyenne est choisie de sorte que
    # l'integrale soit la meme que celle du filtre passe bas
    # (2*pi*sig^2=1/4*x*y (on a suppose que tx=ty))
    sig=(tx*ty)**0.5/2/(pi**0.5)
    mask=np.exp(-(XX**2+YY**2)/2/sig**2)
    imtf=np.fft.fft2(imt)*mask
    return np.real(np.fft.ifft2(imtf))
#%% SECTION 3 exemples de commandes pour effectuer ce qui est demande pendant le TP
    
#%% charger une image 
im=skio.imread('images/maison.tif')

# connaitre la taille de l'image
im.shape

#avoir la valeur d'un pixel
im[9,8] #pixel en y=9 et x=8

# visualiser l'image (en niveaux de gris)
viewimage(im)
# afficher une ligne d'une image comme un signal 
# par exemple on affiche la ligne y=129


plt.plot(im[129,:])
# colonne x=45
plt.plot(im[:,45])

# maximum d'une image
im.max()
# minimum
im.min()
#minimum d'une ligne
im[129,:].min()

# transformation en image a valeurs reelles
imfloat= np.float32(im)
# valeur absolue d'une image
abs(im)
# pour obtenir de l'aide 
help(quantize)
# transformerun tableau en une line
r=im.reshape( ( -1,))
print (r.shape)
# %% Que fait gimp pour afficher l'image en plus grand?

# Gimp augmente la taille de chaque pixel dans l'écran de l'ordinateur. Si chaque pixel de l'image apparaît comme 4 pixel de l'écran, l'image sera plus grand
# %% Ouvrir maison_petit.tif

im = skio.imread("images/maison-petit.tif")
viewimage(im)

# %% Quelle hypothèse pouvez-vous faire sur la génération de maison_petit.tif?

# Il me semble que le méthode d'interpolation a été le responsable de la difference entre les deux images.
#%% une image couleur 
im=skio.imread('images/fleur.tif')
viewimage_color(im,normalise=False) #on ne normalise pas pour garder l'image comme
                                    # a l'origine
# voir un seul canal (rouge)
viewimage(im[:,:,0])
viewimage(im.mean(axis=2)) #la moyenne des trois canaux
# %% omprenez-vous pourquoi les deux positions extrêmes de ce boutons font, en fait, la même transformation?

# Parce que le spectre de la tente est circulaire. C'est-à-dire que une tente de -180° est égal à une tente de 180°.
# %% A quoi correspond la saturation (essayez-100% et +100%)?

# La saturation corresponde à la puissance de la tente. Une saturarion -100% signifie une puissance nulle de couleurs, i.e., une image sans couleurs (en gris).
#%%
#histogrammes
# simple visualisation
im=skio.imread('images/maison.tif')
plt.hist(im.reshape((-1,)),bins=255) #le reshape transforme en tableau 1D
#%%
#calcul d'un histogramme cumule
(histo,bins)=np.histogram(im.reshape((-1,)),np.arange(0,256)) #le reshape est inutile pour np.histogram, mais on le laisse pour la compatibilite avec plt.hist
histo=histo/histo.sum()
histocum=histo.cumsum()
plt.plot(histocum)

#%% ajout de bruit 
imbr=noise(im,10)
viewimage_color(imbr,normalise=False)
#effet sur l'histogramme
plt.hist(im.reshape((-1,)),255)
plt.show()
plt.hist(imbr.reshape((-1,)),255)
plt.show()
# %% Ouvrir une image pour cahngement de contraste

im = skio.imread('images/bat.tif')
viewimage(im)
# %% En considérant les niveaux de gris d'une image comme la réalisation d'une variable aléatoire dont la loi est l'histogramme de l'image, interprétez le résultat.

# L'application d'un filtre de bruit gaussian a fait la distribuition de probabilités plus lisse. Les points où la plupart des gris était dans l'image original sont encore les plus probables, mais la transition entre les pics montre plus de gris.
# %% L'aspect global de l'image est-il modifié par l'application de fonctions croissantes ?

# Le contraste change, mais l'aspect global reste le même.
# %% Que se passe-t-il si l'on applique une transformation non-croissante des niveaux de gris?

# Une transformation non-croissante fait apparaître des régions très sombres. Il me semble que quelques informations sont perdues à cause de ce sombrissement.

#%% egalisation d'histogramme
im=skio.imread('images/sombre.jpg')
im=im.mean(axis=2) #on est sur que l'image est en niveaux de gris
viewimage(im)
(histo,bins)=np.histogram(im.reshape((-1,)),np.arange(0,256)) #le reshape en inutile pour np.histogram, mais on le laisse pour la compatibilite avec plt.hist
histo=histo/histo.sum()
histocum=histo.cumsum()
imequal=histocum[np.uint8(im)]
viewimage(imequal)
# %% Plot hist and cumm hist


plt.hist(im.reshape((-1,)),255)
plt.show()

(histo,bins)=np.histogram(im.reshape((-1,)),np.arange(0,256)) #le reshape est inutile pour np.histogram, mais on le laisse pour la compatibilite avec plt.hist
histo=histo/histo.sum()
histocum=histo.cumsum()
plt.plot(histocum)
plt.show()

# %%

imequal *= 255

plt.hist(imequal.reshape((-1,)),255)
plt.show()


(histo,bins)=np.histogram(imequal.reshape((-1,)),np.arange(0,256)) #le reshape est inutile pour np.histogram, mais on le laisse pour la compatibilite avec plt.hist
histo=histo/histo.sum()
histocum=histo.cumsum()
plt.plot(histocum)
plt.show()

# %% Qu'observez-vous sur imequal, sur son histogramme et sur son histogramme cumulé

# L'histogramme de imequal est beaucoup plus distribué que celle de im. La plupart des tons de gris étaient près du 0 e, maintenant, sont égalements distribués. Cette transformation peut être vu par l'histogramme cummulé, vu qu'il semble vraiment une ligne y = x. Ça montre que les tons sont plus ou moins bien distribués.

#%% 
u=skio.imread('images/vue1.tif')
v=skio.imread('images/vue2.tif')
viewimage(u)
viewimage(v)
viewimage(abs(np.float32(u)-np.float32(v)))
# %%
# TEXTE1 dans le texte du tp
ind=np.unravel_index(np.argsort(u, axis=None), u.shape) #unravel donne les index 2D a partir des index 1d renvoyes par argsort (axis=None)
unew=np.zeros(u.shape,u.dtype)
unew[ind]=np.sort(v,axis=None)
viewimage(unew) #u avec l'histogramme de v

#DE MANIERE EQUIVALENTE et Peut-etre plus claire

ushape=u.shape
uligne=u.reshape((-1,)) #transforme en ligne
vligne=v.reshape((-1,))
ind=np.argsort(uligne)
unew=np.zeros(uligne.shape,uligne.dtype)
unew[ind]=np.sort(vligne)
# on remet a la bonne taille
unew=unew.reshape(ushape)
viewimage(unew)


viewimage(abs(np.float32(unew)-np.float32(v)))
# %% Visualisez la valeur absolue de la différence des images, qu'observe-t-on. Même question après avoir donné à l'une des images l'histogramme de l'autre.

# La différence entre les deux images originaux est très notable. Presque tous les pixels ont un niveau de gris differente et, donc, leur difference est très evidant.
# Après avoir donné l'histogram de u à v, les deux images deviennent presque identiques. Leur difference absolute est quasiment totalement noir, parce que la difference est très petite.
# %% A-t-on un moyen plus simple d'obtenir le même résultat (donner le même histogramme aux deux images) ?

# Nous pourrions changer le méthode de quantization de l'image plus claire. Si on exige que plus de photons soient détectés pour avoir le même ton de gris que l'image plus sombre, les histogrammes seront plus prôches.
# %% Donnez un code simple permettant d'égaliser l'histogramme d'une image (

u=skio.imread('images/vue1.tif')
v = np.random.rand(*u.shape) * 255

viewimage(u)
viewimage(v)

ind=np.unravel_index(np.argsort(u, axis=None), u.shape) #unravel donne les index 2D a partir des index 1d renvoyes par argsort (axis=None)
unew=np.zeros(u.shape,u.dtype)
unew[ind]=np.sort(v,axis=None)

viewimage(unew)
#%% quantification dithering 

im=skio.imread('images/maison.tif')
im2=quantize(im,2)
viewimage(im2)

viewimage(seuil(noise(im,40),128)) #exemple de dithering
# %% Appliquez le même seuillage à une version bruitée de l'image originale et visualisez. Que constatez vous?

im=skio.imread('images/maison.tif')
# viewimage(im)
viewimage(seuil(im, 128))

im = np.float32(im)
im += np.random.rand(*im.shape) * 30
viewimage(seuil(im, 128))

# Le seuillage après le bruit donne une impression meilleure. Il est possible de voir plus d'information avec le bruit. La concentration des pixels noires donne l'impression de differentes tons de gris.
# %% En considérant un pixel de niveau x dans l'image initiale, donnez la probabilité pour que ce pixel soit blanc après ajout de bruit et seuillage. 

# P(x + N > 128) = P(N > 128 - x) = \int_{128 - x}^{\infty} f(t) dt
# %% Pourquoi l'image détramée ressemble-t-elle plus à l'image de départ que l'image simplement seuillée?

# La probabilité d'un pixel d'être blanc est proportionelle à son ton de gris. Ainsi, les plus claires regions d'image originale deviennent les régions où il y a beaucoup de pixels blanches. Le même c'est vrai pour les régions plus sombres.

#%% log d'un histogramme
im=skio.imread('images/maison.tif')
gdx = gradx(im)
gdx = gdx.flatten()

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(gdx, bins=255, color='blue', alpha=0.7)
plt.subplot(1, 2, 2)
plt.plot(np.log(np.histogram(gdx, 255)[0]))
plt.tight_layout()
plt.show()
# %% La distribution des différences vous semble-t-elle obéir a une loi gaussienne ? Pourquoi ?

# 

#%%
im=skio.imread('images/carte_nb.tif')
viewimage(im)
view_spectre(im,option=2,hamming=True)

im=skio.imread('images/amiens1.tif')
viewimage(im)
view_spectre(im,option=2,hamming=True)
#%% FIN TP INTRODUCTION

viewimage(im)

imf = filterlow(im)
viewimage(imf)
view_spectre(imf,option=2,hamming=True)

imf = filtergauss(im)
viewimage(imf)
view_spectre(imf,option=2,hamming=True)