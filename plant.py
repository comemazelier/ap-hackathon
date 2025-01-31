class Plant:
    def __init__(self, x, y, capacite, init, refill, id):
        self._x = x
        self._y = y  # Stocke la position sous forme de tuple (x, y)
        self._capacite = capacite         # Capacité maximale de l’usine
        self._bouteilles_pleines = init
        self._bouteilles_vides = 0               # Nombre actuel de bouteilles pleines en stock
        self._production = refill             # Nombre de bouteilles pouvant être remplies par jour
        self._libre = True
        self._id = id
        
    def get_data(self):
      return {
          "x": self._x,
          "y": self._y,
          "capacite": self._capacite,
          "bouteilles_pleines": self._bouteilles_pleines,
          "libre": self._libre,
          "id": self._id
      }

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

    def actualisation(self, dt): #remplir un certain nombre de bouteilles jusqu’à la capacité de l’usine.
      self._bouteilles_vides = max(0, self._bouteilles_vides - dt*self._production)
      self._bouteilles_pleines = min(0,self._bouteilles_pleines + dt*self._production)

    def change_libre(self) :
        self._libre = 1 - self._libre
