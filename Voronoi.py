from math import *
from tkinter import *

Width=600
Height=600

addPointMode = 1
listePoint = [] #liste sites
listeCentre = [] # liste centre des cercles inscrits
listeBord = [] # liste points au bord du cadre
listePointFlotant = [] # les coordoné d'un point en déplacement
enClick=0

##click
def click(event):
    global listePoint
    global enClick
    x,y=event.x,event.y
    #print(addPointMode)
    if(addPointMode==1):
        cnv.create_rectangle(x-2, y-2, x+2, y+2, fill='red')
        listePoint.append([x,y])
        clearL()
        if (len(listePoint)>1):
            calcul()
    else:
        enClick=1


##bouge
def bouge(event):
    global listePointFlotant
    global listePoint
    if (addPointMode==0) and (enClick==1):
        x,y = event.x , event.y
        #c la ou tu va mettre le changement de point, comnece par la distance souris/point dans listePoint
        minD=300
        T=30
        for i in range(len(listePoint)):
            a=listePoint[i]
            distance= sqrt((x-a[0])**2 + (y-a[1])**2)
            if (distance<=minD):
                minD=distance
                pt=i
        if (minD<=T):
            a=listePoint[pt]
            a[0]=x
            a[1]=y
            clearL()
            calcul()


##unclick
def unclick(event) :
    global enClick
    enClick=0


##clear
def clear():
    global listePoint
    global listeCentre
    global addPointMode
    global listeBord
    cnv.delete('all')
    if(addPointMode==0):
        texte = cnv.create_text(50,10,text='Add Point Mode', fill='red')
    else:
        texte = cnv.create_text(50,10,text='Add Point Mode', fill='green')
    listePoint = []
    listeCentre = []
    listeBord = []

##clearLine
def clearL():
    global listeCentre
    global addPointMode
    global listeBord
    cnv.delete('all')
    if(addPointMode==0):
        texte = cnv.create_text(50,10,text='Add Point Mode', fill='red')
    else:
        texte = cnv.create_text(50,10,text='Add Point Mode', fill='green')
    listeCentre = []
    listeBord = []
    for i in range(len(listePoint)):
        a=listePoint[i]
        cnv.create_rectangle(a[0]-2,a[1]-2,a[0]+2,a[1]+2, fill='red')

##addPointMode
def addPointModeDef():
    global addPointMode
    if(addPointMode==0):
        addPointMode=1
        texte = cnv.create_text(50,10,text='Add Point Mode', fill='green')
    elif (addPointMode==1):
        addPointMode=0
        texte = cnv.create_text(50,10,text='Add Point Mode', fill='red')

