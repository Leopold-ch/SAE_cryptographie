from codes_partie_1 import *
from cryptography.fernet import Fernet
from PIL import Image


def chiffrement_AES(texte):
    """fonction de chiffrement reposant sur l'algorithme d'AES

    Args:
        texte (str): texte à chiffrer

    Returns:
        tuple: couple clé - texte chiffré
    """
    cle = Fernet.generate_key()
    fernet = Fernet(cle)
    texte_chiffre = fernet.encrypt(bytes(texte, "utf-8"))

    return cle, texte_chiffre


def dechiffrement_AES(texte_chiffre, cle):
    """fonction de déchiffrement de texte chiffré grâce à AES

    Args:
        texte_chiffre (bytes): texte chiffré
        cle (bytes): clé utilisée pour chiffrer le texte

    Returns:
        str: texte déchiffré
    """
    fernet = Fernet(cle)
    texte_dechiffre = fernet.decrypt(texte_chiffre)

    return texte_dechiffre.decode()


def cle_MrRobot(nom_image):
    """fonction d'obtention de la clé de MrRobot

    Args:
        nom_image (str): lien de l'image contenant la clé

    Returns:
        bytes: chaîne de 64 bits
    """
    cle = ""
    image = Image.open(nom_image)
    pixels = list(image.getdata())

    for i in range(64):
        couleur = pixels[i]
        cle += str(couleur % 2)
    
    return bytes(cle, 'utf-8')



if __name__ == '__main__':
    
    import time
    import random
    
    mon_texte = ouvrir_fichier("textes/lettres_persanes.txt")
    
    #mesure du temps de chiffrement/déchiffrement avec SDES
    mesures_chiffrement = []
    mesures_dechiffrement = []
    print('Mesures en cours ...')
    for _ in range (100):
        cle1 = random.randint(0, 255)
        cle2 = random.randint(0, 255)
        
        debut = time.time()
        mon_texte_chiffre = chiffrer_texte(mon_texte, cle1, cle2)
        fin = time.time()
        temps_ecoule = round(fin - debut, 5)
        mesures_chiffrement.append(temps_ecoule)
        
        debut = time.time()
        dechiffrer_texte(mon_texte_chiffre, cle1, cle2)
        fin = time.time()
        temps_ecoule = round(fin - debut, 5)
        mesures_dechiffrement.append(temps_ecoule)
        
    
    temps_moyen_chiffrement_SDES = sum(mesures_chiffrement) / len(mesures_chiffrement)
    temps_moyen_dechiffrement_SDES = sum(mesures_dechiffrement) / len(mesures_dechiffrement)
    print("Le temps moyen pour chiffrer lettres_persanes.txt avec SDES est de", round(temps_moyen_chiffrement_SDES, 5), "secondes.")
    print("Le temps moyen pour déchiffrer lettres_persanes.txt avec SDES est de", round(temps_moyen_dechiffrement_SDES, 5), "secondes.")
    
    #mesure du temps de chiffrement/déchiffrement avec AES
    mesures_chiffrement = []
    mesures_dechiffrement = []
    print('\nMesures en cours ...')
    for _ in range (100):
        debut = time.time()
        cle, mon_texte_chiffre = chiffrement_AES(mon_texte)
        fin = time.time()
        temps_ecoule = round(fin - debut, 5)
        mesures_chiffrement.append(temps_ecoule)
        
        debut = time.time()
        dechiffrement_AES(mon_texte_chiffre, cle)
        fin = time.time()
        temps_ecoule = round(fin - debut, 5)
        mesures_dechiffrement.append(temps_ecoule)
        
    
    temps_moyen_chiffrement_AES = sum(mesures_chiffrement) / len(mesures_chiffrement)
    temps_moyen_dechiffrement_AES = sum(mesures_dechiffrement) / len(mesures_dechiffrement)
    print("Le temps moyen pour chiffrer lettres_persanes.txt avec AES est de",  round(temps_moyen_chiffrement_AES, 5), "secondes.")
    print("Le temps moyen pour déchiffrer lettres_persanes.txt avec AES est de",  round(temps_moyen_dechiffrement_AES, 5), "secondes.")
    
    print("\n\nLe plus rapide pour chiffrer est donc", ("SDES" if temps_moyen_dechiffrement_SDES < temps_moyen_dechiffrement_AES else "AES"))
    print("et pour déchiffrer, il s'agit de", ("SDES" if temps_moyen_dechiffrement_SDES < temps_moyen_dechiffrement_AES else "AES"))


    #affichage de la clé de MrRobot
    cle_de_MrRobot = cle_MrRobot("images/rossignol2.bmp")
    print("\n\n\n+", "-"*24, "Clé de MrRobot", "-"*24, "+")
    print("|", cle_de_MrRobot.decode(), "|")
    print("+", "-"*64, "+")
