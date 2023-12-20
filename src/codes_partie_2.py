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