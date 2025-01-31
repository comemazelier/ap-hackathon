class Camion:
    def __init__(self, bouteilles_vides, bouteilles_pleines, position, capacite = 80, deplacement, id, temps_deplacement):
        self._bouteilles_vides = bouteilles_vides
        self._bouteilles_pleines = bouteilles_pleines
        self._position = position
        self._capacite = capacite
        self._deplacement = deplacement
        self._id = id
        self._temps_deplacement = temps_deplacement
        
    @property
    def bouteilles_vides(self):
        return self._bouteilles_vides
    
    @property
    def capacite_totale(self):
        return self._capacite
    
    def capacite_actuelle(self):
        return self._capacite - (self._bouteilles_vides + self._bouteilles_pleines)
    
    @property
    def bouteilles_pleines(self):
        return self.bouteilles_pleines
    
    @property
    def position(self):
        return self._position

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

    def deplacement(self, destination):
        self._position = destination

    def  