from bs4 import BeautifulSoup

def extraire_donnees_html(fichier_html):
    with open(fichier_html, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()

    soup = BeautifulSoup(contenu, 'html.parser')
    
    # Exemple : extraction de tous les liens
    liens = [a['href'] for a in soup.find_all('a', href=True)]

    return liens

# Utiliser le nom de votre fichier HTML
chemin_fichier_html = '/home/deathoftitan/Documents/Cours EPITA/Python/PAGE PHISHING/Roll20.html'
liens_extraits = extraire_donnees_html(chemin_fichier_html)

print(liens_extraits)
