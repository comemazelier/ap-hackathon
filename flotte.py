from camion import Camion
from client import Client
from plant import Plant

class Flotte :
    def __init__(self, clients : 'list[Client]', plants : 'list[Plant]'):
        self.camions = []
        self.clients = clients
        self.plants = plants
        self.profit = 0
        self.camions_en_deplacement = []
        self.camions_stationnes = []
    
    def actualisation(self) :
        dt = min([camion.temps_deplacement for camion in self.camions_en_deplacement])
        for camion in self.camions_en_deplacement :
            camion.actualisation(dt)
        for client in self.clients :
            client.actualisation(dt)
        for usine in self.usines :
            usine.actualisation(dt)

    def calcul_destinations() :
        pass
