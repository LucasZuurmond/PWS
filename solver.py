import numpy as np
import math
import random

"""
er is een matrix opgeslagen in een textbestand genaamd matrix.txt dit bestand zit in dezelfde map als dit programma. 
elke rij  wordt gesplitst met een nieuwe regel teken. 
Tussen elk getal in een rij staat " , " 
Er is ook geen lege regel aan het einde.
"""
afstandsmatrix = np.array([x[:-1].split(" , ") for x in open("matrix.txt", 'r').readlines()], dtype=float)
afstandsmatrix[0][0] = float('inf') # hierdoor kan het algoritme nooit van het beginpunt naar het beginpunt
aantal_wagens = 1


class Solver:
    def __init__(self, actieve_punten):
        self._startoplossing = actieve_punten

        # genereer het aantal iteraties, gebaseerd op hoeveel punten er meedoen in de startoplossing
        # moet de formule nog wat bijschaven, is een startformule
        self._iteraties = math.floor(2 * (len(actieve_punten)+1)**2 + 5)


    def solveOnce(self):
        deeloplossing = self._startoplossing[:]  # door [:] achter de lijst te zetten, maken we een kopie
        random.shuffle(deeloplossing)
        huidig_minimum = (self.GetDistanceSum(deeloplossing), deeloplossing)

        for iteratie in range(self._iteraties):
            mogelijkheid = deeloplossing[:]
            index1, index2 = random.sample(range(len(mogelijkheid)), 2)

            # index3 is om de eigenlijke index op te slaan, zodat we later het invers kunnen vervangen
            index1, index2, index3 = min(index1, index2) - 1, max(index1, index2), min(index1, index2)

            if index1 == -1: # is normaal het laatste item in de lijst
    
                index1 -= len(mogelijkheid)

            inverse = mogelijkheid[index2:index1:-1]

            mogelijkheid[index3:index2+1] = inverse

            # bekijk de waarde van beide deeloplossingen.
            origineleSom = self.GetDistanceSum(deeloplossing)
            mogelijkheidSom = self.GetDistanceSum(mogelijkheid)

            if deeloplossing == mogelijkheid:
                print(index2, index3)

            if mogelijkheidSom <= origineleSom:
                # de oplossing is beter, we accepteren de oplossing
                deeloplossing = mogelijkheid

                if mogelijkheidSom < huidig_minimum[0]:
                    huidig_minimum = (mogelijkheidSom, deeloplossing)

            else:
                kans = self.GetAcceptingChance(mogelijkheidSom=mogelijkheidSom, origineleSom=origineleSom, iteratie=iteratie)

                if kans:
                    # de oplossing is niet beter, we accepteren de oplossing alsnog, omdat we de kans hebben 'geraakt'

                    if origineleSom < huidig_minimum[0]:
                        huidig_minimum = (origineleSom, deeloplossing)
                    deeloplossing = mogelijkheid


        if self.GetDistanceSum(deeloplossing) > huidig_minimum[0]:
            return huidig_minimum[1], huidig_minimum[0]

        return deeloplossing, self.GetDistanceSum(deeloplossing)

    def GetDistanceSum(self, deeloplossing):
        afstand = 0

        for index, positie in enumerate(deeloplossing):
            if index == len(deeloplossing)-1:
                volgende = deeloplossing[0]
            else:
                volgende = deeloplossing[index+1]

            afstand += afstandsmatrix[positie][volgende]

        return afstand

    def GetTemperature(self, iteratie):
        # formule om de temperatuur te berekenen, nodig om de kans om alsnog te accepteren
        T = ( 0.5 * self._iteraties) / (2 ** int(iteratie/(self._iteraties/25))) * (1 - iteratie/self._iteraties)
        return T

    def GetAcceptingChance(self, mogelijkheidSom, origineleSom, iteratie):
        # genereert een kans of we alsnog de slechtere mogelijkheid accepteren
        x = (origineleSom - mogelijkheidSom)/self.GetTemperature(iteratie)
        kans = math.e ** x
        randnum = random.random()
        if randnum <= kans:
            return True
        else:
            return False

def main(actieve_punten):
    global solver
    for _ in range(aantal_wagens - 1):
        actieve_punten.append(0) # voor elke extra wagen, hebben we een extra startpunt nodig
    solver = Solver(actieve_punten)
    print(solver.solveOnce())

if __name__ == "__main__":
    actieve_punten = [x for x in range(int(len(afstandsmatrix)/3))]
    main(actieve_punten)