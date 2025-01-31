class Camion:
    def __init__(self, bouteilles_vides, bouteilles_pleines, x, y, id, v = 50, capacite = 80):
        self._bouteilles_vides = bouteilles_vides
        self._bouteilles_pleines = bouteilles_pleines
        self._v = v
        self._x = x
        self._y = y
        self._capacite = capacite
        self._deplacement = False #booléen pour savoir si le camion est en déplacement
        self._id = id
        self._temps_deplacement = 0
        self._trajet = [(x,y)]
        self._etape_precedente = None
    
    def __repr__(self) :
        return(f'Camion(x = {self._x}, y = {self._y}, déplacement = {self._deplacement}, bouteilles vides = {self._bouteilles_vides}, bouteilles pleines = {self._bouteilles_pleines})')

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
            "trajet" : self._trajet,
            "etape_precedente" : self._etape_precedente
        }

    def capacite_actuelle(self) :
            return self._capacite - (self._bouteilles_pleines + self._bouteilles_vides)

    def charge(self, n, pleines:'bool'):
        if n <= self.capacite_actuelle() :
            if pleines:
                self._bouteilles_pleines = self._bouteilles_pleines + n
            else:
                self._bouteilles_vides = self._bouteilles_vides + n
        else:
            return False
    
    def decharge(self, n, pleines:'bool'):
        if pleines:
            if n <= self._bouteilles_pleines :
                self._bouteilles_pleines = self._bouteilles_pleines - n
            else:
                return False
        else:
            if n <= self._bouteilles_vides :
                self._bouteilles_vides = self._bouteilles_vides - n
            else:
                return False

    def deplacement(self, x, y, duree):
        self._x= x
        self._y = y
        self._trajet.append((x,y))
        self._temps_deplacement = duree

    def set_etape_precedente(self, type : 'str', id : 'int') :
        self._etape_precedente = [type, id]

    def actualisation(self, dt):
        self._temps_deplacement = self._temps_deplacement - dt