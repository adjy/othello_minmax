import jeulib

import joueurlib
#jeu.joueur_courant = joueurlib.IA
opts = {"choix_joueurs": False}


jeu = jeulib.Jeu(opts)
jeu.noir = joueurlib.Minmax(jeu, "noir", opts)
jeu.blanc = joueurlib.AlphaBeta(jeu, "blanc", opts)


jeu.joueur_courant = jeu.noir

jeu.joueur_courant.performances(jeu.noir, jeu.blanc, 15)
