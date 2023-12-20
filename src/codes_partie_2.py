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