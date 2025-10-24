# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Auteur : gpotel
"""

import random as rd
import copy as cp
import numpy as np 



class Grille():
    def __init__(self, taille):
        self.taille = taille
        self.grille = np.zeros((self.taille,self.taille))
        self.bloquee = np.zeros((self.taille,self.taille))
    
    def en_matrice(self, matrice, marque_bloquees):
        self.grille = np.array(matrice)
        if marque_bloquees:
            self.bloquee = self.grille != 0
    
    def en_cases(self):
        return [[Case(self.grille[i,j], self.bloquee[i,j]) for i in range(self.taille)] for j in range(self.taille)]
    
    def en_liste(self):
        return self.grille.tolist()
    
    def est_correct(ligne, colonne, valeur):
        if self.bloquee[ligne, colonne]:
            return False
        if valeur in self.grille[ligne, :]:
            return False
        if valeur in self.grille[:, colonne]:
            return False
        #IMPLEMENTER LA VERIFICATION POUR LA CASE AUSSI (pour l'instant je vois pas trop comment faire^^)
        
        
        return True
        #Vérifie si un coup est correct
    
    def completer_case(self, ligne, colonne, valeur):
        if self.bloquee[ligne, colonne]:
            return False
        if valeur == 0:
            self.grille[ligne, colonne] = 0
            return True
        if self.est_correct(ligne, colonne, valeur):
            self.grille[ligne, colonne] = valeur
            return True
        return False
        #Permet d'ajouter des annotations dans une case (comme sur les applications de sudoku)
    
    def est_complete(self):
        return self.find_empty() is None
        #Ajoute le chiffre voulu dans la case sélectionnée par le joueur
    
    def set_difficulte():
        pass
        #Permet de sélectionner une difficulté (le nombre de chiffres initialement présents sur la grille)
    
    def case_vide(self):
        vide = np.argwhere(self.grille == 0)
        if vide.size:
            return tuple(result[0])
        else:
            return None
    
    


class Case():
    def __init__(self, valeur, bloquee, annotations):
        self.valeur = valeur
        self.bloquee = bloquee
        self.annotations = annotations
        
    def set_valeur(self, valeur):
        if not self.affichee:
            self.valeur = valeur
        #Complète la case avec le chiffre voulu par le joueur
    
    def vider(self):
        if not self.bloquee:
            self.valeur = 0
        #Vide la case
    
    def est_vide(self):
        self.valeur = 0
        #Vérifie si la case est vide ou non

    def set_annotation():
        pass
        #Annote la case avec le chiffre voulu par le joueur



class GenerateurSudoku():
    def generer_grille():
        pass
        #Génère la grille pleine
    
    def retirer_case(difficulte):
        pass
        #Retire un certain nombre de cases selon la difficulté



class ResolveurSudoku():
    def __init__(self, grille):
        self.grille = grille
    
    def resoudre(self):
        vide = self.grille.case_vide()
        if not vide:
            return True
        ligne, colonne = vide
        
        for chiffre in range(1, 10):
            if self.grille.est_correct(ligne, colonne, chiffre):
                self.grille.grille[ligne, colonne] = chiffre
                if self.resoudre():
                    return True
                self.grille.grille[ligne, colonne] = 0
        return False
        #
    


class Jeu():
    def __init__(self, grille_initiale):
        self.grille = Grille()
        if grille_initiale is not None:
            self.grille.en_matrice(grille_initiale)
        self.resolveur = ResolveurSudoku(self.grille)
    
    def resoudre(self):
        print("Résolution en cours \n")
        if self.resolveur.solve():
            print("Sudoku résolu")
            print(self.grille)
        else:
            print("Aucune solution trouvée ... :(")
    
    def montrer():
        print(self.grille)



#Ajouter des fonctions pour print ce qu'il faut
#Ajouter des spécifications de type pour clarifier le code
#Ajouter une méthode pour copier la grille à l'initialisation ?



if __name__ == "__main__":
    pass