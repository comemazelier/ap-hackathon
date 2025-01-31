class Client:
    def __init__(self, coord_x, coord_y, capacite, init, consumption, id):
        self._x = coord_x
        self._y = coord_y
        self._capacite = capacite
        self._b_vides = init
        self._b_pleines = 0
        self._id = id
        self._libre = True
        self._consommation = float(consumption)/24 #Consommation horaire
    
    def get_data(self):
        return {
            "x": self._x,
            "y": self._y,
            "capacite": self._capacite,
            "b_vides": self._b_vides,
            "b_pleines" : self._b_pleines,
            "consommation": self._consommation,
            "libre" : self._libre,
            "id" : self._id
        }
    
    def __repr__(self):
        return (f"Client(x = {self._x}, y = {self._y}",
                f"capacité = {self._capacite}, b pleines = {self._b_pleines}, consumption = {self._consumption})")
    
    def actualisation(self, dt):
        b_consommees = min(self._b_pleines, dt*self._consommation/24)
        self._b_pleines -= b_consommees
        self._b_vides += b_consommees
    
    def capacite_actuelle(self):
        return self._capacite - (self._b_vides + self._b_pleines)

    def charge(self, n):
        if n <= self.capacite_actuelle() :
            self._b_pleines += n
        else :
            print(f'Error charge client {self._id}.')
            return False

    def decharge(self, n):
        if n <= self._b_vides :
            self._b_vides -= n
        else :
            print(f'Error decharge cllient {self._id}.')
            return False

    def change_libre(self) :
        self._libre = 1 - self._libre
