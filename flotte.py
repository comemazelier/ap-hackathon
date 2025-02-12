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
        self.time = 0 #En h
        self.etape = 0
    
    def actualisation(self) :
        if len(self.camions_en_deplacement) == 0 :
            duree_min = 0.5
        else :
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
            for camion in self.camions_en_deplacement :
                camion.actualisation(duree_min)
            for client in self.clients :
                client.actualisation(duree_min)
            for usine in self.usines :
                b_pleines_avant = usine.b_pleines
                usine.actualisation(duree_min)
                self.profit -= 40*(usine.b_pleines - b_pleines_avant)
        print(f'Etape {self.etape} : duree_min = {duree_min}')
        print(f'Profit au bout de {self.time}h : {self.profit}')
        self.time += duree_min

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
        if self.etape > 0 :
            self.actualisation()
        # print(f'Etape {self.etape}')
        # print(f'Bouteilles pleines dans les usines : {[usine.b_pleines for usine in self.usines]}')
        # print(f'Bouteilles vides dans les usines : {[usine.b_vides for usine in self.usines]}')
        # print(f'Bouteilles pleines dans les clients : {[client.b_pleines for client in self.clients]}')
        # print(f'Bouteilles vides dans les clients : {[client.b_vides for client in self.clients]}')
        # print(f'Camions stationnes : {self.camions_stationnes}')
        # print([f'Camion {camion.id} - position {(camion.x, camion.y)}, pleines : {camion.b_pleines}, vides : {camion.b_vides}, dernière étape : {camion.etape_precedente}' for camion in self.camions])
        # print('\n')
        camions_stationnes_2 = []
        for camion in self.camions_stationnes :
            if type(camion.etape_precedente) != type(None) and camion.etape_precedente[0] == 'u' and camion.b_pleines == 0 :
                usine = self.id_to_object('u', camion.etape_precedente[1])
                if usine.b_pleines > 0 :
                    self.echange_usine(camion, usine)
            clients_a_servir = [client for client in self.clients if client.libre]
            # print([f'Client {client.id}' for client in clients_a_servir])
            note_max = -float('inf')
            destination = None
            vers_client = True
            for client in clients_a_servir :
                if self.distance(camion, client) == 0 :
                    print(f'Distance nulle entre {camion} et {client}')
                echange = min(camion.b_pleines, client.b_vides)
                b_echangeables = 2*echange + min(client.capacite_actuelle(), camion.b_pleines - echange) + min(camion.capacite_actuelle(), client.b_vides - echange)
                note = b_echangeables/(self.distance(camion, client))
                if note >= note_max :
                    note_max = note
                    destination = client
            for usine in self.usines :
                if self.distance(camion, usine) > 0 :
                    echange = min(camion.b_vides, usine.b_pleines)
                    b_echangeables = 2*echange + min(usine.capacite_actuelle(), camion.b_vides - echange) + min(camion.capacite_actuelle(), usine.b_pleines - echange)
                    note = b_echangeables/(5*self.distance(camion, usine))
                    if note >= note_max :
                        note_max = note
                        destination = usine
                        vers_client = False
            distance = self.distance(camion, destination)
            if note_max == 0 :
                camions_stationnes_2.append(camion)
            elif vers_client :
                client = destination
                camion.deplacement(client.x, client.y, distance/camion.v)
                self.echange_client(camion, client)
                client.change_libre()
                point_de_depart = camion.etape_precedente
                if  point_de_depart != None :
                    self.id_to_object(point_de_depart[0], point_de_depart[1]).change_libre()
                camion.set_etape_precedente('c', client.id)
                self.camions_en_deplacement.append(camion)
                self.profit -= 0.1*distance
            else :
                usine = destination
                camion.deplacement(usine.x, usine.y, distance/camion.v)
                self.echange_usine(camion, usine)
                point_de_depart = camion.etape_precedente
                if  point_de_depart != None :
                    self.id_to_object(point_de_depart[0], point_de_depart[1]).change_libre()
                camion.set_etape_precedente('u', usine.id)
                self.camions_en_deplacement.append(camion)
                self.profit -= 0.1*distance
        self.camions_stationnes = camions_stationnes_2
        self.etape += 1

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

