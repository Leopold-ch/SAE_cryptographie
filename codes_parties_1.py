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
