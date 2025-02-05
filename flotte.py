import matplotlib.pyplot as plt

from camion import Camion
from client import Client
from usine import Usine
import numpy as np

class Flotte :
    def __init__(self, clients : 'list[Client]', usines : 'list[Usine]', camions : 'list[Camion]'):
        self.camions = camions
        self.clients = clients
        self.usines = usines
        self.profit = 0
        self.camions_en_deplacement = []
        self.camions_stationnes = camions
        self._time = 0 #En h
        self._etape = 0
    
    def actualisation(self) :
        duree_min = float('inf')
        camions_arrives = []
        camions_pas_arrives = []
        for camion in self.camions_en_deplacement :
            tps_restant =  camion.temps_deplacement
            if tps_restant < duree_min :
                duree_min = tps_restant
                camions_pas_arrives = camions_pas_arrives + camions_arrives
                camions_arrives = [camion]
            elif tps_restant == duree_min :
                camions_arrives.append(camion)
            else :
                camions_pas_arrives.append(camion)
        self.camions_stationnes = self.camions_stationnes + camions_arrives
        self.camions_en_deplacement = camions_pas_arrives
        print(f'duree_min = {duree_min}')
        for camion in self.camions_en_deplacement :
            camion.actualisation(duree_min)
        for client in self.clients :
            client.actualisation(duree_min)
        for usine in self.usines :
            b_pleines_avant = usine.b_pleines
            usine.actualisation(duree_min)
            self.profit -= 40*(usine.b_pleines - b_pleines_avant)
        self._time += duree_min

    def id_to_object(self, type : 'str', id : 'int') :
        if type == 'c' :
            for client in self.clients :
                if client.id == id :
                    return client
        elif type == 'u' :
            for usine in self.usines :
                if usine.id == id :
                    return usine

    @staticmethod
    def distance(objet1, objet2) :
        x1, y1, x2, y2 = objet1.x, objet1.y, objet2.x, objet2.y
        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


    def calcul_destinations(self) :
        if self._etape > 0 :
            self.actualisation()
        camions_stationnes_2 = []
        for camion in self.camions_stationnes :
            distances = []
            clients_a_servir = [client for client in self.clients if (client.libre and not client.plein)]
            if camion.b_pleines > 0 and len(clients_a_servir) > 0 :
                for client in clients_a_servir:
                    distances.append(self.distance(client, camion))
                client = clients_a_servir[np.argmin(distances)]
                camion.deplacement(client.x, client.y, min(distances)/camion.v)
                self.echange_client(camion, client)
                client.change_libre()
                camion.set_etape_precedente('c', client.id)
                point_de_depart = camion.etape_precedente
                if  point_de_depart != None :
                    self.id_to_object(point_de_depart[0], point_de_depart[1]).change_libre()
                self.camions_en_deplacement.append(camion)
            elif camion.b_pleines < camion.capacite :
                for usine in self.usines:
                    dist = np.sqrt((usine.x - camion.x)**2 + (usine.y - camion.y)**2)
                    distances.append(dist)
                usine = self.usines[np.argmin(distances)]
                camion.deplacement(usine.x, usine.y, min(distances)/camion.v)
                self.echange_usine(camion, usine)
                camion.set_etape_precedente('u', usine.id)
                point_de_depart = camion.etape_precedente
                if  point_de_depart != None :
                    self.id_to_object(point_de_depart[0], point_de_depart[1]).change_libre()
                self.camions_en_deplacement.append(camion)
            else :
                camions_stationnes_2.append(camion)
        self._etape += 1
        self.camions_stationnes = camions_stationnes_2
        print(f'Etape {self._etape}')
        print(f'Bouteilles pleines dans les usines : {[usine.b_pleines for usine in self.usines]}')
        print(f'Bouteilles vides dans les usines : {[usine.b_vides for usine in self.usines]}')
        print(f'Bouteilles pleines dans les clients : {[client.b_pleines for client in self.clients]}')
        print(f'Bouteilles vides dans les clients : {[client.b_vides for client in self.clients]}')
        print([f'Camion {camion.id} : pleines : {camion.b_pleines}, vides : {camion.b_vides}, dernière étape : {camion.etape_precedente}' for camion in self.camions])
        print('\n')

    def echange_client(self, camion : 'Camion', client : 'Client'):
        echange = min(camion.b_pleines, client.b_vides)
        camion.decharge(echange, 'p')
        camion.charge(echange, 'v')
        client.decharge(echange)
        client.charge(echange)
        self.profit += echange*60
        if client.capacite_actuelle() > 0 and camion.b_pleines > 0 :
            echange = min(client.capacite_actuelle(), camion.b_pleines)
            self.profit += echange*60
            camion.decharge(echange, 'p')
            client.charge(echange)
        elif camion.capacite_actuelle() > 0 and client.b_vides > 0 :
            echange = min(camion.capacite_actuelle(), client.b_vides)
            camion.charge(echange, 'v')
            client.decharge(echange)

    @staticmethod
    def echange_usine(camion : 'Camion', usine : 'Usine'):
        echange = min(camion.b_vides, usine.b_pleines)
        camion.decharge(echange, 'v')
        camion.charge(echange, 'p')
        usine.decharge(echange)
        usine.charge(echange)
        if usine.capacite_actuelle() > 0 and camion.b_vides > 0 :
            echange = min(usine.capacite_actuelle(), camion.b_vides)
            camion.decharge(echange, 'v')
            usine.charge(echange)
        elif camion.capacite_actuelle() > 0 and usine.b_pleines > 0 :
            echange = min(camion.capacite_actuelle(), usine.b_pleines)
            camion.charge(echange, 'p')
            usine.decharge(echange)

    def plot_trajet(self) :
        for client in self.clients:
            plt.scatter(client.x, client.y, color='blue', marker='o')

        for plant in self.usines:
            plt.scatter(plant.x, plant.y, color='red', marker='s')

        for camion in self.camions:
            if camion._trajet:
                trajet_x = [pos[0] for pos in camion.trajet]
                trajet_y = [pos[1] for pos in camion.trajet]
                plt.plot(trajet_x, trajet_y, linestyle='--', marker='x', label=f'Camion {camion.id}')

        plt.xlabel('Coordonnée X')
        plt.ylabel('Coordonnée Y')
        plt.title('Carte des Clients, Usines et Trajets des Camions')
        plt.legend()
        plt.grid(True)
        plt.show()

