import matplotlib.pyplot as plt

from camion import Camion
from client import Client
from plant import Plant
import numpy as np

class Flotte :
    def __init__(self, clients : 'list[Client]', usines, clients_filename, plants_filename ):
        self.camions = []
        self.clients = clients
        self.usines = usines
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
        for camion in camions :
            x_camion, y_camion = camion.coord_x(), camion.coord_y()
            distance = []
            if camion._bouteilles_pleines > 0 :
                clients_libres = [client for client in self.clients if client.get_data()['libre']]
                for client in clients_libres:
                    client_dict = client.get_data()
                    x_client, y_client = client_dict['x'], client_dict['y']
                    dist = np.sqrt( (x_client - x_camion)**2 + (y_client - y_camion)**2  )
                    distance.append(dist)
                client = clients_libres[np.argmin(distance)]
                camion.deplacement(client.get_data()['x'], client.get_data()['y'], min(distance)/camion.get_data()['v'])
                client.change_libre()
            else :
                usines_libres = [usine for usine in self.usines if usine.get_data()['libre']]
                for usine in usines_libres:
                    usine_dict = usine.get_data()
                    x_usine, y_usine = usine_dict['x'], usine_dict['y']
                    dist = np.sqrt( (x_usine - x_camion)**2 + (y_usine - y_camion)**2  )
                    distance.append(dist)
                usine = usines_libres[np.argmin(distance)]
                camion.deplacement(client.get_data()['x'], client.get_data()['y'], min(distance)/camion.get_data()['v'])
                usine.change_libre()

    def plot_flotte(self):
        plt.figure(figsize=(10, 10))

        for client in self.clients:
            plt.scatter(client._coord_x, client._coord_y, color='blue', marker='o', label="Client" if "Client" not in plt.gca().get_legend_handles_labels()[1] else "")

        for plant in self.plants:
            plt.scatter(plant._coord_x, plant.coord_y, color='red', marker='s', label="Usine" if "Usine" not in plt.gca().get_legend_handles_labels()[1] else "")

        for camion in self.camions:
            if camion._trajet:
                trajet_x = [pos[0] for pos in camion._trajet]
                trajet_y = [pos[1] for pos in camion._trajet]
                plt.plot(trajet_x, trajet_y, linestyle='--', marker='x', label=f'Camion {camion._id}')

        plt.xlabel('Coordonnée X')
        plt.ylabel('Coordonnée Y')
        plt.title('Carte des Clients, Usines et Trajets des Camions')
        plt.legend()
        plt.grid(True)
        plt.show()

