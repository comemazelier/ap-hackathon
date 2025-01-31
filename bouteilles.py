import pandas as pd
import numpy as np

clients = pd.read_csv('clients.csv')
plants = pd.read_csv('plants.csv')

print(clients)
print(plants)

class Plant:
    def __init__(self, coord_x, coord_y, capacity, init, refill):
        self.coord = (coord_x, coord_y)  # Stocke la position sous forme de tuple (x, y)
        self.capacity = capacity         # Capacité maximale de l’usine
        self.stock = init                # Nombre actuel de bouteilles pleines en stock
        self.refill = refill             # Nombre de bouteilles pouvant être remplies par jour
    
    def remplir_bouteilles(self, quantite):
        remplissage = min(self.refill, quantite)
        self.stock += remplissage
        return remplissage
    

class Camions:
    def __init__(self, bouteilles_vides, bouteilles_pleines, position):
        self.bouteilles_vides = bouteilles_vides
        self.bouteilles_pleines = bouteilles_pleines
        self.position = position
    
