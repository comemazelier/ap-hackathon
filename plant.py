class Plant:
    def __init__(self, coord_x, coord_y, capacity, init, refill):
        self.coord = (coord_x, coord_y)  # Stocke la position sous forme de tuple (x, y)
        self.capacity = capacity         # Capacité maximale de l’usine
        self.stock = init                # Nombre actuel de bouteilles pleines en stock
        self.refill = refill             # Nombre de bouteilles pouvant être remplies par jour
    
    def remplir_bouteilles(self, quantite): #remplir un certain nombre de bouteilles jusqu’à la capacité de l’usine.
        remplissage = min(self.refill, quantite)
        self.stock += remplissage
        return remplissage