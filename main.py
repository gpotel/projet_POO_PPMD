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
    
    def dapres_matrice(self, matrice):
        self.grille = np.array(matrice)
        self.bloquee = self.grille != 0
    
    def en_cases(self):
        return [[Case(self.grille[i,j], self.bloquee[i,j]) for j in range(self.taille)] for i in range(self.taille)]
    
    def en_liste(self):
        return self.grille.tolist()
    
    def est_correct(self, ligne, colonne, valeur):
        if self.bloquee[ligne, colonne]:
            return False
        if valeur in self.grille[ligne, :]:
            return False
        if valeur in self.grille[:, colonne]:
            return False
        l, c = 3 * (ligne // 3), 3 * (colonne // 3)
        if valeur in self.grille[l:l+3, c:c+3]:
            return False
        return True
        #Vérifie si un coup est correct
    
    def completer_case(self, ligne, colonne, valeur):
        if self.bloquee[ligne, colonne]:
            return False
        if valeur == 0:
            return self.vider_case(ligne, colonne)
        if self.est_correct(ligne, colonne, valeur):
            self.grille[ligne, colonne] = valeur
            return True
        return False
        #Permet d'ajouter des annotations dans une case (comme sur les applications de sudoku)
    
    def vider_case(self, ligne, colonne):
        if self.bloquee[ligne, colonne]:
            return False
        self.grille[ligne, colonne] = 0
        return True
    
    def est_complete(self):
        return self.case_vide() is None
        
    
    def set_difficulte():
        pass
        #Permet de sélectionner une difficulté (le nombre de chiffres initialement présents sur la grille)
    
    def case_vide(self):
        vide = np.argwhere(self.grille == 0)
        if vide.size:
            return tuple(vide[0])
        else:
            return None
    
    def __str__(self):
        cases = self.en_cases()
        lignes = []
        for i, ligne in enumerate(cases):
            if i % 3 == 0 and i != 0:
                lignes.append("-" * 22)
            Ligne = []
            for j, case in enumerate(ligne):
                Ligne.append(str(case))
                if (j + 1) % 3 == 0 and j != 8:
                    Ligne.append("|")
            lignes.append(" ".join(Ligne))
        return "\n".join(lignes)
    


class Case():
    def __init__(self, valeur, bloquee, annotations=[]):
        self.valeur = valeur
        self.bloquee = bloquee
        self.annotations = set()
    
    def est_vide(self):
        return self.valeur == 0
        #Vérifie si la case est vide ou non
    
    def est_bloquee(self):
        return self.bloquee

    def ajouter_annotation(self, chiffre):
        if self.est_vide() and not self.est_bloquee() and 1 <= chiffre <= 9:
            self.annotations.add(chiffre)
        #Annote la case avec le chiffre voulu par le joueur
    
    def retirer_annotations(self, chiffre):
        self.annotations.discard(chiffre)
        
    def vider_annotations(self):
        self.annotations.clear()
    
    def set_valeur(self, valeur):
        if not self.est_bloquee():
            self.valeur = valeur
            self.vider_annotations()
    
    def __repr__(self):
        if self.valeur !=0:
            return str(int(self.valeur))
        elif self.annotations:
            return "(" + "".join(str(x) for x in sorted(self.annotations)) + ")"
        else:
            return "."

class GenerateurSudoku():
    def __init__(self, difficulte=40):
        self.difficulte = difficulte
        
    def generer_grille(self):
        grille = Grille(9)
        self._remplir_grille_aleatoire(grille)
        self._retirer_cases(grille)
        return grille
        #Génère la grille pleine
    
    def _remplir_grille_aleatoire(self, grille):
        chiffres = [1,2,3,4,5,6,7,8,9]
        
        def remplir_cases():
            vide = grille.case_vide()
            if not vide:
                return True
            ligne, colonne = vide
            rd.shuffle(chiffres)
            for chiffre in chiffres:
                if grille.est_correct(ligne, colonne, chiffre):
                    grille.grille[ligne, colonne] = chiffre
                    if remplir_cases():
                        return True
                    grille.grille[ligne, colonne] = 0
            return False
        
        remplir_cases()
        
        grille.bloquee[:, :] = True
    
    def _retirer_cases(self, grille, nb_tentative = 1000):
        cases_a_retirer = self.difficulte
        tentative = 0
        while cases_a_retirer > 0 and tentative < nb_tentative:
            ligne = rd.randint(0,8)
            colonne = rd.randint(0,8)
            if grille.grille[ligne, colonne] == 0:
                continue
            valeur_sauv = grille.grille[ligne, colonne]
            grille.grille[ligne, colonne] = 0
            grille.bloquee[ligne, colonne] = False
            
            copie = Grille(9)
            copie.dapres_matrice(cp.deepcopy(grille.grille))
            resolveur = ResolveurSudoku(copie)
            nb_solutions = self._compter_solutions(resolveur, limite=2)
            
            if nb_solutions != 1:
                grille.grille[ligne, colonne] = valeur_sauv
                grille.bloquee[ligne, colonne] = True
            else:
                cases_a_retirer -= 1
            tentative += 1
            # if grille.grille[ligne, colonne] != 0:
            #     grille.grille[ligne, colonne] = 0
            #     grille.bloquee[ligne, colonne] = False
            #     cases_a_retirer -= 1
    
    def _compter_solutions(self, resolveur, limite=2):
        solutions = [0]
        
        def backtrack():
            if solutions[0] >= limite:
                return
            vide = resolveur.grille.case_vide()
            if not vide:
                solutions[0]+=1
                return
            ligne, colonne = vide
            for chiffre in range(1, 10):
                if resolveur.grille.est_correct(ligne, colonne, chiffre):
                    resolveur.grille.grille[ligne, colonne] = chiffre
                    backtrack()
                    resolveur.grille.grille[ligne, colonne] = 0
        
        backtrack()
        return solutions[0]
    



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
    """     Version qui résoud automatiquement la grille
    def __init__(self, grille_initiale):
        self.grille = Grille(9)
        if grille_initiale is not None:
            self.grille.dapres_matrice(grille_initiale, True)
        self.resolveur = ResolveurSudoku(self.grille)
    
    def resoudre(self):
        print("Résolution en cours \n")
        if self.resolveur.resoudre():
            print("Sudoku résolu")
            print(self.grille)
        else:
            print("Aucune solution trouvée ... :(")
    
    def montrer(self):
        print(self.grille)
    """
    def __init__(self, grille_initiale):
        self.grille = Grille(9)
        if grille_initiale is not None:
            self.grille.dapres_matrice(grille_initiale)
        
        self.annotations = [[set() for i in range(9)] for j in range(9)]
            
    def montrer(self):
        print()
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 43)
            ligne_aff = []
            for j in range(9):
                val = int(self.grille.grille[i,j])
                if val != 0:
                    affichage = " " + str(val) + " "
                elif self.annotations[i][j]:
                    notes = "".join(str(x) for x in sorted(self.annotations[i][j]))
                    affichage = "{" + notes + "}"
                else:
                    affichage = " . "
                ligne_aff.append(affichage)
                if (j+1) % 3 == 0 and j != 8:
                    ligne_aff.append(" | ")
            print(" ".join(ligne_aff))
        print()
    
    def jouer_coup(self, ligne, colonne, valeur):
        if self.grille.bloquee[ligne, colonne]:
            print("\nLa case est fixée")
            return False
        if valeur == 0:
            print(f"\nEffacement ({ligne+1}, {colonne+1})")
            return self.retirer_coup(ligne, colonne)
        if not self.grille.est_correct(ligne, colonne, valeur):
            print(f"\n{valeur} ne peut pas être placée en ({ligne+1},{colonne+1})")
            return False
        self.grille.grille[ligne, colonne] = valeur
        carre_ligne = ligne // 3
        carre_colonne = colonne // 3
        for i in range(3):
            for j in range(3):
                ind_i = carre_ligne * 3 + i
                ind_j = carre_colonne * 3 + j
                print(ind_i, ind_j, self.annotations[ind_i][ind_j])
                if valeur in self.annotations[ind_i][ind_j]:
                    self.annotations[ind_i][ind_j].remove(valeur)
        print(f"\n{valeur} placé en ({ligne+1}, {colonne+1})")
        return True
    
    def retirer_coup(self, ligne, colonne):
        return self.grille.vider_case(ligne, colonne)
    
    def est_complete(self):
        return self.grille.est_complete()
    
    def annoter_case(self, ligne, colonne, chiffre):
        if self.grille.bloquee[ligne, colonne]:
            print("\nImpossible d'annoter une case fixée")
            return False
        if not (1 <= chiffre <= 9):
            print("\nLes annotations doivent être comprises entre 1 et 9")
            return False
        # if not (0<= ligne <= 8) and (0<= colonne <= 8):
        #     print("")
        notes = self.annotations[ligne][colonne]
        if chiffre in notes:
            notes.remove(chiffre)
            print(f"\nAnnotation {chiffre} retirée de ({ligne+1}, {colonne+1})")
        else:
            notes.add(chiffre)
            print(f"\nAnnotation {chiffre} ajoutée en ({ligne+1}, {colonne+1})")
        return True
        

