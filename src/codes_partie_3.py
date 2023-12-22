from scapy.all import *
from codes_partie_2 import *
from cryptography.hazmat.primitives.ciphers import *
from cryptography.hazmat.primitives import *

def filtre_UDP(paquets):
    """fonction permettant, à partir d'un ensemble d'échanges réseau,
    d'en extraire ceux étant ayant une sous couche UDP

    Args:
        paquets (scapy.plist.PacketList): liste des paquets

    Returns:
        list: liste des paquet ayant une sous couche UDP
    """
    return [p for p in paquets if UDP in p]

def filtre_port(paquets_UDP, port_recherche):
    """fonction permettant de ne conserver que les paquets
    utilisant un port donné

    Args:
        paquets_UDP (scapy.plist.PacketList): liste de paquets ayant une sous couche UDP
        port_recherche (int): port de communication recherché

    Returns:
        list: liste des paquets passant par le port donné
    """
    try:
        return [p for p in paquets_UDP if p[UDP].dport == port_recherche]
    except IndexError:
        print("La liste des paquets en paramètre est incorrecte !")


def dechiffrement_plutotBonneConfidentialite(contenu_brut, chemin_image):
    """fonction de déchiffrement par AES en mode CBC (PKCS7)

    Args:
        contenu_brut (bytes): contenu brut du paquet
        chemin_image (str): chemin de l'image nécessaire pour trouver la clé de MrRobot

    Returns:
        bytes: contenu déchiffré
    """
    vecteur_initialisation = contenu_brut[:16]
    contenu_chiffre = contenu_brut[16:]
    cle = cle_MrRobot(chemin_image) * 4
    cle = int(cle, 2).to_bytes(32, byteorder="big")
    
    cipher = Cipher(algorithms.AES(cle), modes.CBC(vecteur_initialisation))
    decrypteur = cipher.decryptor()
    contenu_dechiffre = decrypteur.update(contenu_chiffre) + decrypteur.finalize()

    sans_padding = padding.PKCS7(128).unpadder()
    contenu_dechiffre_sans_padding = sans_padding.update(contenu_dechiffre) + sans_padding.finalize()

    return contenu_dechiffre_sans_padding

if __name__ == '__main__':
        
    paquets_extraits = rdpcap("trace_sae.cap") #echanges_reseau/
    port_alice_bob = 9999
    paquets_UDP = filtre_UDP(paquets_extraits)
    paquets_filtres = filtre_port(paquets_UDP, port_alice_bob)

    for num, message in enumerate(paquets_filtres):
        
        contenu_brut = bytes(message[UDP].payload)

        message_dechiffre = dechiffrement_plutotBonneConfidentialite(contenu_brut, "rossignol2.bmp") #images/
        
        print("\n\nMessage n°", num+1, ':\t',  message.summary())
        print("\nMessage déchiffré :", message_dechiffre.decode(), "\n")

