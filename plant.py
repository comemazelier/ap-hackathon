class Plant:
    def __init__(self, coord_x, coord_y, capacite, init, refill, libre, id):
        self._coord_x = coord_x
        self._coord_y = coord_y  # Stocke la position sous forme de tuple (x, y)
        self._capacite = capacite         # Capacité maximale de l’usine
        self._bouteilles_pleines = init
        self._bouteilles_vides = 0               # Nombre actuel de bouteilles pleines en stock
        self._production = refill             # Nombre de bouteilles pouvant être remplies par jour
        self._libre = libre
        self._id = id
        
    
    def actualisation(self, dt): #remplir un certain nombre de bouteilles jusqu’à la capacité de l’usine.
      self._bouteilles_vides = max(0, self._bouteilles_vides - dt*self._production)
      self._bouteilles_pleines = min(0,self._bouteilles_pleines + dt*self._production)
    
    def charge(self, n):
      if self._bouteilles_vides + n > self._capacite :
         print('Error')
      else :
         self._bouteilles_vides += n
    
    def decharge(self, n) :
      if self._bouteilles_pleines > n :
         print('Error')
      else :
         self._bouteilles_vides += n



