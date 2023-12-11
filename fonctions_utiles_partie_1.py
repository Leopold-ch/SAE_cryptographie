import simplified_DES as sdes

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
