import interfacelib
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

class Joueur:
	def __init__(self, partie, couleur, opts={}):
		self.couleur = couleur
		self.couleurval = interfacelib.couleur_to_couleurval(couleur)
		self.jeu = partie
		self.opts = opts
		

	def demande_coup(self):
		pass

	


class Humain(Joueur):

	def demande_coup(self):
		pass



class IA(Joueur):
	INFINI = 9999
    
	def __init__(self, partie, couleur, opts={}):
		super().__init__(partie,couleur,opts)
		self.temps_exe = 0
		self.nb_appels_jouer = 0
		self.nbCoups = 0    
		 												
	def coups(self):
		self.nbCoups += 1
	
	def stats(self, profondeurs):
		list_profond = []
		list_nbCoups = []
		list_nbTimes = []
  
		startTotal = time.time()
		for profondeur in range (1, profondeurs + 1):
			list_profond.append(profondeur)

			start = time.time()
			self.minmax(self.jeu.plateau.copie(), self.couleurval, profondeur )
			end = time.time()
			list_nbCoups.append(self.nbCoups)
			list_nbTimes.append(end - start)
			self.nbCoups = 0
   
		endTootal = time.time()
		print("************** stats *******************")
		print("temps total: {} s".format(endTootal - startTotal))
  
		xlabel = 'profondeur'
		self.graphique(list_profond, list_nbCoups, xlabel,'Coups', 'stats nbCoups / profondeur')
		self.graphique(list_profond, list_nbTimes, xlabel, 'times', 'stats times / profondeur')
  
		
  
	def graphique(self, x_values, y_values, xlabel, ylabel,  label):	 
		fig, ax = plt.subplots()

		ax.plot(x_values, y_values, label = label)
  
		# Set the format of the y-axis ticks
		ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_title('Simple Line Plot Example')

		# Add a legend
		ax.legend()

		# Show the plot
		plt.show()
  
	def graphique_double(self, x_values, y1_values, y2_values, xlabel, ylabel, label1, label2, title):
		fig, ax = plt.subplots()

		ax.plot(x_values, y1_values, label=label1)
		ax.plot(x_values, y2_values, label=label2)

		# Set the format of the y-axis ticks
		ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_title(title)

		# Add a legend
		ax.legend()

		# Show the plot
		plt.show()
	
	def performances(self, IA1, IA2, profondeurs):
		list_profond = []
		list_nbTimes1 = []
		list_nbTimes2 = []
  
		startTotal = time.time()
		for profondeur in range (1, profondeurs + 1):
			list_profond.append(profondeur)
			
			list_nbTimes1.append(IA1.tempscoupPerformances(profondeur))
			list_nbTimes2.append(IA2.tempscoupPerformances(profondeur))
   
		endTootal = time.time()
		print("************** stats *******************")
		print("temps total: {} s".format(endTootal - startTotal))
  
		xlabel = 'profondeur'
		ylabel = 'times'
		self.graphique_double(list_profond, list_nbTimes1, list_nbTimes2, xlabel, ylabel,  IA1.__class__.__name__, IA2.__class__.__name__, 'stats Tmes 2 Joueur')
		
	def tempscoupPerformances(self, profondeur):
		start = time.time()
		if isinstance(self, Minmax):
			self.minmax(self.jeu.plateau.copie(), self.couleurval, profondeur )
   
		elif isinstance(self, AlphaBeta):
			self.alphabeta(self.jeu.plateau.copie(), self.couleurval, - IA.INFINI, IA.INFINI, profondeur)

		return  time.time() - start

			
         
class Random(IA):

	def demande_coup(self):
		liste = self.jeu.plateau.liste_coups_valides(self.couleurval)
		
		if len(liste) == 0:
			return []
		return liste[np.random.randint(0, len(liste))]


