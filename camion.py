class Camion:
    def __init__(self, bouteilles_vides, bouteilles_pleines, x, y, deplacement, id, v = 50, capacite = 80):
        self._bouteilles_vides = bouteilles_vides
        self._bouteilles_pleines = bouteilles_pleines
        self._v = v
        self._x = x
        self._y = y
        self._capacite = capacite
        self._deplacement = deplacement #booléen pour savoir si le camion est en déplacement
        self._id = id
        self._temps_deplacement = 0
        self._trajet = []

    def get_data(self):
        return {
            "x": self._x,
            "y": self._y,
            "v" : self._v,
            "capacite": self._capacite,
            "bouteilles_pleines": self._bouteilles_pleines,
            "bouteilles_vides": self._bouteilles_vides,
            "deplacement" : self._deplacement,
            "temps_deplacement": self._temps_deplacement,
            "id": self._id,
        }

    def charge(self, n, pleines:'bool'):
        if n <= self.capacite_actuelle():
            if pleines:
                self._bouteilles_pleines = self._bouteilles_pleines + n
            else:
                self._bouteilles_vides = self.bouteilles_vides + n
        else:
            return False
    
    def decharge(self, n, bouteilles_pleines:'bool'):
        if bouteilles_pleines:
            if n <= self._bouteilles_pleines:
                self._bouteilles_pleines = self._bouteilles_pleines - n
            else:
                return False
        else:
            if n <= self._bouteilles_vides:
                self._bouteilles_vides = self._bouteilles_vides - n
            else:
                return False

    def deplacement(self, x, y, duree):
        self._x= x
        self._y = y
        self._trajet.append((x,y))
        self._temps_deplacement = duree
        
    def actualisation(self, dt):
        self._temps_deplacement = self._temps_deplacement - dt