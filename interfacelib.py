from __future__ import division

from PIL import ImageTk
from PIL import Image, ImageDraw
import tkinter as tk
import time

import joueurlib

class Interface():

	def __init__(self, jeu, taille_img=400):

		self.taille_img = taille_img
		self.jeu = jeu
		self.coup = None

		self.init_fenetre()
		self.message_tour = tk.StringVar()
		self.message_tour.set("A noir de jouer")
		self.ajoute_message_tour()
		self.ajoute_plateau()
		self.ajoute_bouton_quitter()

		self.flag_humain_active = False
		self.flag_ia_active = False

	def init_fenetre(self):
		self.fenetre = tk.Tk()
		self.fenetre.title("Othello")

	def ajoute_message_tour(self):
		label_tour = tk.Label(textvariable=self.message_tour)
		label_tour.pack()

	def ajoute_plateau(self):
		linewidth = 5
		self.img_plateau = gen_img_plateau(8, self.taille_img, linewidth)
		for i in range(self.jeu.plateau.taille):
			for j in range(self.jeu.plateau.taille):
				if self.jeu.plateau.tableau_cases[i][j] == 1:
					ajoute_img_pierre([i,j], "black", self.img_plateau, self.jeu.plateau.taille, linewidth)
				elif self.jeu.plateau.tableau_cases[i][j] == -1:
					ajoute_img_pierre([i,j], "white", self.img_plateau, self.jeu.plateau.taille, linewidth)

		self.canvas = tk.Canvas(master=self.fenetre, width=self.taille_img, height=self.taille_img)
		self.canvas.pack(side=tk.LEFT)

		self.tkimg_plateau = ImageTk.PhotoImage(self.img_plateau, master=self.canvas)
		self.image_on_canvas = self.canvas.create_image(0,0, anchor=tk.NW, image=self.tkimg_plateau)

	def actualise_plateau(self):
		linewidth = 5
		self.img_plateau = gen_img_plateau(8, self.taille_img, linewidth)
		for i in range(self.jeu.plateau.taille):
			for j in range(self.jeu.plateau.taille):
				if self.jeu.plateau.tableau_cases[i][j] == 1:
					ajoute_img_pierre([i,j], "black", self.img_plateau, self.jeu.plateau.taille, linewidth)
				elif self.jeu.plateau.tableau_cases[i][j] == -1:
					ajoute_img_pierre([i,j], "white", self.img_plateau, self.jeu.plateau.taille, linewidth)

		self.tkimg_plateau = ImageTk.PhotoImage(self.img_plateau, master=self.canvas)
		self.canvas.itemconfig(self.image_on_canvas, image=self.tkimg_plateau)

	def ajoute_bouton_pass(self):
		self.bouton_pass = tk.Button(text="Passer", width=10, height=3, bg="grey", fg="white")
		self.bouton_pass.pack(side=tk.LEFT)
		self.bouton_pass.bind('<Button-1>', lambda event: self.humain_passe())

	def bind_plateau(self):
		self.canvas.bind("<Button-1>", lambda event: self.humain_joue(event))

	def ajoute_bouton_quitter(self):
		self.bouton_quitte = tk.Button(text="Quitter", width=10, height=3, bg="grey", fg="white")
		self.bouton_quitte.pack(side=tk.BOTTOM)
		self.bouton_quitte.bind('<Button-1>', lambda event: self.quitter())

	def ajoute_bouton_tour_ia(self):
		self.bouton_tour_ia = tk.Button(text="Tour IA", width=10, height=3, bg="grey", fg="white")
		self.bouton_tour_ia.pack(side=tk.TOP)
		self.bouton_tour_ia.bind('<Button-1>', lambda event: self.ia_joue())

	def quitter(self):
		self.fenetre.destroy()

	def humain_passe(self):
		couleurval = self.jeu.joueur_courant.couleurval
		if not self.jeu.plateau.existe_coup_valide(couleurval):
			self.jeu.jouer([])
			if not self.jeu.partie_finie:
				if isinstance(self.jeu.joueur_courant, joueurlib.IA):
					self.desactive_humain() #pour empecher l'humain de jouer si c'est le tour de l'ia
					self.active_ia()

	def humain_joue(self, event):
		case = self.clic_to_coord(event)
		couleurval = couleur_to_couleurval(self.jeu.joueur_courant.couleur)
		if min(case[0], case[1])>=0 and max(case[0],case[1]<self.jeu.plateau.taille) and self.jeu.plateau.est_coup_valide(case, couleurval):
			self.jeu.jouer(case)
			if not self.jeu.partie_finie and isinstance(self.jeu.joueur_courant, joueurlib.IA):
				self.desactive_humain() #pour empecher l'humain de jouer si c'est le tour de l'ia
				self.active_ia()

	def desactive_humain(self):
		if self.flag_humain_active:
			self.canvas.unbind("<Button-1>")
			self.bouton_pass.destroy()
			self.flag_humain_active = False

	def active_humain(self):
		if not self.flag_humain_active:
			self.ajoute_bouton_pass()
			self.bind_plateau()
			self.flag_humain_active = True

	def desactive_ia(self):
		if self.flag_ia_active:
			#self.bouton_tour_ia.destroy()
			self.flag_ia_active = False

	def active_ia(self):
		if not self.flag_ia_active:
			#self.ajoute_bouton_tour_ia()
			self.flag_ia_active = True
		self.ia_joue()

	def ia_joue(self):
		assert isinstance(self.jeu.joueur_courant, joueurlib.IA)
		coup = self.jeu.joueur_courant.demande_coup()
		self.jeu.jouer(coup)
		if not self.jeu.partie_finie:
			if not isinstance(self.jeu.joueur_courant, joueurlib.IA):
				self.desactive_ia()
				self.active_humain()
			else:
				self.ia_joue()

	def rien_faire(self):
		pass

	def clic_to_coord(self, event):
		i = int(event.x / self.taille_img * self.jeu.plateau.taille)
		j = int(event.y / self.taille_img * self.jeu.plateau.taille)
		return [i,j]


def couleur_to_couleurval(couleur):
	if couleur == "noir":
		return 1
	elif couleur == "blanc":
		return -1

def gen_img_plateau(nb_cases=8, taille_image=400, linewidth=5):
	im = Image.new('RGB', (taille_image, taille_image), (0, 175, 30))
	draw = ImageDraw.Draw(im)

	for i in range(nb_cases+1):
		draw.line((linewidth/2, linewidth/2+(taille_image - linewidth)/nb_cases*i,
				taille_image-linewidth/2, linewidth/2 + (taille_image - linewidth)/nb_cases*i), width=5, fill=15)
		draw.line((linewidth/2 + (taille_image - linewidth)/nb_cases*i, 0,
			   linewidth/2 + (taille_image - linewidth)/nb_cases*i, taille_image), width=5, fill=15)
	return im


def ajoute_img_pierre(coord, couleur, im_plateau, nb_cases=8, linewidth=5):
	taille_image = im_plateau.size[0] #suppose image carrée
	draw = ImageDraw.Draw(im_plateau)
	draw.ellipse((linewidth+coord[0]*(taille_image-linewidth)/nb_cases,
			  linewidth+coord[1]*(taille_image - linewidth)/nb_cases,
			  (coord[0]+1)*(taille_image - linewidth)/nb_cases,
			  (coord[1]+1)*(taille_image - linewidth)/nb_cases), fill = couleur, outline ="black")



