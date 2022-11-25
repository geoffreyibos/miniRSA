import random 
 
# Calcule un modulo d'une puissance de manière optimisée
def puissance (a,e,n):
  p = a
  res = 1
  while(e>0):
    if (e % 2):
      res = (res*p)%n
    p = p*p%n
    e = e//2
  return res

# Test si l'entier n en paramètre est premier
def test_premier(n):
    if(n == 2 or n == 3 or n == 5 or n == 7 or n == 11 or n == 13):
        return 1
    if((puissance(2,n-1,n) == 1)and
        (puissance(3,n-1,n) == 1) and
        (puissance(3,n-1,n) == 1) and
        (puissance(5,n-1,n) == 1) and
        (puissance(7,n-1,n) == 1) and
        (puissance(11,n-1,n) == 1) and
        (puissance(13,n-1,n) == 1)):
        return 1
    return 0
 # Renvoie le pgcd de a et b   
def pgcd(a,b):
    while(b):
        t = a
        a = b
        b = t%a
    return a
# Théorème de Bézout 

def bezout(a,b):
    p = 1
    q = 0
    r = 0
    s = 1
    while(b):
        c = a%b
        quotient = a//b
        a = b
        b = c
        nouveau_r = p-quotient*r
        nouveau_s = q-quotient*s
        p = r
        q = s
        r = nouveau_r
        s = nouveau_s
    return (p,q)
# Génération d'une clé publique et d'une clé privée

def creation_cle():
    p = random.randint(2**127,2**128)
    while(test_premier(p)==0):
        p = random.randint(2**127,2**128)
    q = random.randint(2**127,2**128)
    while(test_premier(q)==0):
        q = random.randint(2**127,2**128)
    n = p*q
    φ = (p-1)*(q-1)
    e = random.randint(1,φ)
    while(pgcd(e,φ)!=1):
        e = random.randint(1,φ)
    d = bezout(e,φ)[0]%φ  
    clé_public = [e,n]
    clé_privé = [d,n]
    return clé_public,clé_privé

def creation_cle_CA():
    p = random.randint(2**128,2**129)
    while(test_premier(p)==0):
        p = random.randint(2**128,2**129)
    q = random.randint(2**128,2**129)
    while(test_premier(q)==0):
        q = random.randint(2**128,2**129)
    n = p*q
    φ = (p-1)*(q-1)
    e = random.randint(1,φ)
    while(pgcd(e,φ)!=1):
        e = random.randint(1,φ)
    d = bezout(e,φ)[0]%φ  
    clé_public = [e,n]
    clé_privé = [d,n]
    return clé_public,clé_privé

def chiffrement(m,cle_publique):
    e = cle_publique[0]
    n = cle_publique[1]
    return puissance(m,e,n)

def dechiffrement(c,cle_privée):
    d = cle_privée[0]
    n = cle_privée[1]
    return puissance(c,d,n) 
    
def signature_Empreinte(empreinte,clé_privée):
    d = clé_privée[0]
    n = clé_privée[1]
    return puissance(empreinte,d,n) 

def verif_Empreinte(empreinte,clé_public): 
    e = clé_public[0]
    n = clé_public[1]
    return puissance(empreinte,e,n) 
    
def verif_Empreinte_Juste(empreinte,m):
    return empreinte == hachage(m)

# Classe Personne
class Personne:
    def __init__(self, name):
        self.Prenom = name
        clé = creation_cle()
        self.cléPublique = clé[0]
        self.cléPrivée = clé[1]  

    def affiche(self):
        print(self.Prenom+" | clé privée: " + str(self.cléPublique) + " | clé publique: " + str(self.cléPrivée))

# Transforme un message de caractères en ascii
def string_to_ascii(message):
    ascii = ""  
    for carac in message:
        a = str(ord(carac))
        if(len(a)<3): 
            a = "0" + a
        ascii += a
    return int(ascii)

# Transforme un message en ascii en caractères
def ascii_to_string(messageNombre):
    ascii = str(messageNombre)
    if len(ascii)%3!=0:
        ascii = "0" + ascii
    message = ""
    for i in range(0, len(ascii), 3):
        message += chr(int(ascii[i]+ascii[i+1]+ascii[i+2]))      
    return message


def hachage(message):
    m = message /2
    m = message +(25635*message%5) + len(str(message))
    return m%15986
