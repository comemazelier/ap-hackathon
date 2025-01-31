import matplotlib.pyplot as plt

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

    def calcul_destinations():
        pass

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