#Ajouter des fonctions pour print ce qu'il faut
#Ajouter des spécifications de type pour clarifier le code
#Ajouter une méthode pour copier la grille à l'initialisation ?
# __str__ de grille tombe en désuétude par la modification de jeu.montrer()
#La classe Case() ne sert à rien en fait
#Nettoyer les annotations partout où elles ne servent plus

if __name__ == "__main__":
    generateur = GenerateurSudoku()
    grille_sudoku = generateur.generer_grille()
    
    jeu = Jeu(grille_sudoku.en_liste())
    print("Sudoku généré :\n")
    jeu.montrer()
    
    while not jeu.est_complete():
        entree = input('Ligne Colonne Valeur ("a Ligne Colonne Valeur" pour annoter, q pour quitter):').strip().lower()
        if entree in ("q", "quit", "exit"):
            print("\nVous avez quitté le jeu :(")
            break
        
        try:
            parties = entree.split()
            if parties[0] == "a" and len(parties) == 4:
                x, l, c, v = parties
                ligne, colonne, valeur = int(l)-1, int(c)-1, int(v)
                if not (0 <= ligne <= 8 and 0 <= colonne <= 8 and 0 <= valeur <= 9):
                    print("Vous avez dépassé les bornes ! 1-9 pour les cases, 1-9 pour les valeurs et 0 pour effacer")
                    continue
                jeu.annoter_case(ligne, colonne, valeur)
            else:
                ligne, colonne, valeur = map(int, parties)
                ligne -= 1
                colonne -= 1
                if not (0 <= ligne <= 8 and 0 <= colonne <= 8 and 0 <= valeur <= 9):
                    print("Vous avez dépassé les bornes ! 1-9 pour les cases, 1-9 pour les valeurs et 0 pour effacer")
                    continue
                jeu.jouer_coup(ligne, colonne, valeur)
                
        except ValueError:
            print("Format invalide : concentre toi")
            continue
        
        # if not (0 <= ligne <= 8 and 0 <= colonne <= 8 and 0 <= valeur <= 9):
        #     print("Vous avez dépassé les bornes ! 1-9 pour les cases, 1-9 pour les valeurs et 0 pour effacer")
        #     continue
        
        # success = jeu.jouer_coup(ligne, colonne, valeur)
        print("\n")
        
        jeu.montrer()
    
    if jeu.est_complete():
        print("Trop fort ! Quel boss !!!")
    if entree not in ("q", "quit", "exit"):
        input("Appuyer sur entrée pour quitter")
        
        