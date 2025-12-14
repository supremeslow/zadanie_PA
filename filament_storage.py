from abc import ABC, abstractmethod

# Sklad filamentov 
class Filament:
    def __init__(self, farba: str, hmotnost: float):
        self.farba = farba
        self.hmotnost = hmotnost  # v gramoch
        self.cena_za_gram = 0.02  # x eur za gram

    def cena(self, pouzite_gramy: float):
        return pouzite_gramy * self.cena_za_gram

    def __str__(self):
        return f"{self.farba} filament ({self.hmotnost}g zostava)"

class SkladFilamentov:
    def __init__(self):
        self.filamenty = []

    def pridaj_filament(self, filament: Filament):
        self.filamenty.append(filament)
        print(f"Pridany {filament} do skladu.")

    def pouzi_filament(self, farba: str, hmotnost: float):
        for f in self.filamenty:
            if f.farba == farba and f.hmotnost >= hmotnost:
                f.hmotnost -= hmotnost
                cena = f.cena(hmotnost)
                print(f"Pouzite {hmotnost}g {farba} filamentu. Cena: {cena:.2f}€")
                if f.hmotnost == 0:
                    self.filamenty.remove(f)
                return hmotnost
        print(f"Nedostatok {farba} filamentu!")
        return 0

    def vypis_filamenty(self):
        if not self.filamenty:
            print("V sklade nie su ziadne filamenty.")
        for f in self.filamenty:
            print(f)

#Odpad zo supportov 
class Odpad:
    def __init__(self):
        self.hmotnost_podpory = 0.0

    def pridaj_podporu(self, hmotnost: float):
        self.hmotnost_podpory += hmotnost
        print(f"Pridanych {hmotnost}g podpory do odpadu.")

    def vypis_odpad(self):
        print(f"Celkova hmotnost podpory v odpade: {self.hmotnost_podpory}g")


class Tlacenie(ABC):
    def __init__(self, nazov: str, farba_filamentu: str, hmotnost_filamentu: float):
        self.nazov = nazov
        self.farba_filamentu = farba_filamentu
        self.hmotnost_filamentu = hmotnost_filamentu

    @abstractmethod
    def vytlac(self, sklad: SkladFilamentov, odpad: Odpad):
        pass

class Model(Tlacenie):
    def __init__(self, nazov: str, farba_filamentu: str, hmotnost_filamentu: float, hmotnost_podpory: float = 0, cas_tlace_hodiny: float = 1.0):
        super().__init__(nazov, farba_filamentu, hmotnost_filamentu)
        self.hmotnost_podpory = hmotnost_podpory
        self.cas_tlace_hodiny = cas_tlace_hodiny  

    def vytlac(self, sklad: SkladFilamentov, odpad: Odpad):
        print(f"Tlac modelu {self.nazov}...")
        pouzite = sklad.pouzi_filament(self.farba_filamentu, self.hmotnost_filamentu)
        if pouzite > 0 and self.hmotnost_podpory > 0:
            odpad.pridaj_podporu(self.hmotnost_podpory)
        print(f"Cas tlace: {self.cas_tlace_hodiny} hodin\n")
        print("--- Zostatok vo sklade ---")
        sklad.vypis_filamenty()
        print("--------------------------\n")

def main():
    sklad = SkladFilamentov()
    odpad = Odpad()

    # Pridanie filamentov
    sklad.pridaj_filament(Filament("Cerveny", 500))
    sklad.pridaj_filament(Filament("Modry", 300))
    sklad.pridaj_filament(Filament("Zeleny", 200))

    # Vytvorenie tlacovych uloh
    ulohy = [
        Model("Kocka", "Cerveny", 100, hmotnost_podpory=10, cas_tlace_hodiny=2.0),
        Model("Gula", "Modry", 50, hmotnost_podpory=5, cas_tlace_hodiny=1.5),
        Model("Pyramida", "Cerveny", 200, cas_tlace_hodiny=3.0),
        Model("Pologula", "Zeleny", 150, cas_tlace_hodiny=2.5)
    ]

    # Tlac vsetkych uloh
    for uloha in ulohy:
        uloha.vytlac(sklad, odpad)

    print("\n--- Stav odpadu ---")
    odpad.vypis_odpad()

if __name__ == "__main__":
    main()