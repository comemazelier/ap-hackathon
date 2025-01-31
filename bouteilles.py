import pandas as pd



class Plant:
    def __init__(self, coord_x, coord_y, capacity, init, refill):
        self.coord = (coord_x, coord_y)
        self.capacity = capacity
        self.stock = init
        self.refill = refill
    
    def remplir_bouteilles(self, quantite):
        remplissage = min(self.refill, quantite)
        self.stock += remplissage
        return remplissage
    




