class Client:
    def __init__(self, coord_x, coord_y, capacite, init, consumption, id):
        self._x = int(coord_x)
        self._y = int(coord_y)
        self._capacite = int(capacite)
        self._bouteilles_vides = init
        self._bouteilles_pleines = 0
        self._id = id
        self._libre = True
        self._consumption = float(consumption)
    
    def get_data(self):
        return {
            "x": self._x,
            "y": self._y,
            "capacite": self._capacite,
            "bouteilles_vides": self._bouteilles_vides,
            "bouteilles pleines" : self._bouteilles_pleines,
            "consumption": self._consumption,
            "libre" : self._libre,
            "id" : self._id
        }
    
    def __repr__(self):
        return (f"Client(coord_x={self._x}, coord_y={self._y}, "
                f"capacity={self._capacity}, stock={self._bouteilles}, consumption={self._consumption})")
    
    def actualisation(self,dt):
        self._bouteilles_pleines = max(0,self._bouteilles_pleines-dt*self._consumption)
        self._bouteilles_vides = self._bouteilles - self._bouteilles_pleines
    
    def capacite_actuelle(self):
        return self._capacite - (self._bouteilles_vides + self._bouteilles_pleines)

    def charge(self,n):
        if n > self.capacite_actuelle() :
            self._bouteilles_pleines += n
        else :
            return False

    def decharge(self, m):
        if self._bouteilles_vides >= m :
            self._bouteilles_vides -= m
        else :
            return False

    def change_libre(self) :
        self._libre = 1 - self._libre
