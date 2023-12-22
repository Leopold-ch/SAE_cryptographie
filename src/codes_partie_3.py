from scapy.all import *

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
