import pandas as pd
import numpy as np
import argparse
from client import Client
from usine import Usine
from flotte import Flotte
from camion import Camion

parser = argparse.ArgumentParser()
parser.add_argument('--clients_filename', '-c', help = 'Enter clients file path', default = 'clients.csv')
parser.add_argument('--plants_filename', '-p', help = 'Enter plants file path', default = 'plants.csv')
args = parser.parse_args()

clients_filename = args.clients_filename
plants_filename = args.plants_filename

df_clients = pd.read_csv(clients_filename)
df_plants = pd.read_csv(plants_filename)


clients = []
id = 0
for _, row in df_clients.iterrows() :
    clients.append(Client(row["coord_x"], row["coord_y"], row["capacity"], row["init"], row["consumption"], id))
    id += 1


plants = []
id = 0
for _,row in df_plants.iterrows():
    plants.append(Usine(row["coord_x"], row["coord_y"], row["capacity"], row["init"], row["refill"], id))
    id += 1

camions = [Camion(b_pleines = 0, b_vides = 0, x = 300, y = 4850, id = i) for i in range(100)]
camions_tres_simple = [Camion(b_pleines = 0, b_vides = 0, x = 3, y = 0, id = i) for i in range(2)]

flotte = Flotte(clients, plants, camions)
# for i in range(150):
while flotte.time < 15 :
    flotte.calcul_destinations()
# print(flotte.camions_stationnes)
# print(flotte.camions[0].trajet)
print(flotte.time)
jours = flotte.time//24
heure = flotte.time%24
minutes = (60*heure)%60
print(f'Profit au bout de {int(jours)}j, {int(heure)}h et {int(minutes)}min ({flotte.etape} étapes): {flotte.profit} €.')
flotte.plot_trajet()

