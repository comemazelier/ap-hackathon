class Camion:
    def __init__(self, b_vides, b_pleines, x, y, id, v = 50, capacite = 80):
        self._b_vides = b_vides
        self._b_pleines = b_pleines
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
        return(f'Camion(x = {self._x}, y = {self._y}, déplacement = {self._deplacement}, b vides = {self._b_vides}, b pleines = {self._b_pleines})')

    def get_data(self):
        return {
            "x": self._x,
            "y": self._y,
            "v" : self._v,
            "capacite": self._capacite,
            "b_pleines": self._b_pleines,
            "b_vides": self._b_vides,
            "deplacement" : self._deplacement,
            "temps_deplacement": self._temps_deplacement,
            "id": self._id,
            "trajet" : self._trajet,
            "etape_precedente" : self._etape_precedente
        }

    def capacite_actuelle(self) :
            return self._capacite - (self._b_pleines + self._b_vides)

    def charge(self, n, bouteilles : 'str'):
        if n <= self.capacite_actuelle() :
            if bouteilles == 'p':
                self._b_pleines = self._b_pleines + n
            else:
                self._b_vides = self._b_vides + n
        elif bouteilles == 'v':
            return False
    
    def decharge(self, n, bouteilles : 'str'):
        if bouteilles == 'p':
            if n <= self._b_pleines :
                self._b_pleines = self._b_pleines - n
            else:
                return False
        elif bouteilles == 'v':
            if n <= self._b_vides :
                self._b_vides = self._b_vides - n
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