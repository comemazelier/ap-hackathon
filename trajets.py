import pandas as pd
import numpy as np

clients = pd.read_csv('clients.csv')
plants = pd.read_csv('plants.csv')

# Paramètres
NUM_CAMIONS = 100
CAP_CAMION = 80
VITESSE = 50  # km/h
COUT_KM = 0.10  # AC/km
PRIX_VENTE = 100  # AC/bouteille
COUT_REMPLISSAGE = 40  # AC/bouteille
DUREE_SIMULATION = 30  # jours

def distance (p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))





    


