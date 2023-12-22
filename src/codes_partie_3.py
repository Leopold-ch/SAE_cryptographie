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
