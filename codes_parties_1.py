import simplified_DES as sdes
from fonction_utiles_partie_1 import *


def chiffrer_texte(texte, cle1, cle2):
    """fonction de chiffrement d'un texte grâce au double SDES

    Args:
        texte (str): chaîne de caractères
        cle1 (int): comprise entre 0 et 255 inclus; clé utilisée pour chiffrer chaque caractère du texte une première fois
        cle2 (int): comprise entre 0 et 255 inclus; clé utilisée pour chiffrer chaque caractère du texte une seconde fois

    Returns:
        str: texte chiffré
    """
    texte_chiffre = ""
    for carac in texte:
        carac_numerique = ord(carac)    #conversion du caractère en code ascii
        carac_simplement_chiffre = sdes.encrypt(cle1, carac_numerique)     #chiffrement du code ascii
        carac_doublement_chiffre = sdes.encrypt(cle2, carac_simplement_chiffre)    #second chiffrement
        texte_chiffre += chr(carac_doublement_chiffre)
    return texte_chiffre


def cassage_brutal(message_clair, message_chiffre):
    """fonction de cassage brutal

    Args:
        message_clair (str): message en clair
        message_chiffre (str): message chiffré

    Returns:
        tuple: couple de clés de chiffrement (-1 si clé non trouvée)
    """
    for cle1 in range(256):
        for cle2 in range(256):
            if chiffrer_texte(message_clair, cle1, cle2) == message_chiffre:
                return (cle1, cle2)
    
    return (-1, -1)