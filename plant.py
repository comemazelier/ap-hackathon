class Plant:
    def __init__(self, coord_x, coord_y, capacity, init, refill):
        self.coord = (coord_x, coord_y)  # Stocke la position sous forme de tuple (x, y)
        self.capacity = capacity         # Capacité maximale de l’usine
        self.stock = init                # Nombre actuel de bouteilles pleines en stock
        self.refill = refill             # Nombre de bouteilles pouvant être remplies par jour
    
    def remplir_bouteilles(self): #remplir un certain nombre de bouteilles jusqu’à la capacité de l’usine.
        remplissage = min(self.refill, self.capacity - self.stock)
        self.stock += remplissage
    
    def modifier_stock(self, pleines=0, vides=0):
      if pleines > 0:
        espace_disponible = self.capacity - self.stock
        ajout = min(pleines, espace_disponible)  # Ne pas dépasser la capacité
        self.stock += ajout
        message_pleines = f"{ajout} bouteilles pleines ajoutées."
      elif pleines < 0:
        retrait = min(abs(pleines), self.stock)  # Ne pas retirer plus que ce qui est dispo
        self.stock -= retrait
        message_pleines = f"{retrait} bouteilles pleines retirées."
      else:
        message_pleines = "Aucune modification de bouteilles pleines."

    # Message pour les bouteilles vides (non stockées dans l’usine)
      message_vides = f"{vides} bouteilles vides reçues (non stockées ici)."

      return f"{message_pleines} {message_vides} Stock actuel : {self.stock}/{self.capacity}."




