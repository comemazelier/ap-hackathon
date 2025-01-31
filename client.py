
import pandas as pd

class Client:
    def __init__(self, coord_x, coord_y, capacity, init, _consumption):
        self._x = int(coord_x)
        self._y = int(coord_y)
        self._capacity = int(capacity)
        self._bouteilles_vides = init
        self._bouteilles = init
        self._bouteilles_pleines = 0
        self._libre = True
        self._consumption = float(_consumption)
    
    def get_data(self):
        return {
            "coord_x": self._x,
            "coord_y": self._y,
            "capacity": self._capacity,
            "stock": self._bouteilles,
            "consumption": self._consumption
        }
    
    def __repr__(self):
        return (f"Client(coord_x={self._x}, coord_y={self._y}, "
                f"capacity={self._capacity}, stock={self._bouteilles}, consumption={self._consumption})")
    
    def actualisation(self,dt):
        self._bouteilles_pleines = max(0,self._bouteilles_pleines-dt*self._consumption)
        self._bouteilles_vides = self._bouteilles - self._bouteilles_pleines
    
    def charge(self,n,m):
        if n-m + self._bouteilles > self._capacity :
            return False
        elif self._bouteilles_vides - m < 0 :
            return False
        else : 
            self._bouteilles += n-m
            self._bouteilles_vides -= m
            self._bouteilles_pleines += n
               



class ClientsList:
    def __init__(self, filename):
        self.clients = self.load_clients(filename)
    
    def load_clients(self, filename):
        clients = []
        df = pd.read_csv(filename)  
        for _, row in df.iterrows(): 
            clients.append(Client(row["coord_x"], row["coord_y"], row["capacity"], row["init"], row["_consumption"]))
        return clients
    
    def get_all_clients_data(self):
        return [client.get_data() for client in self.clients]
    
    def __repr__(self):
        return f"ClientsList({self.clients})"

clients_list = ClientsList("clients.csv")
print(clients_list.get_all_clients_data())