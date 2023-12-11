"""
Ficher contenant des fonctions utiles à la première partie
"""

import simplified_des as sdes

def ouvrir_fichier(nom_fichier):
    """fonction de lecture d'un fichier afin d'en connaître le contenu

    Args:
        nom_fichier (str): nom du fichier à ouvrir

    Returns:
        str: contenu du fichier ouvert
    """
    contenu = ""
    with open(nom_fichier, 'r', encoding='utf-8') as file:
        for ligne in file.readlines():
            contenu += ligne
    return contenu


def dechiffrer_texte(texte_chiffre, cle1, cle2):
    """fonction de déchiffrement d'un texte chiffré grâce au double SDES

    Args:
        texte (str): chaîne de caractères
        cle1 (int): comprise entre 0 et 255 inclus; clé nécessaire au déchiffrement
        cle2 (int): comprise entre 0 et 255 inclus; clé nécessaire au déchiffrement

    Returns:
        str: texte déchiffré
    """
    texte_dechiffre = ""
    for carac in texte_chiffre:
        carac_numerique = ord(carac) #conversion du caractère en code ascii
        carac_simplement_chiffre = sdes.decrypt(cle2, carac_numerique) #chiffrement du code ascii
        carac_dechiffre = sdes.decrypt(cle1, carac_simplement_chiffre) #second chiffrement
        texte_dechiffre += chr(carac_dechiffre)
    return texte_dechiffre
