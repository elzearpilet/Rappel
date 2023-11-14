from pygame import *
largeur, hauteur = 640, 550
fenetre = display.set_mode((largeur, hauteur))
display.set_caption('Tutoriel pygame')
init()

#les images
fond = image.load('backgroundPlay.jpg')
fond = fond.convert()

#les spritesheets

#paramètres de départ
jouer = True

#les fonctions du jeu

while jouer:
    for events in event.get():
         if events.type == QUIT:
             jouer=False
             quit()
    fenetre.blit(fond, (-150,-20))
    display.flip()

rouge = (255, 0, 0)

# Position et dimensions de l'antivirus
antivirus_x = largeur // 2
antivirus_y = hauteur - 50
antivirus_largeur = 50
antivirus_hauteur = 50

# Vitesse de l'antivirus
antivirus_vitesse = 5

# Liste pour stocker les positions des virus
virus_liste = []

# Fonction pour créer un virus
def creer_virus():
    x = random.randint(0, largeur - 50)
    y = 0
    virus_liste.append([x, y])

# Boucle principale du jeu
continuer = True
score = 0

horloge = pygame.time.Clock()

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    # Contrôles de l'antivirus
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT] and antivirus_x > 0:
        antivirus_x -= antivirus_vitesse
    if touches[pygame.K_RIGHT] and antivirus_x < largeur - antivirus_largeur:
        antivirus_x += antivirus_vitesse

    # Création aléatoire de virus
    if len(virus_liste) < 5:
        creer_virus()

    # Déplacement des virus
    for virus in virus_liste:
        virus[1] += 5

    # Supprimer les virus qui sont sortis de l'écran
    virus_liste = [virus for virus in virus_liste if virus[1] < hauteur]

    # Vérifier si un virus touche l'antivirus
    for virus in virus_liste:
        if antivirus_x < virus[0] < antivirus_x + antivirus_largeur and antivirus_y < virus[1] < antivirus_y + antivirus_hauteur:
            virus_liste.remove(virus)
            score += 1

    # Effacer l'écran
    fenetre.fill(blanc)

    # Dessiner l'antivirus
    pygame.draw.rect(fenetre, rouge, (antivirus_x, antivirus_y, antivirus_largeur, antivirus_hauteur))

    # Dessiner les virus
    for virus in virus_liste:
        pygame.draw.rect(fenetre, rouge, (virus[0], virus[1], 20, 20))

    pygame.display.update()
    horloge.tick(30)

pygame.quit()