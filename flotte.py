import matplotlib.pyplot as plt

from camion import Camion
from client import Client
from plant import Plant
import numpy as np

class Flotte :
    def __init__(self, clients : 'list[Client]', usines : 'list[Plant]', camions : 'list[Camion]'):
        self.camions = camions
        self.clients = clients
        self.usines = usines
        self.profit = 0
        self.camions_en_deplacement = []
        self.camions_stationnes = camions
        self.t = 0
    
    def actualisation(self) :
        if self.t == 0 :
            return None
        dt = min([camion.get_data()['temps_deplacement'] for camion in self.camions_en_deplacement])
        for camion in self.camions_en_deplacement :
            camion.actualisation(dt)
        for client in self.clients :
            client.actualisation(dt)
        for usine in self.usines :
            usine.actualisation(dt)

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
        self.actualisation()
        for camion in self.camions_stationnes :
            camion_dict = camion.get_data()
            x_camion, y_camion = camion_dict['x'], camion_dict['y']
            distance = []
            if camion_dict['bouteilles_pleines'] > 0 :
                clients_libres = [client for client in self.clients if client.get_data()['libre']]
                for client in clients_libres:
                    client_dict = client.get_data()
                    x_client, y_client = client_dict['x'], client_dict['y']
                    dist = np.sqrt( (x_client - x_camion)**2 + (y_client - y_camion)**2  )
                    distance.append(dist)
                client = clients_libres[np.argmin(distance)]
                camion.deplacement(client.get_data()['x'], client.get_data()['y'], min(distance)/camion.get_data()['v'])
                self.echange_bouteilles(camion, client)
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
                self.echange_bouteilles(camion, usine)
                usine.change_libre()
                camion.set_etape_precedente('u', usine.get_data()['id'])
                point_de_depart = camion_dict['etape_precedente']
                if  point_de_depart != None :
                    self.id_to_object(point_de_depart[0], point_de_depart[1]).change_libre()

    @staticmethod
    def echange_bouteilles(camion : 'Camion', client):
        camion_dict = camion.get_data()
        client_dict = client.get_data()
        echange = min(camion_dict['bouteilles_pleines'], client_dict['bouteilles_vides'])
        camion.decharge(echange, True)
        camion.charge(echange, False)
        client.charge(echange)
        client.decharge(echange)
        if client.capacite_actuelle() > 0 and camion_dict['bouteilles_pleines'] > 0 :
            echange = min(camion_dict['bouteilles_pleines'], client.capacite_actuelle())
            camion.decharge(echange, True)
            client.charge(echange)
        elif camion.capacite_actuelle() > 0 and client_dict['bouteilles_vides'] > 0 :
            echange = min(camion_dict['bouteilles_pleines'], client.capacite_actuelle())
            camion.charge(echange, False)
            client.decharge(echange)

    def plot_trajet(self):
        
       
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

