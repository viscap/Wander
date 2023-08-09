# -*- coding: utf-8 -*-
"""
@author: AranaCorp
https://www.aranacorp.com/pt/detectar-uma-linha-com-python-e-a-opencv/
"""
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


class LineTracking():
    """
    Classe permettant le traitement d'image, la délimitation d'un contour et permet de 
    trouver le centre de la     forme detectée
    Aula que permite o tratamento de imagens, a delimitação de um contorno e permite
    encontre o centro da forma detectada
    """
    def __init__(self,img_file):
        """The constructor."""
        self.img = cv2.imread(img_file)
        self.img_inter = self.img
        self.img_final = self.img
        self.cendroids = []
        self.mean_centroids = [0,0]

    def processing(self):
        """Méthode permettant le traitement d'image"""
        """Método para processamento de imagem"""
        #self.img=cv2.resize(self.img,(int(self.img.shape[1]*0.2),int(self.img.shape[0]*0.2))) #redimensionar imagem original
        print(self.img.shape)
        #self.img = self.img[199:391, 149:505] # refocamos a imagem excluindo as áreas externas para ter maior precisão no restante
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) # mudamos a imagem para tons de cinza
        blur = cv2.GaussianBlur(gray,(5,5),0) # desfocamos a imagem
        ret,thresh = cv2.threshold(blur,180,255,cv2.THRESH_BINARY_INV) # binarizamos a imagem

        self.img_inter=thresh
        """Une ouverture permet d'enlever tous les élements qui sont plus petits que l'élement structurant (ou motif)
        Une fermeture permet de "combler" les trous qui ont une taille inférieur à l'élement structurant """
        """Uma abertura permite remover todos os elementos menores que o elemento estruturante (ou padrão)
        Um fecho permite "preencher" os buracos que têm um tamanho menor que o elemento estruturante """

        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)) # criamos o elemento estruturante da abertura
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)) # criamos o elemento estruturante do fechamento

        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open) # fazemos uma abertura seguindo um padrão
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close) # fazemos um fechamento seguindo um padrão

        connectivity = 8

        output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S) #delimita uma forma
        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        
        self.centroids = output[3] #retorna os centros da(s) forma(s) da imagem

        for c in self.centroids :
            """Permet de faire la moyenne des centres de la forme, en effet sur l'image test,
               il y a deux centres qui sont très proches et la moyenne de deux convient.
               On pourra imaginer que dans un cas général on modifie cela

               Permite calcular a média dos centros da forma, de fato na imagem de teste,
               tem dois centros muito próximos e a média de dois está bom.
               Podemos imaginar que em um caso geral modificamos este
            """
            self.mean_centroids[0] += c[0]/len(self.centroids)
            self.mean_centroids[1] += c[1]/len(self.centroids)

        self.img_final = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        #permet de rajouter un carré rouge à l'endroit du centre de la forme
        #permite adicionar um quadrado vermelho no centro da forma
        #self.img_final[int(self.mean_centroids[1])-10 : int(self.mean_centroids[1])+20, int(self.mean_centroids[0])-10 : int(self.mean_centroids[0])+20] = [0,0,255]
        for c in self.centroids :
            self.img_final[int(c[1])-5 : int(c[1])+10, int(c[0])-5 : int(c[0])+10] = [0,255,0]

if __name__ == '__main__' :
   
    #para capturar da camera do drone ou webcam  
    #camera = cv2.VideoCapture(0) 

    #para capturar um arquivo de video
    camera = cv2.VideoCapture('ramos5.mp4')

    if camera.isOpened():
        validacao, frame = camera.read()
        while validacao:
            validacao, frame = camera.read()
            
            #gera uma imagem do frame capturado
            cv2.imwrite('imgTmp.png',frame)

            #processa a imagem 
            test = LineTracking('imgTmp.png') #créer un objet LineTracking qui est la Classe créée au dessus .png ou .jpg
            #test = LineTracking('teste.png') #cria um objeto LineTracking que é a classe criada acima .png ou .jpg
            
            test.processing()

            #exibe a imagem original após o redimensionamento
            cv2.imshow('image',frame) #affiche l'image original après redimensionnement

            #exibe a imagem após o processamento
            ##cv2.imshow('process',test.img_inter ) #affiche l'image après traitement
            cv2.imshow('cable',test.img_final) #affiche l'image après traitement

            #para fechar as janelas aperte a barra de 'espaço'
            key= cv2.waitKey(1);
            if  key == ord(' '): #pour fermer les fenêtres appuyer sur la barre 'espace'
                break

        camera.release()    
        cv2.destroyAllWindows()