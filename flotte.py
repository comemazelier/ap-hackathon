from camion import Camion
from clients import Client
from plant import Plant

class Flotte :
    def __init__(self, clients : 'list[Client]', usines, clients_filename, plants_filename ):
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
            usine.actualisation(t)

    def load_clients(self, filename):
        clients = []
        df = pd.read_csv(filename)  
        for _, row in df.iterrows(): 
            clients.append(Client(row["coord_x"], row["coord_y"], row["capacity"], row["init"], row["consumption"]))
        return clients
        

    def calcul_destinations() :
        pass