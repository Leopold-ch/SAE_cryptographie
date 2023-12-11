"""
Fichier contenant les differentes fonction de chiffrement et de dechiffrement et le main
"""

from fonction_utiles_partie_1 import *
import simplified_des as sdes


def chiffrer_texte(texte, cle1, cle2):
    """fonction de chiffrement d'un texte grâce au double SDES

    Args:
        texte (str): chaîne de caractères
        cle1 (int): comprise entre 0 et 255 inclus;
            clé utilisée pour chiffrer chaque caractère du texte une première fois
        cle2 (int): comprise entre 0 et 255 inclus;
            clé utilisée pour chiffrer chaque caractère du texte une seconde fois

    Returns:
        str: texte chiffré
    """
    texte_chiffre = ""
    for carac in texte:
        carac_numerique = ord(carac) #conversion du caractère en code ascii
        carac_simplement_chiffre = sdes.encrypt(cle1, carac_numerique) #chiffrement du code ascii
        carac_doublement_chiffre = sdes.encrypt(cle2, carac_simplement_chiffre) #second chiffrement
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


def cassage_astucieux(message_clair, message_chiffre):
    """fonction de cassage brutal mais de façon astucieuse

    Args:
        message_clair (str): message en clair
        message_chiffre (str): message chiffré

    Returns:
        tuple: couple de clés de chiffrement (-1 si clé non trouvée)
    """
    for cle1 in range(256):
        for cle2 in range(256):
            texte_chiffre = ""
            carac_connus = {}
            for carac in message_clair:
                if carac not in carac_connus:
                    #conversion du caractère en code ascii
                    carac_numerique = ord(carac)

                    #chiffrement du code ascii
                    carac_simplement_chiffre = sdes.encrypt(cle1, carac_numerique)

                    #second chiffrement
                    carac_doublement_chiffre = sdes.encrypt(cle2, carac_simplement_chiffre)
                    carac_chiffre = chr(carac_doublement_chiffre)
                    texte_chiffre += carac_chiffre
                    carac_connus[carac] = carac_chiffre
                else:
                    texte_chiffre += carac_connus[carac]

            if texte_chiffre == message_chiffre:
                return (cle1, cle2)

    return (-1, -1)


#scénario de démonstration
if __name__ == '__main__':

    import time

    #liste des fichiers manipulables
    fichiers = ["arsene_lupin_extrait.txt", "lettres_persanes.txt"]

    #initialisation du texte et des clés utilisés pour l'experience
    mon_texte = ouvrir_fichier(fichiers[0])
    MA_CLE_1 = 0b10000110   #en base 10 : 134
    MA_CLE_2 = 0b10101101   #en base 10 : 173

    print('Texte à traiter :\n\n' + mon_texte)

    mon_texte_chiffre = chiffrer_texte(mon_texte, MA_CLE_1, MA_CLE_2)
    print("\n\nTexte chiffré :\n\n" + mon_texte_chiffre)

    #cassage des clés par force brute
    print('\n\nCassage en cours ...')
    debut = time.time()
    cles_cassage_brutal = cassage_brutal(mon_texte, mon_texte_chiffre)
    fin = time.time()
    temps_ecoule = int(fin - debut)
    print('Clés issues du cassage brutal :', cles_cassage_brutal[0], cles_cassage_brutal[1])
    print('Temps écoulé :', temps_ecoule, 'secondes')
    print("Clés correctes :", cles_cassage_brutal == (MA_CLE_1, MA_CLE_2))

    #cassage des clés par cassage astucieux
    print('\nCassage en cours ...')
    debut = time.time()
    cles_cassage_astucieux = cassage_astucieux(mon_texte, mon_texte_chiffre)
    fin = time.time()
    temps_ecoule = int(fin - debut)
    print('Clés issues du cassage astucieux :',
          cles_cassage_astucieux[0], cles_cassage_astucieux[1])
    print('Temps écoulé :', temps_ecoule, 'secondes')
    print("Clés correctes :", cles_cassage_astucieux == (MA_CLE_1, MA_CLE_2))
