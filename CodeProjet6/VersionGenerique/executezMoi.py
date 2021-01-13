#!/usr/bin/python3.9
# -*-coding:utf-8 -*

# test execution bash via python
import re
from subprocess import call

# le necessaire pour la boite de dialogue 
import tkinter as tk
from tkinter.filedialog import askopenfilename
root = tk.Tk()
root.withdraw()

#-------------- Variables ------------------------------------------

#ces variables doivent correspondre aux variables des script bash
#c'est la liste des occurences qui seront remplacées par le string.replace(ancienne occurence, nouvelle occurence)
listeOccuARemplPostes = ['nomUserSSH','hoteSSH','mdpUserSSH']


#--------------Fin Variables ---------------------------------------


#--------------Lecture des fichiers et mise en variables--------------------------------

#on lit le fichier puis on lancera la chaine avec call apres modification des valeurs
with open('bash/nePasModifier', 'r') as fichier:
    bashPreRempli = fichier.read()

#on lit votre fichier avec vos commandes a effectuer pour les incorporer dans bashPreRempli
chemin = askopenfilename()
with open(chemin, 'r') as fichier:
	#le strip() est important car la commande << eof gere pas les indentations
    bashChoisi = fichier.read().strip()

#on incorpore bashChoisi dans bashPreRempli
bashPreRempli = bashPreRempli.replace('XXXmonBashXXX',bashChoisi)

#recupération des valeurs des postes distants
with open('listePostesDistants', 'r') as fichier:
	#on lit et on sépare chaque lignes dans une liste
    listePostesDistants = fichier.read().replace(",",";").replace(":",";").splitlines()
    #on enleve le premier element (ce sont les titres de colonnes)
    del listePostesDistants[0]
    
#-------------- Fin Lecture des fichiers --------------------------------


#-------------- Fonctions -----------------------------------------------  
  
def remplirScriptBash(lstParam,lstVal,stScript):
	"""Cette fonction utilise la fonction replace de string.
	Premier parametre lstParam est une liste de string des occurences qui seront remplacé
	Deuxieme parametre lstVal est la nouvelle valeur
	Le troisieme parametre est la chaine où seront effectué les remplacements
	
	lstVal[0] remplacera lstParam[0] dans stScript puis [1] ...[2] etc
	
	"""
	i=0
	#on parcours la liste de valeur car sa taille peut varier
	for stVal in lstVal:
		#exemple :  remplace nomParam="" par monParam="Ma Valeur"
		stScript = stScript.replace(lstParam[i] + '=""',lstParam[i] + '="' + stVal + '"')
		i += 1	
	return stScript
	
#-------------------------------------------------------------------------- 

def executeScriptSurChaquePoste(script):
	"""Se connecte en ssh a partir d'une liste de postes distant puis execute le script
	
	"""
	for stringLigne in listePostesDistants:
		# on sépare les valeurs avec le ; 
		listeInfoPoste = stringLigne.split(";")
		scriptFinal = remplirScriptBash(listeOccuARemplPostes,listeInfoPoste,script)
		rc = call(scriptFinal, shell=True,executable="/bin/bash")
		
#-------------------------------------------------------------------------- 

#-------------Fin Fonctions ---------------------------------------------
#========================  Partie Main   ============================================

executeScriptSurChaquePoste(bashPreRempli)
input("Tapez n'importe où pour quitter")
