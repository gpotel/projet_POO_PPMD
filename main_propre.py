# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Auteur : gpotel
"""

import random as rd
import copy as cp
import numpy as np 



class Grille():
    """ Représente une grille de sudoku 
    
    Attributs
    ---------
    taille : int
        Taille de la grille (9 pour une grille usuelle)
    grille : np.ndarray
        Tableau 2D contenant les valeurs du Sudoku (à = vide)
    bloquee : np.ndarray
        Tableau 2d booléen indiquant si une case est bloquée (True) ou libre (False)
    
    """
    def __init__(self, taille):
        """
        Initialise les paramètres de la grille. 

        Parameters
        ----------
        taille : int
            Taille de la grille

        """
        self.taille = taille
        self.grille = np.zeros((self.taille,self.taille))
        self.bloquee = np.zeros((self.taille,self.taille))
    
    def en_matrice(self, liste):
        """
        Inititalise la grille à partir d'une liste existante de chiffres et marque les cases non-nulles comme bloquées

        Parameters
        ----------
        liste : list[list[int]]
            Liste contenant les valeurs du sudoku (0 = cases vides)

        """
        self.grille = np.array(liste)
        self.bloquee = self.grille != 0
      
    def en_liste(self):
        """
        Transforme la grille de sudoku en liste de listes

        Returns
        -------
        list[list[int]]
            Grille sous forme de liste

        """
        return self.grille.tolist()
    
    def est_correct(self, ligne:int, colonne:int, valeur:int):
        """
        Vérifie si une valeur peut-être placée à une position donnée (selon les règles du sudoku)

        Parameters
        ----------
        ligne : int
            Indice de ligne (0-8)
        colonne : int
            Indice de colonne (0-8)
        valeur : int
            Valeur à tester (1-9)

        Returns
        -------
        bool
            True si la valeur peut-être placée, False sinon

        """
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
        """
        Essaye de placer une valeur à une position donnée

        Parameters
        ----------
        ligne : int
            Indice de ligne (0-8)
        colonne : int
            Indice de colonne (0-8)
        valeur : int
            Valeur à tester (1-9)

        Returns
        -------
        bool
            True si la valeur est placée, False sinon

        """
        if self.bloquee[ligne, colonne]:
            return False
        if valeur == 0:
            return self.vider_case(ligne, colonne)
        if self.est_correct(ligne, colonne, valeur):
            self.grille[ligne, colonne] = valeur
            return True
        return False
    
    def vider_case(self, ligne, colonne):
        """
        Vide une case si elle n'est pas bloquée

        Parameters
        ----------
        ligne : int
            Indice de ligne (0-8)
        colonne : int
            Indice de colonne (0-8)

        Returns
        -------
        bool
            True si la case est vidée, False sinon

        """
        if self.bloquee[ligne, colonne]:
            return False
        self.grille[ligne, colonne] = 0
        return True
    
    def est_complete(self):
        """
        Indique si la grille est entièrement remplie

        Returns
        -------
        bool
            True si la grille est complète, False sinon

        """
        return self.case_vide() is None
    
    def case_vide(self):
        """
        Trouve une case vide de la grille

        Returns
        -------
        tuple(int, int) ou None
            Coordonnées (ligne, colonne) de la case vide, None si la grille est complète

        """
        vide = np.argwhere(self.grille == 0)
        if vide.size:
            return tuple(vide[0])
        else:
            return None
    
    def set_difficulte():
        pass
        #Permet de sélectionner une difficulté (le nombre de chiffres initialement présents sur la grille)



class GenerateurSudoku():
    """
    Génère aléatoirement des grilles de sudoku valides
    
    Attributs
    ---------
    difficulte : int
        Nombre de cases à retirer pour définir la difficulté
    
    """
    
    def __init__(self, difficulte=40):
        """
        Initialise le générateur avec sa difficulté

        Parameters
        ----------
        difficulte : int, optional
            Nombre de cases à retirer de la grille. On le met à 40 par défaut (la moitié de la grille)

        """
        self.difficulte = difficulte
        
    def generer_grille(self):
        """
        Génère une grille de sudoku pleine, puis retire des cases
        pour créer une grille jouable

        Returns
        -------
        grille : Grille
            Objet Grille contenant la configuration initiale du sudoku

        """
        grille = Grille(9)
        self._remplir_grille_aleatoire(grille)
        solution = cp.deepcopy(grille.grille)
        self._retirer_cases(grille)
        grille.solution = solution
        return grille
        #Génère la grille pleine
    
    def _remplir_grille_aleatoire(self, grille):
        """
        Remplit récursivement la grille de sudoku entière et en "bloque" toutes les cases

        Parameters
        ----------
        grille : Grille
            Grille à remplir

        """
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
        """
          Retire des cases d'une grille au hasard en s'assurant qu'il existe une solution unique

        Parameters
        ----------
        grille : Grille
            Grille complète à vider
        nb_tentative : int, optional
            Nombre de tentative à réaliser (pour garantir l'uncicité) avant d'abandonner. La valeur par défaut est 1000

        """
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
            copie.en_matrice(cp.deepcopy(grille.grille))
            resolveur = ResolveurSudoku(copie)
            nb_solutions = self._compter_solutions(resolveur, limite=2)
            
            if nb_solutions != 1:
                grille.grille[ligne, colonne] = valeur_sauv
                grille.bloquee[ligne, colonne] = True
            else:
                cases_a_retirer -= 1
            tentative += 1
    
    def _compter_solutions(self, resolveur, limite=2):
        """
        Compte le nombre de solutions possibles pour une grille donnée

        Parameters
        ----------
        resolveur : ResolveurSudoku
            Objet servant à résoudre la grille
        limite : int, optional
            Nombre maximal de solutions à chercher avant d'arrêter. La valeur par défaut est 2

        Returns
        -------
        int
            Nombre de solutions trouvées

        """
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
    """
    Résout une grille de sudoku donnée à l'aide d'un algorithme récursif
    
    Attributs
    ---------
    grille : Grille
        Grille de sudoku à résoudre
    
    """
    def __init__(self, grille):
        """
        Initialise le résolveur

        Parameters
        ----------
        grille : grille
            Grille à résoudre

        """
        self.grille = grille
    
    def resoudre(self):
        """
        Résout la grille de sudoku

        Returns
        -------
        bool
            True si la grille a été résolue, False sinon

        """
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



class Jeu():
    """
    Gère la logique du jeu côté joueur : affichage, saisie, ...
    
    Attributs
    ---------
    grille : Grille
        Grille de sudoku active
    anotations : list[list[set(int)]]
        Tableau contenant les annotations du joueur pour chaque case
    
    """
    
    #       Version qui résoud automatiquement la grille
    # def __init__(self, grille_initiale):
    #     self.grille = Grille(9)
    #     if grille_initiale is not None:
    #         self.grille.en_matrice(grille_initiale, True)
    #     self.resolveur = ResolveurSudoku(self.grille)
    
    # def resoudre(self):
    #     print("Résolution en cours \n")
    #     if self.resolveur.resoudre():
    #         print("Sudoku résolu")
    #         print(self.grille)
    #     else:
    #         print("Aucune solution trouvée ... :(")
    
    # def montrer(self):
    #     print(self.grille)

    def __init__(self, grille_initiale, solution = None, verif_solution = False):
        """
        Initialise le jeu avec une grille

        Parameters
        ----------
        grille_initiale : list[list[int]]
            Grille de départ du sudoku

        """
        self.grille = Grille(9)
        if grille_initiale is not None:
            self.grille.en_matrice(grille_initiale)
        if solution is not None:
            self.solution = np.array(solution)
        else:
            self.solution = None
        self.verif_solution = verif_solution
        self.annotations = [[set() for i in range(9)] for j in range(9)]
            
    def montrer(self):
        """
        Affiche la grille actuelle et les annotations dans la console

        """
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
        """
        Tente de placer une valeur dans une case donnée et supprime les annotations si nécessaire

        Parameters
        ----------
        ligne : int
            Indice de ligne (0-8)
        colonne : int
            Indice de colonne (0-8)
        valeur : int
            Valeur à tester (1-9)

        Returns
        -------
        bool
            True si le coup est valide et joué, False sinon

        """
        if self.grille.bloquee[ligne, colonne]:
            print("\nLa case est fixée")
            return False
        if valeur == 0:
            print(f"\nEffacement ({ligne+1}, {colonne+1})")
            return self.retirer_coup(ligne, colonne)
        if not self.grille.est_correct(ligne, colonne, valeur):
            print(f"\n{valeur} ne peut pas être placée en ({ligne+1},{colonne+1})")
            return False
        
        #Vérification optionnelle avec la solution
        if self.verif_solution and self.solution is not None :
            if valeur != self.solution[ligne, colonne]:
                print(f"\nErreur : {valeur} n'est pas la bonne valeur à ({ligne+1},{colonne+1})")
                return False
        
        self.grille.completer_case(ligne, colonne, valeur)
        carre_ligne = ligne // 3
        carre_colonne = colonne // 3
        for i in range(3):
            for j in range(3):
                ind_i = carre_ligne * 3 + i
                ind_j = carre_colonne * 3 + j
                if valeur in self.annotations[ind_i][ind_j]:
                    self.annotations[ind_i][ind_j].remove(valeur)
        print(f"\n{valeur} placé en ({ligne+1}, {colonne+1})")
        return True
    
    def retirer_coup(self, ligne, colonne):
        """
        Efface la valeur d'une case si elle n'est pas bloquée
        
        Parameters
        ----------
        ligne : int
            Indice de ligne (0-8)
        colonne : int
            Indice de colonne (0-8)
        
        Returns
        -------
        bool
            True si la case a été vidée, False sinon
        
        
        """
        return self.grille.vider_case(ligne, colonne)
    
    def est_complete(self):
        """
        Indique si la grille est entièrement remplie

        Returns
        -------
        bool
            True si la grille est complète, False sinon

        """
        return self.grille.est_complete()
    
    def annoter_case(self, ligne, colonne, chiffre):
        """
        Ajoute ou retire une annotation dans une case

        Parameters
        ----------
        ligne : int
            Indice de ligne (0-8)
        colonne : int
            Indice de colonne (0-8)
        valeur : int
            Valeur à tester (1-9)

        Returns
        -------
        bool
            True si l'annotation a été modifiée, False sinon

        """
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

#####   Fonctions utilitaires #####
def mode_verif(jeu):
    jeu.verif_solution = not jeu.verif_solution
    if jeu.verif_solution:
        etat = "activée" 
    else:
        etat = "désactivée"
        print(f"\nVérification par rapport à la solution {etat}")

def traiter_entree(entree, jeu):
    entree = entree.strip().lower()
    
    if entree in ("q", "quit", "exit"):
        print("\nVous avez quitté le jeu :(")
        return False
    
    elif entree.startswith("mode"):
        mode_verif(jeu)
        return True
    
    try:
        parties = entree.split()
        if parties[0] == "a" and len(parties) == 4:
            x, l, c, v = parties
            ligne, colonne, valeur = int(l)-1, int(c)-1, int(v)
            if not (0 <= ligne <= 8 and 0 <= colonne <= 8 and 0 <= valeur <= 9):
                print("Vous avez dépassé les bornes ! 1-9 pour les cases, 1-9 pour les valeurs et 0 pour effacer")
                    
            jeu.annoter_case(ligne, colonne, valeur)
        else:
            ligne, colonne, valeur = map(int, parties)
            ligne -= 1
            colonne -= 1
            if not (0 <= ligne <= 8 and 0 <= colonne <= 8 and 0 <= valeur <= 9):
                print("Vous avez dépassé les bornes ! 1-9 pour les cases, 1-9 pour les valeurs et 0 pour effacer")
                    
            jeu.jouer_coup(ligne, colonne, valeur)
                
    except ValueError:
        print("Format invalide : concentre toi")
        
    return True

def afficher_grille(jeu):
    print("\n")
    jeu.montrer()
    
def main():
    generateur = GenerateurSudoku()
    grille_sudoku = generateur.generer_grille()
    jeu = Jeu(grille_sudoku.en_liste(), solution = grille_sudoku.solution, verif_solution=True)
    print('"q" pour quitter')
    print('"mode" pour regarder la vérification')
    print('"a Ligne Colonne Valeur" pour annoter')
    print('"Ligne Colonne Valeur" pour compléter')
    afficher_grille(jeu)
    while not jeu.est_complete():
        entree = input('Entrer une commande (ex : 3 3 5): ').strip().lower()
        continuer = traiter_entree(entree, jeu)
        if not continuer:
            break
        afficher_grille(jeu)
    
    if jeu.est_complete():
        print("Trop fort ! Tié un tigre !!!")

if __name__ == "__main__":
    main()
    # generateur = GenerateurSudoku()
    # grille_sudoku = generateur.generer_grille()
    
    # jeu = Jeu(grille_sudoku.en_liste(), solution = grille_sudoku.solution, verif_solution=True)
    # print("Sudoku généré :\n")
    # jeu.montrer()
    
    # while not jeu.est_complete():
    #     entree = input('Ligne Colonne Valeur ("a Ligne Colonne Valeur" pour annoter, q pour quitter):').strip().lower()
    #     if entree in ("q", "quit", "exit"):
    #         print("\nVous avez quitté le jeu :(")
    #         break
        
    #     elif entree.startswith("mode"):
    #         jeu.verif_solution = not jeu.verif_solution
    #         if jeu.verif_solution:
    #             etat = "activée" 
    #         else:
    #             etat = "désactivée"
    #         print(f"\nVérification par rapport à la solution {etat}")
    #         continue
        
    #     try:
    #         parties = entree.split()
    #         if parties[0] == "a" and len(parties) == 4:
    #             x, l, c, v = parties
    #             ligne, colonne, valeur = int(l)-1, int(c)-1, int(v)
    #             if not (0 <= ligne <= 8 and 0 <= colonne <= 8 and 0 <= valeur <= 9):
    #                 print("Vous avez dépassé les bornes ! 1-9 pour les cases, 1-9 pour les valeurs et 0 pour effacer")
    #                 continue
    #             jeu.annoter_case(ligne, colonne, valeur)
    #         else:
    #             ligne, colonne, valeur = map(int, parties)
    #             ligne -= 1
    #             colonne -= 1
    #             if not (0 <= ligne <= 8 and 0 <= colonne <= 8 and 0 <= valeur <= 9):
    #                 print("Vous avez dépassé les bornes ! 1-9 pour les cases, 1-9 pour les valeurs et 0 pour effacer")
    #                 continue
    #             jeu.jouer_coup(ligne, colonne, valeur)
                
    #     except ValueError:
    #         print("Format invalide : concentre toi")
    #         continue
        
    #     print("\n")
        
    #     jeu.montrer()
    
    # if jeu.est_complete():
    #     print("Trop fort ! Quel boss !!!")
    # if entree not in ("q", "quit", "exit"):
    #     input("Appuyer sur entrée pour quitter")
        
        