import random
import numpy as np
import json

class rsa():
    def __init__(self):
        pass
    
    def encrypt(self, message_to_encrypt: list, key: dict) -> list:

        # Jede Zahl der Liste wird mit dem Schlüssel verschlüsselt, welcher als Parameter übergeben wird.
        # Der Liste message_encrypted werden die neuen Werte zugeschrieben.
        message_encrypted = []
        for i in message_to_encrypt:
           message_encrypted.append(pow(int(i), key["a"], key["n"]))
        return message_encrypted

    def decrypt(self, message_to_decrypt: list, key: dict) -> list:
        # B wird generiert, da dieser Teil des Schlüssels noch nicht in dem Dictionary enthalten ist.
        b = self.extended_euclidean_algorithm([key["m"], 1, 0], [key["a"] , 0, 1])
        
        # Hier wird dann die Formel zur Entschlüsselung auf alle Zahlen der Liste angewendet. 
        # 1 und 0 werden ohne diesen Prozess zurückgegeben, da sonst Fehler auftreten.
        message_decrypted = []
        for i in message_to_decrypt:
            if i == 0 or i == 1:
                message_decrypted.append(i)
            else:
                message_decrypted.append(pow(int(i), b, key["n"]))
        
        return message_decrypted
        
        
    
    def generate_key(self, __key_length_lower: int, __key_length_upper: int) -> dict:
        # Diese Funktion generiert ein Dictionary mit einem vollen Schlüssel (ausgeschlossen b)
        dict = self.generate_p_q_n_m(__key_length_lower, __key_length_upper)
        dict["a"] = self.generate_coprime(dict["m"])
        return dict

    
    
    def is_prime_MRT(self, p: int, k: int) -> bool:
        # Diese Funktion ruft den Miller Rabin Test eine gegebene Anzahl auf und prüft somit, ob es sich bei der Zahl p um eine Primzahl handelt.
        while k > 0:
            if self.Miller_Rabin_test(p) == False:
                return False
            k -= 1
            
        return True
    
    def Miller_Rabin_test(self, p: int) -> bool:
        # Der Miller Rabin Test prüft mit einer gewissen Wahrscheinlichkeit, ob es sich um eine Primzahl handelt.
        # Dieser Test ist wesentlich schneller als herkömmliche Primzahltests.
        d = p - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        a = random.randint(2, p - 1)
        x = pow(a, d, p)
        if x == 1 or x == p - 1:
            return True
        while r > 1:
            x = pow(x, 2, p)
            if x == 1:
                return False
            if x == p - 1:
                return True
            r -= 1
        return False

    

    def generate_prime_number(self, length: int) -> int:
        # Diese Funktion generiert eine Primzahl mit einer bestimmten Länge.
        # Die gegebene Zahl length generiert dann einen unteren Bereich und einen oberen Bereich zwischen dem die Primzahl generiert wird.
        # Es wird so oft eine zufällige Zahl generiert, bis sie den Miller Rabin Test besteht, es sich also um eine Primzahl handelt.
        a = "1"
        z = "9"
        for i in range(length):
            a += "0"
            z += "9"
        while True:
            number = random.randint(int(a), int(z))
            if self.is_prime_MRT(number, 8):
                return number

    def generate_p_q_n_m(self, lowerValue: int, upperValue: int) -> dict:
        # Diese Funktion generiert die Werte p, q, n und m. 
        # Diese Werte werden in einem Dictionary gespeichert und zurückgegeben.
        p = self.generate_prime_number(random.randint(lowerValue, upperValue))
        q = self.generate_prime_number(random.randint(lowerValue, upperValue))
        n = p * q
        m = (p - 1) * (q - 1)

        return {"p": p,"q": q,"n": n,"m": m}

    def euclidean_algorithm_is_one(self, a: int, n: int) -> bool:
        # Diese Funktion prüft, ob der größte gemeinsame Teiler von a und n 1 ist.
        # Wenn dies der Fall ist, dann handelt es sich um eine teilerfremde Zahl.
        if a == 1 and n == 0:
            return True
        elif n == 0:
            return False
        return self.euclidean_algorithm_is_one(int(n), int(int(a) % int(n)))


    def generate_coprime(self, n: int) -> int:
        # Diese Funktion generiert eine teilerfremde Zahl zu n.
        # Auch hier wird wieder eine zufällige Zahl generiert, bis diese die Prüfung besteht.
        while True:
            a = random.randint(2, n - 1)
            if self.euclidean_algorithm_is_one(a, n) == True:
                return a

    def extended_euclidean_algorithm(self, array1: list, array2: list):
        # Diese Funktion beinhaltet den erweiterten euklidischen Algorithmus.
        # Dieser Algorithmus wird benötigt, um das modulare Inverse von m zu a zu finden.
        # Es handelt sich hierbei um eine rekursive Funktion.
        # Dadurch können Probleme auftreten, wenn die maximale Rekursionstiefe erreicht wird.
        # Jedoch kann diese auch manuell in Python festgelegt werden.
        # Wenn der erste Wert in array2 1 ist, dann wird der dritte Wert in array2 zurückgegeben, also das modulare Inverse
        if array2[0] == 1:
            return int(array2[2])
        values1 = np.array(array1)
        values2 = np.array(array2)
        factor = values1[0] // values2[0]
        values2 = np.subtract(values1, np.multiply(factor, values2))
        return self.extended_euclidean_algorithm(array2, values2)