class Minmax(IA):
	def minmax(self, plateau, couleurval, profondeur):
		self.coups()
		if (not plateau.existe_coup_valide(couleurval) and not plateau.existe_coup_valide(- couleurval) ) or profondeur == 0:
			return (plateau.positionEvaluation(couleurval), None)
		
		if self.couleurval == couleurval: #Player max
			M = - IA.INFINI # infini
			liste_coups = plateau.liste_coups_valides(self.couleurval)
			for coup in liste_coups:
				plateau1 = plateau.copie()
				plateau1.jouer(coup, self.couleurval)
				val, B = self.minmax(plateau1, - self.couleurval , profondeur - 1)
				if M < val:
					M = val
					argmax = coup
			return (M, argmax)

		else:
			m = IA.INFINI
			liste_coups = plateau.liste_coups_valides(couleurval)
			for coup in liste_coups:
				plateau1 = plateau.copie()
				plateau1.jouer(coup, couleurval)
				val, B = self.minmax(plateau1, - self.couleurval, profondeur - 1)
				if m > val:
					m = val
					argmin = coup
			return (m, argmin)

	def minmax2(self, plateau, couleurval, profondeur):
			self.coups()
			if not plateau.existe_coup_valide(couleurval) or profondeur == 0:
				return (plateau.positionEvaluation(couleurval), None)

			
			bestEval = {"coup": None, "score": 0}
			if self.couleurval == couleurval: #Player max
				M = - IA.INFINI # infini
				liste_coups = plateau.liste_coups_valides(self.couleurval)
				for coup in liste_coups:
					plateau1 = plateau.copie()
					plateau1.jouer(coup, self.couleurval)
					score = plateau1.positionEvaluation(self.couleurval)
					if bestEval['coup'] == None or bestEval['score'] < score:
						bestEval['coup'] = coup
						bestEval['score'] = score
						
				val, B = self.minmax2(plateau1, - self.couleurval , profondeur - 1)
				return (val, coup)

			else:
				m = IA.INFINI
				liste_coups = plateau.liste_coups_valides(couleurval)
				for coup in liste_coups:
					plateau1 = plateau.copie()
					plateau1.jouer(coup, couleurval)
					val, B = self.minmax2(plateau1, - self.couleurval, profondeur - 1)
					if m > val:
						m = val
						argmin = coup
				return (m, argmin)

	def demande_coup(self):
		
		start = time.time()
		M, argmax = self.minmax(self.jeu.plateau.copie(), self.couleurval, np.random.randint(1, 6))
		end = time.time()
		
		self.temps_exe += (end - start)
		
		if argmax == None:
			return []
		return argmax
		


class AlphaBeta(IA):
	def alphabeta(self, plateau, couleurval, alpha, beta, profondeur):
		if (not plateau.existe_coup_valide(couleurval) and not plateau.existe_coup_valide(- couleurval) ) or profondeur == 0:
			return (plateau.positionEvaluation(couleurval), None)

		if self.couleurval == couleurval: #Player max
			M = - IA.INFINI # infini
			liste_coups = plateau.liste_coups_valides(self.couleurval)
			for coup in liste_coups:
				plateau1 = plateau.copie()
				plateau1.jouer(coup, self.couleurval)
				val, B = self.alphabeta(plateau1, - self.couleurval , alpha, beta, profondeur - 1)
				if M < val:
					M = val
					argmax = coup
					alpha = max(alpha, M)
				if alpha >= beta:
					break
			return (M, argmax)
		
		else:
			m = IA.INFINI
			liste_coups = plateau.liste_coups_valides(couleurval)
			for coup in liste_coups:
				plateau1 = plateau.copie()
				plateau1.jouer(coup, couleurval)
				val, B = self.alphabeta(plateau1, - self.couleurval, alpha, beta, profondeur - 1)
				if m > val:
					m = val
					argmin = coup
					beta = min(beta, m)
				if alpha >= beta:
					break
			return (m, argmin)

	def demande_coup(self):
		start = time.time()
		M, argmax = self.alphabeta(self.jeu.plateau.copie(), self.couleurval, - IA.INFINI, IA.INFINI, np.random.randint(1, 6))
		end = time.time()
		
		self.temps_exe += (end - start)
		
		if argmax == None:
			return []
		return argmax