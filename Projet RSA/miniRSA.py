import fonctions as f
import colorama
from colorama import Fore
# $ pip3 install colorama

print()
# Création des acteurs du dialogue
Alice = f.Personne("Alice")
Bob = f.Personne("Bob")
CA = f.Personne("CA")
# Redéfinition de la clé du CA pour éviter les bugs
cles_CA = f.creation_cle_CA()
CA.cléPublique=cles_CA[0]
CA.cléPrivée=cles_CA[1]

Bob.affiche()
Alice.affiche()
CA.affiche()
print()

print(Fore.GREEN + "--------------------------------------------------------------------------------------------")
print("Dialogue entre Alice & le CA\n" + Fore.RESET)

print(Fore.YELLOW + "[Alice] Hachage de sa clé publique\n" + Fore.RESET)
empreinte_Alice = f.hachage(Alice.cléPublique[0]),f.hachage(Alice.cléPublique[1])

print(Fore.YELLOW + "[Alice] Signature de son empreinte \n" + Fore.RESET)
empreinte_Alice_Pour_CA = f.signature_Empreinte(empreinte_Alice[0], Alice.cléPrivée),f.signature_Empreinte(empreinte_Alice[1], Alice.cléPrivée)

print(Fore.YELLOW + "[Alice] Envoi du message chiffré au CA\n" + Fore.RESET)
message_Alice_Vers_CA = [f.chiffrement(Alice.cléPublique[0],CA.cléPublique),f.chiffrement(Alice.cléPublique[1],CA.cléPublique)] ,[empreinte_Alice_Pour_CA[0],empreinte_Alice_Pour_CA[1]]

# Envoie du message vers Le CA et le CA va maintenant vérifier l'empreinte

cle_Alice_chiffrée=message_Alice_Vers_CA[0]
empreinte_Alice_Chiffrée = message_Alice_Vers_CA[1]

print(Fore.RED + "[CA] Vérification de l'empreinte\n" + Fore.BLUE)
certificat_cléPublic_Alice = f.dechiffrement(cle_Alice_chiffrée[0],CA.cléPrivée),f.dechiffrement(cle_Alice_chiffrée[1],CA.cléPrivée)

# Vérification de l'empreinte par le CA
certificat_Empreinte_Alice_verif = f.verif_Empreinte(empreinte_Alice_Chiffrée[0],Alice.cléPublique),f.verif_Empreinte(empreinte_Alice_Chiffrée[1],Alice.cléPublique)

if(f.verif_Empreinte_Juste(certificat_Empreinte_Alice_verif[0],certificat_cléPublic_Alice[0]) and f.verif_Empreinte_Juste(certificat_Empreinte_Alice_verif[1],certificat_cléPublic_Alice[1])  ):
    print(Fore.RED + "[CA] L'empreinte est valide, envoie du certificat à Alice\n" + Fore.RESET)
    certificat_pour_Alice=f.chiffrement(Alice.cléPublique[0],CA.cléPrivée),f.chiffrement(Alice.cléPublique[1],CA.cléPrivée)
else:
    print(Fore.RED + "[CA] L'empreinte n'est pas valide\n" + Fore.RESET)


print(Fore.GREEN + "--------------------------------------------------------------------------------------------")
print("Dialogue entre Alice & Bob\n" + Fore.RESET)

# Envoi des clés publiques  
clé_publique_Bob = Bob.cléPublique
clé_publique_Alice = Alice.cléPublique

# Alice envoie un message chiffré à Bob avec la clé publique de Bob
message = str(input(Fore.YELLOW + "[Alice] Entrez le message que vous voulez envoyer à Bob :\n" + Fore.RESET))
message = f.string_to_ascii(message)

print(Fore.YELLOW + "\n[Alice] Chiffrement du message" + Fore.RESET)
message_chiffré_Alice = f.chiffrement(message,clé_publique_Bob)
print(Fore.WHITE + "Message chiffré : " + str(message_chiffré_Alice) +"\n" + Fore.RESET)

print(Fore.YELLOW + "[Alice] Création de l'empreinte")
empreinte_Alice = f.hachage(message)
print(Fore.WHITE + "Empreinte après hachage : " + str(empreinte_Alice) +"\n" + Fore.RESET)

print(Fore.YELLOW + "[Alice] Signature de l'empreinte\n" + Fore.RESET)
empreinte_signée_Alice = f.signature_Empreinte(empreinte_Alice, Alice.cléPrivée)

print(Fore.YELLOW + "[Alice] Envoi le message chiffré à Bob, son empreinte ainsi que le certificat\n" + Fore.RESET)
print(Fore.BLUE + "[Bob] Message reçu\n" + Fore.RESET)


# Oscar peut intervenir pour changer le message

attaque = str(input(Fore.MAGENTA + "[Oscar] Voulez-vous attaquer Alice en changeant son message vers Bob ? [oui/non]\n" + Fore.RESET))

if(attaque == "oui"):
    message_a_inserer = str(input(Fore.MAGENTA + "\n[Oscar] Quel message voulez vous insérer ?\n" + Fore.RESET))
    message_chiffré_Alice = f.string_to_ascii(message_a_inserer)
#------------------------------------------------------------------------

# Au tour de Bob
# Bob vérifie le certificat

print(Fore.BLUE + "\n[Bob] Vérification du message\n" + Fore.RESET)

dechiffrement_certificat_de_alice = f.dechiffrement(certificat_pour_Alice[0],CA.cléPublique), f.dechiffrement(certificat_pour_Alice[1],CA.cléPublique)

if(dechiffrement_certificat_de_alice[0]==clé_publique_Alice[0] and dechiffrement_certificat_de_alice[1]==clé_publique_Alice[1]):
    print(Fore.BLUE + "[Bob] Le certificat est correct\n" + Fore.RESET)
else:
    print(Fore.BLUE + "[Bob] Attention le certificat n'est pas correct , quelqu'un a du modifier le message\n" + Fore.RESET)

print(Fore.BLUE + "[Bob] Déchiffrement du message\n" + Fore.RESET)
message_dechiffré = f.dechiffrement(message_chiffré_Alice, Bob.cléPrivée)

message_recu = f.ascii_to_string(message_dechiffré)
print(Fore.BLUE + "[Bob] Le message reçu est : "+ Fore.RESET + message_recu + "\n")

# Bob vérifie l'empreinte d'Alice afin de savoir si le message n'a pas été modifié
Empreinte_verifiée = f.verif_Empreinte(empreinte_signée_Alice, clé_publique_Alice)

if(f.verif_Empreinte_Juste(Empreinte_verifiée, message_dechiffré)):
    print(Fore.GREEN + "=> Il s'agit du bon message\n" + Fore.RESET)
else:
    print(Fore.RED + "=> Attention ! Le message n'est pas celui d'origine, il a sûrement été modifié en cours de route\n")
print(Fore.GREEN + "Fin du dialogue entre Alice & Bob\n--------------------------------------------------------------------------------------------" + Fore.RESET)