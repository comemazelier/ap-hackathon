import pandas as pd
import numpy as np
import argparse
from client import Client
from plant import Plant
from flotte import Flotte

parser = argparse.ArgumentParser()
parser.add_argument('--clients_filename', '-c', help = 'Enter clients file path', default = 'clients.csv')
parser.add_argument('--plants_filename', '-p', help = 'Enter plants file path', default = 'plants.csv')
args = parser.parse_args()

clients_filename = args.clients_filename
plants_filename = args.plants_filename

df_clients = pd.read_csv(clients_filename)
df_plants = pd.read_csv(plants_filename)


clients = []
for _, row in df_clients.iterrows(): 
    clients.append(Client(row["coord_x"], row["coord_y"], row["capacity"], row["init"], row["consumption"]))


plants = []
for _,row in df_plants.ierrows():
    plants.append(Plant(row["coord_x"], row["coord_y"], row["capacity"], row["capacity"], row["init"], row["refill"], row["libre"] ))

flotte = Flotte(clients, plants)
flotte.plot_flotte()    

