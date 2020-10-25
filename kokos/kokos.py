#!/usr/bin/env python3
class Kokos(object):
    def __init__(self, sailors = 5):
        self.sailors = sailors
        self.parts = [ (0) for _ in range(self.sailors + 1)]
        self.rest = [ (0) for _ in range(self.sailors + 1)]
    def __str__(self):
        return """
Kokosnüsse teilem:

Es dreht sich um N (Vorgabe N = 5) schiffbrüchige Seeleute, die mit ihrem Maskottchen, einem Affen, auf eine einsame Insel verschlagen wurden.
Da sie sehr hungrig waren, schickten sie sich an, Kokosnüsse zu sammeln. Als sie einen recht großen Haufen Kokosnüsse zusammen hatten,
waren sie jedoch so müde, dass sie sich entschlossen, die Teilung der Nüsse auf den nächsten Morgen zu verschieben und erst einmal ordentlich auszuschlafen.
Während der Nacht wachte einer der Seeleute auf und entschlosss ich, den ihm zustehenden Teil zunächst einmal sicherzustellen.
Er teilte also die vorhandenen Kokosnüsse in N gleiche Teile und verbarg seinen Anteil im Laub.
Bei der Teilung stellte er fest, dass eine Kokosnuss übriggeblieben war, die er dem Affen zuteilte. Dann legte er sich wieder schlafen.
Eine Stunde später wachte der zweite Seemann auf, und auch er wollte seinen Teil sicherstellen.
Das Ganze wiederholte sich N mal.
Am nächsten Morgen, als die Seeleute aufwachten, hatte jeder ein schlechtes Gewissen, und es wurde daher über die stark verringerte Anzahl
der noch vorhandenen Kokosnüsse kein weiteres Wort verloren.
Sie teilten den verbliebenen Rest und diesmal blieb keine Nuss übrig.

Wieviel Kokosnüsse hatten die Seeleute gesammelt?""" 

    def calc(self):
        self.rest[0] = self.sailors
        isSolution = False
        while not isSolution:
            self.rest[0] += 1
            for loop in range(1, self.sailors + 1):
                pr = self.rest[loop - 1]
                if pr % self.sailors != 1:
                    break
                self.parts[loop] = pr // self.sailors
                self.rest[loop] = pr - self.parts[loop] - 1
                isSolution = (loop == self.sailors) and (self.rest[self.sailors] % self.sailors == 0)
        for loop in range(1, self.sailors + 1):
            print("{:d}.Seemann:{:6d}{:>18}{:>20}{:6d}".format(loop, self.parts[loop], 'Affe: 1', 'Teilsumme:', self.parts[loop] + 1))
        print("\n{:54s}{:6d}".format('Heimliche Teilung:', sum(self.parts) + self.sailors))
        print("{:54s}{:6d}".format('Verbliebener Rest:',self.rest[self.sailors]))
        print("{:54s}{:6d}".format('G e s a m t:',self.rest[0]))

kokos = Kokos()
kokos.calc()

