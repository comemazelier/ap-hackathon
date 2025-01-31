class Usine:
  def __init__(self, x, y, capacite, init, refill, id):
        self._x = x
        self._y = y  
        self._capacite = capacite         # Capacité maximale de l’usine
        self._b_pleines = init
        self._b_vides = 0               # Nombre actuel de b pleines en stock
        self._production = refill             # Nombre de b pouvant être remplies par jour
        self._libre = True
        self._id = id
        
  def get_data(self):
      return {
          "x": self._x,
          "y": self._y,
          "capacite": self._capacite,
          "b_pleines": self._b_pleines,
          "b_vides" : self._b_vides,
          "libre": self._libre,
          "id": self._id
      }

  def capacite_actuelle(self):
      return self._capacite - (self._b_pleines + self._b_vides)

  def charge(self, n):
      if n <= self.capacite_actuelle() :
        self._b_vides += n
      else :
        print(f'Error charge plant {self._id}.')

  def decharge(self, n) :
      if n <= self._b_pleines  :
        self._b_pleines -= n
      else :
        print(f'Error decharge plant {self._id}.')

  def actualisation(self, dt): #remplir un certain nombre de b jusqu’à la capacité de l’usine.
      b_produites = min(self.capacite_actuelle(), dt*self._production)
      self._b_vides -= b_produites
      self._b_pleines += b_produites

  def change_libre(self) :
        self._libre = 1 - self._libre
