import matplotlib.pyplot as plt

from camion import Camion
from client import Client
from plant import Plant
import numpy as np

class Flotte :
    def __init__(self, clients : 'list[Client]', usines, clients_filename, plants_filename ):
        self.camions = []
        self.clients = clients
        self.plants = usines
        self.profit = 0
        self.camions_en_deplacement = []
        self.camions_stationnes = []
    
    def actualisation(self) :
        t = min([camion.temps_deplacement for camion in self.camions_en_deplacement])
        for camion in self.camions_en_deplacement :
            camion.actualisation(t)
        for client in self.clients :
            client.actualisation(t)
        for usine in self.usines :
            usine.actualisation(t)

    def calcul_destinations(self) :
        camions = self.camions_en_deplacement
        clients_libres = [client for client in self.clients if client._libre]
        for camion in camions :
            x_camion, y_camion = camion.coord_x(), camion.coord_y()
            distance = []
            for client in clients_libres:
                x_client, y_client = clients_libres.coord_x(), clients_libres.coord_y()
                dist = np.sqrt( (x_client - x_camion)**2 + (y_client - y_camion)**2  )
                distance.append(dist)
            
            camion.position = clients_libres[np.argmin(distance)]
            camion.deplacement = not camion.deplacement
            camion._temps_deplacement = np.min(distance)/50
            clients_libres[np.argmin(distance)]._libre = not clients_libres[np.argmin(distance)]._libre

