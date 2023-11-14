import os
import pygame
from pygame.locals import *

# Initialisation de pygame
pygame.init()

# Définir la taille de la fenêtre et le titre
fen_largeur = 780
fen_hauteur = 500
pygame.display.set_caption("Anti-Virus")
pygame.mouse.set_visible(True)
font = pygame.font.Font(None, 36)

# Création de la surface d'arrière-plan
background_size = (fen_largeur, fen_hauteur)
background = pygame.display.set_mode(background_size)
background_rect = Rect(0, 0, *background_size)

# Chargement de l'image de fond
fond = pygame.image.load("Assets/backgroundPlay.jpg").convert()
fond = fond.convert()

# Classe pour les BLOCS
class Bloc(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/obstacle.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = (479, 233)  # Coordonnées du point central
        self.image = pygame.transform.scale(self.image, (101, 91))  # (141,131):(101, 91)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = (563, 313)

    def check_collision(self, virus_sprites):
        # Vérifie les collisions avec d'autres virus (sprites)
        collision_list = pygame.sprite.spritecollide(self, virus_sprites, False)
        for sprite in collision_list:
            if sprite != self:
                self.rect.centerx += -50
                self.rect.centery += -50


# Classe pour le sprite VirusRose
class VirusRose(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Pink_2.png")
        self.rect = self.image.get_rect()
        self.rect.x = 190
        self.rect.y = 160
        self.image = pygame.transform.scale(self.image, (245, 100))  # (285,140):(245, 100)
        self.dragging = False
        self.rect.center = (190 + self.rect.width / 2, 160 + self.rect.height / 2)  # Définir le point central
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 0 <= mouse_x <= fen_largeur and 0 <= mouse_y <= fen_hauteur:
                self.rect.center = (mouse_x, mouse_y)
        if not self.dragging:
            self.old_pos = self.rect.center  # Mémorise la position précédente

    def check_collision(self, virus_sprites):
        # Vérifie les collisions avec d'autres virus (sprites)
        collision_list = pygame.sprite.spritecollide(self, virus_sprites, False)
        for sprite in collision_list:
            if sprite != self:
                # Empêche le déplacement si une collision est détectée
                self.rect.center = self.old_pos  # Rétablit la position précédente

# Classe pour le sprite VirusRouge
class VirusRouge(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Virus.png")
        self.rect = self.image.get_rect()
        self.rect.x = 405
        self.rect.y = 385
        self.image = pygame.transform.scale(self.image, (175, 173))  # (215, 213):(175, 173)
        self.dragging = False
        self.rect.center = (405 + self.rect.width / 2, 385 + self.rect.height / 2)  # Définir le point central
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 0 <= mouse_x <= fen_largeur and 0 <= mouse_y <= fen_hauteur:
                self.rect.center = (mouse_x, mouse_y)
        if not self.dragging:
            self.old_pos = self.rect.center  # Mémorise la position précédente

    def check_collision(self, virus_sprites):
        # Vérifie les collisions avec d'autres virus (sprites)
        collision_list = pygame.sprite.spritecollide(self, virus_sprites, False)
        for sprite in collision_list:
            if sprite != self:
                # Empêche le déplacement si une collision est détectée
                self.rect.center = self.old_pos  # Rétablit la position précédente

#######################################################################################################
#######################################################################################################
#######################################################################################################

# Création d'un groupe de sprites
sprites = pygame.sprite.Group()
bloc = Bloc()
virusrose = VirusRose()
virusrouge = VirusRouge()
sprites.add(virusrose, virusrouge, bloc)

# Variables pour suivre l'Etat de "dragging" pour chaque virus
dragging_virusrose = False
dragging_virusrouge = False

# variable
active_sprite = None

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            print("Fermeture de jeu")

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if virusrose.rect.collidepoint(event.pos):
                    virusrose.dragging = True
                    active_sprite = virusrose
                elif virusrouge.rect.collidepoint(event.pos):
                    virusrouge.dragging = True
                    active_sprite = virusrouge

        if event.type == MOUSEMOTION:  # Vérifie si l'événement est de type MOUSEMOTION
            if active_sprite:
                active_sprite.rect.center = event.pos

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if active_sprite:
                    active_sprite.dragging = False
                    active_sprite = None

     # Obtenir la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Créer le texte pour afficher la position de la souris

    mouse_text = font.render("Position de la souris : ({}, {})".format(mouse_x, mouse_y), True, (255, 255, 255))
    # Créer le texte pour afficher la position du sprite "Bloc"
    bloc_text = font.render("Position du Bloc : ({}, {})".format(bloc.rect.x, bloc.rect.y), True, (255, 255, 255))

    # Affichage de l'arrière-plan
    background.blit(fond, (0, 0))

    # Mise à jour des sprites
    sprites.update()

    # Appeler la méthode check_collision pour chaque virus avec le groupe de sprites "sprites"
    virusrose.check_collision(sprites)
    virusrouge.check_collision(sprites)
    bloc.check_collision(sprites)
    # Affichage des sprites
    sprites.draw(background)

    # Afficher



