from camion import Camion
from clients import Client
from plant import Plant

class Flotte :
    def __init__(self, clients : 'list[Client]', usines ):
        self.camions = []
        self.clients = clients
        self.plants = usines
        self.profit = 0
        self.camions_en_deplacement = self.camions
        self.camions_stationnes = []
    
    def actualisation(self) :
        t = min([camion.temps_deplacement for camion in self.camions_en_deplacement])
        for camion in self.camions_en_deplacement :
            camion.actualisation(t)
        for client in self.clients :
            client.actualisation(t)
        for usine in self.usines :
            usines.actualisation(t)


        

    def calcul_destinations() :
        pass