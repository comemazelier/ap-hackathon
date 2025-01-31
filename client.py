
import pandas as pd

class Client:
    def __init__(self, coord_x, coord_y, capacity, init, consumption):
        self.coord_x = int(coord_x)
        self.coord_y = int(coord_y)
        self.capacity = int(capacity)
        self.stock = int(init)
        self.consumption = float(consumption)
    
    def get_data(self):
        return {
            "coord_x": self.coord_x,
            "coord_y": self.coord_y,
            "capacity": self.capacity,
            "stock": self.stock,
            "consumption": self.consumption
        }
    
    def __repr__(self):
        return (f"Client(coord_x={self.coord_x}, coord_y={self.coord_y}, "
                f"capacity={self.capacity}, stock={self.stock}, consumption={self.consumption})")
    
    def __evol_stock__(t, self):
        pass        



class ClientsList:
    def __init__(self, filename):
        self.clients = self.load_clients(filename)
    
    def load_clients(self, filename):
        clients = []
        df = pd.read_csv(filename)  
        for _, row in df.iterrows(): 
            clients.append(Client(row["coord_x"], row["coord_y"], row["capacity"], row["init"], row["consumption"]))
        return clients
    
    def get_all_clients_data(self):
        return [client.get_data() for client in self.clients]
    
    def __repr__(self):
        return f"ClientsList({self.clients})"

# Exemple d'utilisation
clients_list = ClientsList("clients.csv")
print(clients_list.get_all_clients_data())