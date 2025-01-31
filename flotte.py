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
        for camion in self.camions_en_deplacement :
            tps_restant =  camion.get_data()['temps_deplacement']
            if tps_restant < duree_min :
                duree_min = tps_restant
                camions_arrives = [camion]
            elif tps_restant == duree_min :
                camions_arrives.append(camion)
        print(f'duree_min = {duree_min}')
        for camion in self.camions_en_deplacement :
            camion.actualisation(duree_min)
        for client in self.clients :
            client.actualisation(duree_min)
        for usine in self.usines :
            usine.actualisation(duree_min)
        self._time += duree_min

    def id_to_object(self, type : 'str', id : 'int') :
        if type == 'c' :
            for client in self.clients :
                if client.get_data()['id'] == id :
                    return client
        elif type == 'u' :
            for usine in self.usines :
                if usine.get_data()['id'] == id :
                    return usine

    def calcul_destinations(self) :
        if self._etape > 0 :
            self.actualisation()
        print(f'Etape {self._etape}')
        print(f'Bouteilles pleines dans les usines : {[usine.get_data()['b_pleines'] for usine in self.usines]}')
        print(f'Bouteilles vides dans les usines : {[usine.get_data()['b_vides'] for usine in self.usines]}')
        print(f'Bouteilles pleines dans les clients : {[client.get_data()['b_pleines'] for client in self.clients]}')
        print(f'Bouteilles vides dans les clients : {[client.get_data()['b_vides'] for client in self.clients]}')
        print('Camion : ', [f': (Pleines : {camion.get_data()['b_pleines']}, vides : {camion.get_data()['b_vides']}' for camion in self.camions])
        print('\n')
        for camion in self.camions_stationnes :
            camion_dict = camion.get_data()
            x_camion, y_camion = camion_dict['x'], camion_dict['y']
            distance = []
            if camion_dict['b_pleines'] > 0 :
                clients_libres = [client for client in self.clients if client.get_data()['libre']]
                for client in clients_libres:
                    client_dict = client.get_data()
                    x_client, y_client = client_dict['x'], client_dict['y']
                    dist = np.sqrt( (x_client - x_camion)**2 + (y_client - y_camion)**2  )
                    distance.append(dist)
                client = clients_libres[np.argmin(distance)]
                camion.deplacement(client.get_data()['x'], client.get_data()['y'], min(distance)/camion.get_data()['v'])
                self.echange_client(camion, client)
                client.change_libre()
                camion.set_etape_precedente('c', client.get_data()['id'])
                point_de_depart = camion_dict['etape_precedente']
                if  point_de_depart != None :
                    self.id_to_object(point_de_depart[0], point_de_depart[1]).change_libre()
            else :
                usines_libres = [usine for usine in self.usines if usine.get_data()['libre']]
                for usine in usines_libres:
                    usine_dict = usine.get_data()
                    x_usine, y_usine = usine_dict['x'], usine_dict['y']
                    dist = np.sqrt( (x_usine - x_camion)**2 + (y_usine - y_camion)**2  )
                    distance.append(dist)
                usine = usines_libres[np.argmin(distance)]
                camion.deplacement(usine.get_data()['x'], usine.get_data()['y'], min(distance)/camion.get_data()['v'])
                self.echange_usine(camion, usine)
                usine.change_libre()
                camion.set_etape_precedente('u', usine.get_data()['id'])
                point_de_depart = camion_dict['etape_precedente']
                if  point_de_depart != None :
                    self.id_to_object(point_de_depart[0], point_de_depart[1]).change_libre()
            self.camions_en_deplacement.append(camion)
        self._etape += 1 

    @staticmethod
    def echange_client(camion : 'Camion', client : 'Client'):
        camion_dict = camion.get_data()
        client_dict = client.get_data()
        echange = min(camion_dict['b_pleines'], client_dict['b_vides'])
        camion.decharge(echange, 'p')
        camion.charge(echange, 'v')
        client.decharge(echange)
        client.charge(echange)
        if client.capacite_actuelle() > 0 and camion_dict['b_pleines'] > 0 :
            echange = min(client.capacite_actuelle(), camion_dict['b_pleines'])
            camion.decharge(echange, 'p')
            client.charge(echange)
        elif camion.capacite_actuelle() > 0 and client_dict['b_vides'] > 0 :
            echange = min(camion.capacite_actuelle(), client_dict['b_vides'])
            camion.charge(echange, 'v')
            client.decharge(echange)

    @staticmethod
    def echange_usine(camion : 'Camion', usine : 'Usine'):
        camion_dict = camion.get_data()
        usine_dict = usine.get_data()
        echange = min(camion_dict['b_vides'], usine_dict['b_pleines'])
        camion.decharge(echange, 'v')
        camion.charge(echange, 'p')
        usine.decharge(echange)
        usine.charge(echange)
        if usine.capacite_actuelle() > 0 and camion_dict['b_vides'] > 0 :
            echange = min(usine.capacite_actuelle(), camion_dict['b_vides'])
            camion.decharge(echange, 'v')
            usine.charge(echange)
        elif camion.capacite_actuelle() > 0 and usine_dict['b_pleines'] > 0 :
            echange = min(camion.capacite_actuelle(), usine_dict['b_pleines'])
            camion.charge(echange, 'p')
            usine.decharge(echange)

    def plot_trajet(self) :
        for client in self.clients:
            client_dict = client.get_data()
            plt.scatter(client_dict['x'], client_dict['y'], color='blue', marker='o')

        for plant in self.usines:
            plant_dict = plant.get_data()
            plt.scatter(plant_dict['x'], plant_dict['y'], color='red', marker='s')

        for camion in self.camions:
            if camion._trajet:
                camion_dict = camion.get_data()
                trajet_x = [pos[0] for pos in camion_dict['trajet']]
                trajet_y = [pos[1] for pos in camion_dict['trajet']]
                plt.plot(trajet_x, trajet_y, linestyle='--', marker='x', label=f'Camion {camion_dict['id']}')

        plt.xlabel('Coordonnée X')
        plt.ylabel('Coordonnée Y')
        plt.title('Carte des Clients, Usines et Trajets des Camions')
        plt.legend()
        plt.grid(True)
        plt.show()