##Calcul
def calcul():
    global listePoint
    global listeCentre
    global listeBord

    #a)
    for i in range(len(listePoint)):
        for j in range(len(listePoint)):
            for k in range(len(listePoint)) : # on parcoure toutes les combinaisons de 3 points (triangle)
                if i!=j and i!=k and j!=k : # on exclut les situations où les points sont confondus
                    listeDpt = []
                    centreConforme = 1 #le centre est par défaut bon
                    a=listePoint[i]
                    b=listePoint[j] ## on stocke les coordonnées des points dans les var a,b,c pour les manipuler
                    c=listePoint[k]
                    xa=a[0]
                    ya=a[1]
                    xb=b[0]
                    yb=b[1]
                    xc=c[0]
                    yc=c[1]
                    #calcul du centre du cercle circonscrit
                    delta = 2*((xa*yb)+(ya*xc)+(xb*yc)-(xc*yb)-(yc*xa)-(xb*ya))
                    x=(((xa**2)+(ya**2))*yb+ya*((xc**2)+(yc**2))+yc*((xb**2)+(yb**2))-yb*((xc**2)+(yc**2))-yc*((xa**2)+(ya**2))-ya*((xb**2)+(yb**2)))/(delta)
                    y=-1*((xa**2+ya**2)*xb+xa*(xc**2+yc**2)+xc*(xb**2+yb**2)-xb*(xc**2+yc**2)-xc*(xa**2+ya**2)-xa*(xb**2+yb**2))/(delta)

                    da = sqrt(((xa-x)**2)+(ya-y)**2)    #meme distance pour les points b et c

                    for t in range(len(listePoint)):
                        if (t!=i) and (t!=j) and (t!=k):
                            pt = listePoint[t] #point t
                            dpt = sqrt(((pt[0]-x)**2)+(pt[1]-y)**2) #distance du point pt
                            listeDpt.append(dpt) #on stocke toutes les distances entre le centre t et d'autres point
                    for t in range(len(listeDpt)):
                        if (listeDpt[t]<da):
                            centreConforme = 0 # si 1 seul site est trop proche d'un centre, on ne l'affiche pas
                    if centreConforme:
                        listeCentre.append([x,y])
    #afficher les points centres sélectionnés
    for i in range(len(listeCentre)):
        a = listeCentre[i]
        cnv.create_rectangle(a[0]-2, a[1]-2, a[0]+2, a[1]+2, fill='blue')
    #print('listeCentre:')
    #print(listeCentre)



    #b)
    for i in range(len(listePoint)):
        for j in range(len(listePoint)):
            if (i!=j): # 2 sites différents
                a=listePoint[i]
                b=listePoint[j] ## on stocke les coordonnées des points dans les var a,b,c pour les manipuler
                xa=a[0]
                ya=a[1]
                xb=b[0]
                yb=b[1]
                midPoint = []
                midPoint.append((xa+xb)/2) # calcul du centre du couple de site
                midPoint.append((ya+yb)/2)
                G = [] # points du bord du canvas
                if (xa!=xb) and (ya!=yb):
                    slope = (xa-xb)/(yb-ya) # calcul de la pente
                    x0=midPoint[0]
                    y0=midPoint[1]
                    b=y0-slope*x0           #y=slope*x+b
                    if (-b/slope >= 0) and (-b/slope<=600): # cas y=0
                        G.append([-b/slope,0])
                    if (b>=0) and (b<=600) : #cas x=0
                        G.append([0,b])
                    if (b<=600-slope*600) and (b>=-slope*600): # cas x=600
                        G.append([600,(slope*600)+b])
                    if ((600-b)/slope<=600) and ((600-b)/slope>=0) : # cas y=600
                        G.append([(600-b)/slope,600])
                if (xa==xb):
                    G.append([0,midPoint[1]])
                    G.append([600,midPoint[1]])
                if (ya==yb):
                    G.append([midPoint[0],0])
                    G.append([midPoint[0],600])

                """
                for k in range(len(G)):
                    a=G[k]
                    cnv.create_rectangle(a[0]-2, a[1]-2, a[0]+2, a[1]+2, fill='black')
                """

                for k in range(len(G)):
                    G_ok = 1 #le point est conforme par défaut
                    p = G[k] # on nomme 1 point de G
                    da = sqrt(((xa-p[0])**2)+(ya-p[1])**2)   # distance G avec a ou b (meme distance)
                    for l in range(len(listePoint)):
                        if (l!=i) and (l!=j):
                            z = listePoint[l]
                            dl = sqrt(((z[0]-p[0])**2)+(z[1]-p[1])**2)   #distance entre G et d'autres sites
                            if (dl<da):
                                G_ok = 0
                    if G_ok:
                        listeBord.append(G[k])
    #afficher les points du bord sélectionnés

    for i in range(len(listeBord)):
        a = listeBord[i]
        cnv.create_rectangle(a[0]-2, a[1]-2, a[0]+2, a[1]+2, fill='yellow')


    #c)
    newListeCentre = []
    for i in listeCentre :
        if i not in newListeCentre:
            newListeCentre.append(i)

    newListeBord = []
    for i in listeBord :
        if i not in newListeBord:
            newListeBord.append(i)


    # on prend un centre ou un bord, on calcule sa distance à tous les points :
    # soit 2 points à la même distance = médiane
    # soit 3 point à la même distance = centre
    # on stocke les relations bords/site et centre/site
    # a voir : si 2 site en commun : on relie les points (ligne 2/3 du commentaire)

    listeCentre = newListeCentre + newListeBord # création liste points à relier
    listeRelier = [] # contient numéros des sites équidistants callé par i croissants (i appartient à listeCentre)

    for i in range(len(listeCentre)): # on prend 1 point à relier
        listeTemp = [] #liste distance point à relier/sites
        a = listeCentre[i]
        for j in range(len(listePoint)): # on prend 1 site
            b = listePoint[j]
            ab = round(sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)) # on prend la distance entre 1 point à relier et 1 site, on arrondi cette distance
            listeTemp.append(ab)
        setTemp2 = set() # stockage sites équidistants
        for j in range(len(listeTemp)):
            for k in range(len(listeTemp)):
                if j!=k:
                    if (round(listeTemp[j]) == listeTemp[k]): # marge?
                        setTemp2.add(j)
                        setTemp2.add(k) # ajout des site equidistants
        listeRelier.append(list(setTemp2))


    for i in range(len(listeRelier)):
        for j in range(len(listeRelier)):
            lTemp = []
            if j>i:
                l1=listeRelier[i]
                l2=listeRelier[j]
                lTemp=list(set(l1).intersection(l2))
                if len(lTemp)>=2:
                    a=listeCentre[i]
                    b=listeCentre[j]
                    cnv.create_line(a[0],a[1],b[0],b[1])



##code principal

fen = Tk()
titre = "Voronoi"
fen.title(titre)
cnv = Canvas(fen, width=Width, height=Height,bg='white')
cnv.pack()

Quitter= Button(fen,text='Quitter', command=fen.destroy)
Quitter.pack(side='right')

addPointModeB= Button(fen,text='addPointMode', command=addPointModeDef)
addPointModeB.pack(side='left')

calcul1= Button(fen,text='Calcul', command=calcul)
calcul1.pack(side='right')

clear= Button(fen,text='Clear All', command=clear)
clear.pack(side='right')

clear= Button(fen,text='Clear Lines', command=clearL)
clear.pack(side='right')

texte = cnv.create_text(50,10,text='Add Point Mode', fill='green')

cnv.bind('<Button-1>', click)
cnv.bind('<Motion>', bouge)
cnv.bind('<ButtonRelease-1>', unclick )


fen.mainloop()